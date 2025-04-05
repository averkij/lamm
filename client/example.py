# %%
# 1. read

import src.gigametr as gm
import json


domains = ["krasota", "travel_creation", "synonims_list", "samopoznanie", "pretrain_hf"]

#%%
for domain in domains:
    input_file = f"./test_data/{domain}_questionable.json"
    with open(
        input_file,
        "r",
        encoding="utf8",
    ) as fin:
        # docs = [json.loads(x) for x in fin.read().splitlines()]
        docs = json.load(fin)
        texts = []
        meta = []

        for d in docs:
            # d looks like [{'role': 'system', 'message_index': 0, 'trainable': False, 'content': nan} #nan is not string
            acc = []
            for m in d:
                # Skip entries with missing, empty, or NaN content
                if m["content"] is None or m["content"] == "" or m["content"] == "nan" or (isinstance(m["content"], float) and m["content"] != m["content"]):
                    continue
                if "trainable" in m:
                    traniable_sign = " 🟢" if m["trainable"] else " 🔵"
                else:
                    traniable_sign = ""
                acc.append(f"—{traniable_sign} [{m['role']}] {m['content']}")
            text = "\n\n".join(acc)
            texts.append(text)

            meta.append({"source_file": f"{domain}"})

    json.dump(
        texts,
        open(f"./test_data/gemba_4_{domain}.json", "w", encoding="utf8"),
        ensure_ascii=False,
        indent=4,
    )

    json.dump(
        meta,
        open(f"./test_data/gemba_4_{domain}_meta.json", "w", encoding="utf8"),
        ensure_ascii=False,
        indent=4,
    )


#%%
# 2. do escape html tags

# %%
# 3. upload

import src.gigametr as gm
import time

for domain in domains[:1]:
    first_model = {
        "name": f"{domain}",
        "data": f"./test_data/gemba_4_{domain}_escaped.json",
        "meta": f"./test_data/gemba_4_{domain}_meta.json",
    }

    res = gm.sbs.create(
        name=f"Gemba 4. {domain}", first=first_model, address="localhost", type="single"
        # name=f"Gemba 4. {domain}", first=first_model, address="gm.pp.ru", type="single"
    )

    print(f"\n\nhttp://gm.pp.ru/data/check/{res['id']}")
    time.sleep(1)

#["redactor", "krasota", "travel_creation", "synonims_list", "samopoznanie", "pretrain_hf"]

# http://gm.pp.ru/data/check/4c9fa7a6124c4624be9ebdacbea36450
# http://gm.pp.ru/data/check/a7dee7d534e342fd99467bd7cb92206e
# http://gm.pp.ru/data/check/195a55e57aba4e9f9f7108fb8bee215a
# http://gm.pp.ru/data/check/04404b87e85242f4ae9ee5be3c025d53
# http://gm.pp.ru/data/check/ff9abf6da37a4cfd9648e62a8a0e7f50
# http://gm.pp.ru/data/check/bbba2163b29a49bc90d6cce970a3c9a5

# %%
# http://localhost:5173/data/check/ddecfa51b13c40fc8c56e462d628b769


#%%
#download results

import src.gigametr as gm
import json
import time


domains = ["redactor", "krasota", "travel_creation", "synonims_list", "samopoznanie", "pretrain_hf"]
guids = ['4c9fa7a6124c4624be9ebdacbea36450', 'a7dee7d534e342fd99467bd7cb92206e', '195a55e57aba4e9f9f7108fb8bee215a', '04404b87e85242f4ae9ee5be3c025d53', 'ff9abf6da37a4cfd9648e62a8a0e7f50', 'bbba2163b29a49bc90d6cce970a3c9a5']

for domain, guid in zip(domains, guids):
    sbs_guid = guid

    #get comments
    comments = gm.sbs.get_comments(sbs_guid=sbs_guid, address="gm.pp.ru")
    comments_to_save = []
    # leave last comment with same 'id'
    for c in comments["data"][::-1]:
        if c["id"] not in [x["id"] for x in comments_to_save]:
            comments_to_save.append(c)
    json.dump(
        comments_to_save,
        open(f"./comments_{domain}_{sbs_guid}.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )

    #get actions
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
        open(f"./no_baza_{domain}_{sbs_guid}.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )

    time.sleep(1)

# %%
comments
# %%
