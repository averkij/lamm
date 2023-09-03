import logging
import os
import pathlib
import sqlite3
import datetime
import json
import constants as con


def create_db(sbs_guid, sbs_name, model_name_1, model_name_2):
    """Init SBS database"""
    sbs_db_path = os.path.join(con.DATA_FOLDER, sbs_guid, f"{sbs_guid}.db")
    if not os.path.isfile(sbs_db_path):
        logging.info(f"Creating SBS db: {sbs_db_path}")
        with sqlite3.connect(sbs_db_path) as db:
            db.execute(
                "create table info(id integer primary key, guid text, name text, model_1 text, model_2 text, state integer, create_ts text)"
            )
            db.execute(
                """create table items(
                        id integer primary key,
                        question_1 text,
                        question_2 text,
                        answer_1 text,
                        answer_2 text,
                        get_count int default 0 NOT NULL,
                        answer_count int default 0 NOT NULL,
                        user_ids text default '[]' NOT NULL
                       )"""
            )
            db.execute(
                """create table users(
                        id integer primary key,
                        guid text,
                        name text,
                        answer_count int
                       )"""
            )
            db.execute("create table version(id integer primary key, version text)")

            db.execute(
                "insert into info(guid, name, model_1, model_2, state, create_ts) values (?, ?, ?, ?, ?, ?)",
                (
                    sbs_guid,
                    sbs_name,
                    model_name_1,
                    model_name_2,
                    0,
                    datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S"),
                ),
            )
            db.execute("insert into version(version) values (?)", (con.DB_VERSION,))


def fill_db(sbs_guid, items_1, items_2):
    """Check data and fill database"""
    sbs_db_path = os.path.join(con.DATA_FOLDER, sbs_guid, f"{sbs_guid}.db")
    logging.info(f"Filling SBS db: {sbs_db_path}")
    with sqlite3.connect(sbs_db_path) as db:
        db.executemany(
            "insert into items(question_1, question_2, answer_1, answer_2) values (?,?,?,?)",
            [
                (
                    data_1[0],
                    data_2[0],
                    data_1[1],
                    data_2[1],
                )
                for data_1, data_2 in zip(items_1, items_2)
            ],
        )
