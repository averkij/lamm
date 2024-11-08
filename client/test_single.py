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
