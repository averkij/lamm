# %%
import lamm_cli


first_model = {"name": "gpt-3.5-turbo", "data": "./test_samples_1.json"}
second_model = {"name": "giga-chat", "data": "./test_samples_2.json"}

res = lamm_cli.create_sbs(
    name="Test SBS 1",
    first=first_model,
    second=second_model,
)

# %%
res

# %%
