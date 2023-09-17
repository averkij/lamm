# %%
import src.gigametr as gm


first_model = {"name": "gpt-3.5-turbo", "data": "./test_data/test_samples_1.json"}
second_model = {"name": "giga-chat", "data": "./test_data/test_samples_2.json"}


# %%

res = gm.sbs.create(
    name="Test SBS 5", first=first_model, second=second_model, address="localhost"
)

# %%
res

# %%

gm.sbs.info("bcf0dca9453648b4bc733eef70e13469", address="195.140.147.102")

# %%
