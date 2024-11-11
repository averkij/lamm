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
#save as plain list
import json

with open('./test_data/demo_sample_100.jsonl', 'r', encoding='utf8') as fin:
    docs = [json.loads(x) for x in fin.read().splitlines()]
    res = []

    for d in docs:
        text = [f"— [{x['role']}] {x['content']}" for x in d['messages']]
        text = '\n\n'.join(text)

        res.append(text)

json.dump(res, open('./test_data/demo_100.json', 'w', encoding='utf8'), ensure_ascii=False, indent=4)        

# %%
import gigametr as gm


first_model = {"name": "GigaSFT 1", "data": "./test_data/demo_100.json"}

res = gm.sbs.create(
    name="Test data demo 1", first=first_model, address="localhost", type="single"
)

print(f"\n\nhttp://localhost:5173/data/check/{res['id']}")


# %%
first_model = {"name": "GigaSFT", "data": "./test_data/demo_100.json"}

res = gm.sbs.create(
    name="Test data demo 1", first=first_model, address="gm.pp.ru", type="single"
)
# %%
