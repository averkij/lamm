#%%
!pip install gigametr

# %%
import gigametr as gm
from gigametr import sbs


first_model = {"name": "gpt-3.5-turbo", "data": "./test_samples_1.json"}
second_model = {"name": "giga-chat", "data": "./test_samples_2.json"}

#%%
import os


os.path.basename('./sbs/data/asd.json')

# %%

res = sbs.create(
    name="Test SBS 5", first=first_model, second=second_model, address="gm.pp.ru"
)

# %%
res
#2234059b9c62495eae4a50a888713610
#905f453134c5408b9ce235d2182d883e

#%%

sbs.info("905f453134c5408b9ce235d2182d883e", address="195.140.147.102")


# %%
import client.src.gigametr as gm


gm.get_info("b9a14e6583b942ed9247b9200a4ca9c2")

# %%


import client.src.gigametr as gm


first_model = {
    "name": "GigaChat-sft-v2.4.16.0-2k-exp",
    "data": "./GigaChat-sft-v2.4.16.0-2k-exp-k4.json",
}
second_model = {
    "name": "GigaChat-sft-v1.2.16.0-2k-altsampling",
    "data": "./GigaChat-sft-v1.2.16.0-2k-altsampling-k4_fix.json",
}

res = gm.create_sbs(
    name="Большая корзина",
    first=first_model,
    second=second_model,
)


# %%
res
# %%