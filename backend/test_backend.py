# %%
import db_helper

sbs_guid = "b9a14e6583b942ed9247b9200a4ca9c2"
user_guid = "new_user_3"


db_helper.ensure_user_exists(sbs_guid, user_guid)
# %%
tasks = db_helper.get_tasks(sbs_guid, user_guid, n=3)

# %%
tasks

# %%

# EVENT_GET = 0
# EVENT_LEFT_BETTER = 1
# EVENT_RIGHT_BETTER = 2
# EVENT_BOTH_GOOD = 3
# EVENT_BOTH_BAD = 4
# EVENT_SKIP = 5

tasks = db_helper.resolve_task(sbs_guid, user_guid, 3, 1)

# %%
db_helper.get_info(sbs_guid)

# %%
