import logging
import os
import sqlite3
import constants as con
import helper


# states: 0 - new, started, 3 - finished, stopped


def create_db(sbs_guid, sbs_name, model_name_1, model_name_2, extra_data):
    """Init SBS database"""
    db_path = helper.get_sbs_path(sbs_guid)
    curr_time = helper.get_curr_time()

    if not os.path.isfile(db_path):
        logging.info(f"Creating SBS db: {db_path}")
        with sqlite3.connect(db_path) as db:
            db.execute(
                """create table info(
                        id integer primary key,
                        guid text UNIQUE,
                        name text,
                        model_1 text,
                        model_2 text,
                        state integer,
                        create_ts text,
                        extra_data text default '{}' NOT NULL
                    )"""
            )
            db.execute(
                """create table tasks(
                        id integer primary key,
                        question_1 text,
                        question_2 text,
                        answer_1 text,
                        answer_2 text,
                        get_count int default 0 NOT NULL,
                        answer_count int default 0 NOT NULL,
                        meta_1 text default '{}' NOT NULL,
                        meta_2 text default '{}' NOT NULL
                       )"""
            )
            db.execute(
                """create table users(
                        id integer primary key,
                        guid text UNIQUE,
                        name text
                       )"""
            )
            db.execute(
                """create table history(
                        id integer primary key,
                        task_id integer NOT NULL,
                        try_id text NULL,
                        user_id integer NOT NULL,
                        event_id int default 0 NOT NULL,
                        insert_ts text NOT NULL,
                        comment text NULL
                       )"""
            )
            db.execute("""create index ix_history_try_id on history (try_id);""")

            db.execute("create table version(id integer primary key, version text)")

            db.execute(
                "insert into info(guid, name, model_1, model_2, state, create_ts, extra_data) values (?, ?, ?, ?, ?, ?, ?)",
                (
                    sbs_guid,
                    sbs_name,
                    model_name_1,
                    model_name_2,
                    0,
                    curr_time,
                    extra_data,
                ),
            )
            db.execute("insert into version(version) values (?)", (con.DB_VERSION,))


def fill_db(sbs_guid, items_1, items_2):
    """Check data and fill database"""
    db_path = helper.get_sbs_path(sbs_guid)
    logging.info(f"Filling SBS db: {db_path}")
    with sqlite3.connect(db_path) as db:
        db.executemany(
            "insert into tasks(question_1, question_2, answer_1, answer_2, meta_1, meta_2) values (?,?,?,?,?,?)",
            [
                (
                    data_1[0],
                    data_2[0],
                    data_1[1],
                    data_2[1],
                    data_1[2],
                    data_2[2],
                )
                for data_1, data_2 in zip(items_1, items_2)
            ],
        )


def ensure_user_exists(sbs_guid, user_guid):
    """Add or update user for count statistics"""
    db_path = helper.get_sbs_path(sbs_guid)
    logging.info(f"Add user. Guid:{user_guid}")
    with sqlite3.connect(db_path) as db:
        db.execute(
            """insert or replace into users (id, guid) values (
                (select u.id from users u where u.guid=?),?)""",
            (user_guid, user_guid),
        )


def update_sbs_state(sbs_guid, state):
    """Update SBS state"""
    db_path = helper.get_sbs_path(sbs_guid)
    with sqlite3.connect(db_path) as db:
        db.execute("update info set state=?", (state,))


def get_tasks(sbs_guid, user_guid, try_id, n=1):
    """Get tasks for SBS"""
    db_path = helper.get_sbs_path(sbs_guid)
    curr_time = helper.get_curr_time()

    with sqlite3.connect(db_path) as db:
        db_version = get_version(sbs_guid)
        # get tasks
        print("DB VERSION", db_version)
        if db_version >= 0.4:
            tasks = db.execute(
                f"""select
                        t.id, t.question_1, t.question_2, t.answer_1, t.answer_2, t.answer_count, t.meta_1, t.meta_2
                    from
                        tasks t
                    order
                        by t.answer_count, t.get_count, t.id
                    limit ?""",
                (n,),
            ).fetchall()
        else:
            tasks = db.execute(
                f"""select
                        t.id, t.question_1, t.question_2, t.answer_1, t.answer_2, t.answer_count
                    from
                        tasks t
                    order
                        by t.answer_count, t.get_count, t.id
                    limit ?""",
                (n,),
            ).fetchall()

        task_ids = [x[0] for x in tasks]

        logging.info(f"Get {n} tasks. Ids:{', '.join([str(x) for x in task_ids])}")

        # update get count for tasks (sort optimization)
        db.execute(
            """update tasks
                set
                    get_count = get_count + 1
                where
                    id in ({0})""".format(
                ",".join("?" * len(task_ids))
            ),
            task_ids,
        )

        # update history
        db.executemany(
            """insert into history (task_id, try_id, user_id, event_id, insert_ts) values (
                    ?, ?, (select u.id from users u where u.guid=?),?,?
                )""",
            [
                (task_id, try_id, user_guid, con.EVENT_GET, curr_time)
                for task_id in task_ids
            ],
        )

    return tasks


def resolve_task(sbs_guid, user_guid, task_id, try_id, event_id, comment):
    """Process user answer"""
    db_path = helper.get_sbs_path(sbs_guid)
    curr_time = helper.get_curr_time()
    db_version = get_version(sbs_guid)

    with sqlite3.connect(db_path) as db:
        # update history
        if db_version >= 0.3:
            db.execute(
                """insert into history (task_id, try_id, user_id, event_id, insert_ts, comment) values (
                        ?, ?, (select u.id from users u where u.guid=?),?,?,?
                    )""",
                (task_id, try_id, user_guid, event_id, curr_time, comment),
            )
        else:
            db.execute(
                """insert into history (task_id, try_id, user_id, event_id, insert_ts) values (
                        ?, ?, (select u.id from users u where u.guid=?),?,?
                    )""",
                (task_id, try_id, user_guid, event_id, curr_time),
            )

        # update get count for tasks (sort optimization)
        if event_id != con.EVENT_SKIP:
            db.execute(
                """update tasks
                    set
                        answer_count = answer_count + 1
                    where
                        id = ?""",
                (task_id,),
            )


def get_info(sbs_guid):
    """Get SBS info"""
    db_path = helper.get_sbs_path(sbs_guid)

    with sqlite3.connect(db_path) as db:
        data = db.execute(
            """select
                    t.id, t.answer_count, t.get_count
               from
                    tasks t"""
        ).fetchall()

        info = db.execute(
            """select
                    i.guid, i.name, i.model_1, i.model_2, i.state, i.create_ts, i.extra_data
               from
                    info i"""
        ).fetchone()

    return data, info


def get_stat(sbs_guid):
    """Get full SBS stat"""
    db_path = helper.get_sbs_path(sbs_guid)

    with sqlite3.connect(db_path) as db:
        # data = db.execute(
        #     """select
        #             h_get.task_id,
        #             h_answer.event_id as answer_event,
        #             h_get.insert_ts as get_ts,
        #             h_answer.insert_ts as answer_ts
        #         from
        #             history h_get
        #         join
        #             history h_answer
        #                 on h_answer.task_id = h_get.task_id
        #         where
        #             h_get.event_id = 0 and
        #             h_answer.event_id in (1,2,3,4)
        #             """
        # ).fetchall()

        data = db.execute(
            """select
                    h.task_id,
                    h.event_id as answer_event,
                    h.insert_ts as answer_ts
                from
                    history h
                where
                    h.event_id in (1,2,3,4)
                    """
        ).fetchall()

    return data


def get_history(sbs_guid, event_ids=[1, 2, 3, 4]):
    """Get full history with comments"""
    db_path = helper.get_sbs_path(sbs_guid)
    db_version = get_version(sbs_guid)

    # meta is available in 0.4
    if db_version >= 0.4:
        with sqlite3.connect(db_path) as db:
            data = db.execute(
                """select
                        h.task_id,
                        u.guid,
                        t.question_1,
                        t.question_2,
                        t.answer_1,
                        t.answer_2,
                        h.event_id,
                        h.insert_ts,
                        h.comment,
                        t.meta_1,
                        t.meta_2
                    from
                        history h
                            join tasks t on t.id = h.task_id
                            join users u on u.id = h.user_id
                    where
                        h.event_id in ({0})
                    order by
                        h.task_id""".format(
                    ",".join("?" * len(event_ids))
                ),
                event_ids,
            ).fetchall()
    # comments are available in 0.3
    elif db_version >= 0.3:
        with sqlite3.connect(db_path) as db:
            data = db.execute(
                """select
                        h.task_id,
                        u.guid,
                        t.question_1,
                        t.question_2,
                        t.answer_1,
                        t.answer_2,
                        h.event_id,
                        h.insert_ts,
                        h.comment
                    from
                        history h
                            join tasks t on t.id = h.task_id
                            join users u on u.id = h.user_id
                    where
                        h.event_id in ({0})
                    order by
                        h.task_id""".format(
                    ",".join("?" * len(event_ids))
                ),
                event_ids,
            ).fetchall()
    else:
        with sqlite3.connect(db_path) as db:
            data = db.execute(
                """select
                        h.task_id,
                        u.guid,
                        t.question_1,
                        t.question_2,
                        t.answer_1,
                        t.answer_2,
                        h.event_id,
                        h.insert_ts
                    from
                        history h
                            join tasks t on t.id = h.task_id
                            join users u on u.id = h.user_id
                    where
                        h.event_id in ({0})
                    order by
                        h.task_id""".format(
                    ",".join("?" * len(event_ids))
                ),
                event_ids,
            ).fetchall()

    return data


def patch_db(sbs_guid):
    """Patch database schema to the latest version"""
    db_path = helper.get_sbs_path(sbs_guid)
    db_version = get_version(sbs_guid)

    if db_version < float(con.DB_VERSION):
        # add comment field to history table
        with sqlite3.connect(db_path) as db:
            col_comment_exists = db.execute(
                "select count(*) as cnt from pragma_table_info('history') where name='comment'"
            ).fetchone()[0]

            if col_comment_exists == 0:
                db.execute("alter table history add column comment text")

        # update DB version
        with sqlite3.connect(db_path) as db:
            db.execute("update version set version = ?", (con.DB_VERSION,))


def set_answer_counter(sbs_guid, task_id, counter):
    """Set answer counter for a task"""
    db_path = helper.get_sbs_path(sbs_guid)

    with sqlite3.connect(db_path) as db:
        db.execute(
            """update tasks
                set
                    answer_count = ?
                where
                    id = ?""",
            (counter, task_id),
        )


def get_version(sbs_guid):
    """Get SBS DB version"""
    db_path = helper.get_sbs_path(sbs_guid)

    with sqlite3.connect(db_path) as db:
        data = db.execute(
            """select
                        version
                    from
                        version"""
        ).fetchone()

    return float(data[0])
