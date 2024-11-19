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

import gigametr as gm


first_model = {"name": "GigaSFT", "data": "./test_data/test_samples_1_single.json"}

res = gm.sbs.create(
    name="Test data check 1", first=first_model, address="gm.pp.ru", type="single"
)
# %%
# save texts and meta
import json

with open("./test_data/demo_sample_100.jsonl", "r", encoding="utf8") as fin:
    docs = [json.loads(x) for x in fin.read().splitlines()]
    texts = []
    meta = []

    for d in docs:
        acc = []
        for m in d["messages"]:
            if "trainable" in m:
                traniable_sign = " 🟢" if m["trainable"] else " 🔵"
            else:
                traniable_sign = ""
            acc.append(f"—{traniable_sign} [{m['role']}] {m['content']}")
        text = "\n\n".join(acc)
        texts.append(text)
        meta.append(d["meta"])

json.dump(
    texts,
    open("./test_data/demo_100.json", "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)

json.dump(
    meta,
    open("./test_data/demo_100_meta.json", "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)

# %%
import gigametr as gm
# import src.gigametr as gm


first_model = {"name": "GigaSFT 1", "data": "./test_data/demo_100.json", "meta": "./test_data/demo_100_meta.json"}
# first_model = {"name": "GigaSFT 1", "data": "./test_data/demo_100.json"}

res = gm.sbs.create(
    name="Test data demo 1", first=first_model, address="localhost", type="single"
)

print(f"\n\nhttp://localhost:5173/data/check/{res['id']}")


# %%

#pip install gigametr==0.2.2

import gigametr as gm

first_model = {"name": "GigaSFT 1", "data": "./test_data/demo_100.json", "meta": "./test_data/demo_100_meta.json"}

res = gm.sbs.create(
    name="Test data demo 1", first=first_model, address="gm.pp.ru", type="single"
)

# %%
#GET COMMENTS
import gigametr as gm
import json

sbs_guid = "417d79e90ad843e29d62846730b79e15"

comments = gm.sbs.get_comments(sbs_guid=sbs_guid, address="gm.pp.ru")

json.dump(comments, open(f'./comments_{sbs_guid}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


# %%
#GET RESULTS
import gigametr as gm
import json

sbs_guid = "417d79e90ad843e29d62846730b79e15"

actions = gm.sbs.get_actions(sbs_guid=sbs_guid, address="gm.pp.ru")

actions = [{'id': x['id'], 'prompt': x['prompt_1'], 'res': 'Не база'} for x in actions['data'] if x['res'] == 'both_bad']

for a in actions:
    c = [x for x in comments['data'] if x['id'] == a['id']]
    if c:
        a['comment'] = c[0]['comment']


json.dump(actions, open(f'./no_baza_{sbs_guid}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


# %%
comments
# %%
actions
# %%
