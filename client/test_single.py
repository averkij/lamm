# %%
import src.gigametr as gm


first_model = {"name": "GigaSFT", "data": "./test_data/test_samples_1_single.json"}


# %%

res = gm.sbs.create(
    name="Test data check 1", first=first_model, address="localhost", type="single"
)

# res = gm.sbs.create(
#     name="Test SBS 17", first=first_model, second=second_model, address="gm.pp.ru"
# )

# %%
res

# %%

gm.sbs.info("bcf0dca9453648b4bc733eef70e13469", address="195.140.147.102")

# %%
import src.gigametr as gm


actions = gm.sbs.get_actions("5c71a9c2ec53441aab2b2b383c675364", address="gm.pp.ru")

# %%
comments = gm.sbs.get_comments("5c71a9c2ec53441aab2b2b383c675364", address="gm.pp.ru")


# %%

# data = gm.sbs.update_db("5c71a9c2ec53441aab2b2b383c675364", address="gm.pp.ru")
# %%
len(actions["data"]), len(comments["data"])


# %%
info = gm.sbs.info("5c71a9c2ec53441aab2b2b383c675364", address="gm.pp.ru")

print(info["solved_tasks"])

# %%
counted = [x for x in info["answer_ids"] if x[1] > 0]

print(len(counted))

counted_ids = [x[0] for x in counted]


# %%
action_ids = [x["id"] for x in actions["data"]]

print(len(action_ids))


# %%

set(counted_ids) - set(action_ids)

# %%
for action in actions["data"]:
    if action["id"] in list(set(counted_ids) - set(action_ids)):
        print(action)


# %%
fix_ids = [528, 529, 531, 532, 533, 683, 786, 830]

import time

for id in fix_ids:
    gm.sbs.debug_set_answer_counter(
        "5c71a9c2ec53441aab2b2b383c675364", id, 0, address="gm.pp.ru"
    )
    time.sleep(5)

# %%
{188, 404, 528, 529, 531, 532, 533, 683, 786, 830}

# %%
import src.gigametr as gm

gm.sbs.debug_update_sbs_state("5c71a9c2ec53441aab2b2b383c675364", 3)
# %%
gm.sbs.debug_update_sbs_state("5c71a9c2ec53441aab2b2b383c675364", 3, address="gm.pp.ru")

# 884c1fe07e494354a93d554e914d116d
# 6e4eb946146446a0a04e934576f3f4f9
# 0890c784a3b6432aa1d1199fcdce2c4d
# 5c71a9c2ec53441aab2b2b383c675364
# %%
