# %%
import lamm_cli


first_model = {"name": "gpt-3.5-turbo", "data": "./test_samples_1.json"}
second_model = {"name": "giga-chat", "data": "./test_samples_2.json"}

res = lamm_cli.create_sbs(
    name="Test SBS 4",
    first=first_model,
    second=second_model,
)

# %%
res

# %%
import lamm_cli

lamm_cli.get_info("b9a14e6583b942ed9247b9200a4ca9c2")
# %%
