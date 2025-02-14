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

with open(
    "./test_data/all_sherlock_default_system_with_meta_and_predicted_meta_cleaned_2.json",
    "r",
    encoding="utf8",
) as fin:
    # docs = [json.loads(x) for x in fin.read().splitlines()]
    docs = json.load(fin)
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
        # meta.append(d["meta"])
        id = (
            "-"
            if not "id" in d["sherlock_default_meta"]
            else d["sherlock_default_meta"]["id"]
        )
        meta.append({"source_file": f"sherlock_id_{id}"})
        # print(d['sherlock_default_meta']['id'])

json.dump(
    texts,
    open("./test_data/gemba_3_2.json", "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)

json.dump(
    meta,
    open("./test_data/gemba_3_2_meta.json", "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)

# %%
import gigametr as gm

# import src.gigametr as gm


first_model = {
    "name": "GigaSFT 1",
    "data": "./test_data/demo_100.json",
    "meta": "./test_data/demo_100_meta.json",
}
# first_model = {"name": "GigaSFT 1", "data": "./test_data/demo_100.json"}

res = gm.sbs.create(
    name="Test data demo 1", first=first_model, address="localhost", type="single"
)

print(f"\n\nhttp://localhost:5173/data/check/{res['id']}")

# %%
texts2 = []
metas2 = []

with open("./test_data/gemba_sft_27.1_escaped.json", "r", encoding="utf8") as fin:
    with open("./test_data/gemba_sft_27.1_meta.json", "r", encoding="utf8") as fin_meta:
        texts = json.load(fin)
        metas = json.load(fin_meta)

        for t, m in zip(texts, metas):
            if m["source_file"] == "lmsys-chat-1m-ru_marked":
                texts2.append(t)
                metas2.append(m)

print(len(texts2), len(metas2))

json.dump(
    texts2,
    open("./test_data/gemba_sft_27.1_lmsys.json", "w", encoding="utf8"),
    ensure_ascii=False,
)
json.dump(
    metas2,
    open("./test_data/gemba_sft_27.1_meta_lmsys.json", "w", encoding="utf8"),
    ensure_ascii=False,
)

# %%

# pip install gigametr==0.2.2

import gigametr as gm

first_model = {
    "name": "GigaSFT 1",
    "data": "./test_data/demo_1000_samples_all_sft.json",
    "meta": "./test_data/demo_1000_samples_all_sft_meta.json",
}

first_model = {
    "name": "GigaSFT 1",
    "data": "./test_data/gemba_sft_27.1_krasota.json",
    "meta": "./test_data/gemba_sft_27.1_meta_krasota.json",
}

# first_model = {
#     "name": "Gemba 3",
#     "data": "./test_data/gemba_3_1.json",
#     "meta": "./test_data/gemba_3_1_meta.json",
# }

# first_model = {
#     "name": "Gemba 3",
#     "data": "./test_data/gemba_3_2_escaped.json",
#     "meta": "./test_data/gemba_3_2_meta.json",
# }

res = gm.sbs.create(
    name="Test data demo 1", first=first_model, address="gm.pp.ru", type="single"
)

# %%
# GET COMMENTS
import gigametr as gm
import json

sbs_guid = "417d79e90ad843e29d62846730b79e15"

comments = gm.sbs.get_comments(sbs_guid=sbs_guid, address="gm.pp.ru")

json.dump(
    comments,
    open(f"./comments_{sbs_guid}.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)


# %%
# GET RESULTS
import gigametr as gm
import json

sbs_guid = "417d79e90ad843e29d62846730b79e15"

actions = gm.sbs.get_actions(sbs_guid=sbs_guid, address="gm.pp.ru")

actions = [
    {"id": x["id"], "prompt": x["prompt_1"], "res": "Не база"}
    for x in actions["data"]
    if x["res"] == "both_bad"
]

for a in actions:
    c = [x for x in comments["data"] if x["id"] == a["id"]]
    if c:
        a["comment"] = c[0]["comment"]


json.dump(
    actions,
    open(f"./no_baza_{sbs_guid}.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)


# %%
comments
# %%
actions
# %%
