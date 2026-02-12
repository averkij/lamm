# %% 
import json
import time
from pathlib import Path

import src.gigametr as gm
from escape_tags import escape_nonvalid_html_tags


ADDRESS = "localhost" 
MODEL_NAME = "example"
META_TEMPLATE = {"source_file": "example_source"}


# %% 
def _is_nan(x: object) -> bool:
    return isinstance(x, float) and x != x


def build_data_and_meta_from_raw(
    *,
    raw_path: Path,
    data_out_path: Path,
    meta_out_path: Path,
    meta_template: dict,
) -> None:
    """
    Builds `data_out_path` + `meta_out_path` from a single `raw_path`.

    raw format: list[list[{"role": str, "content": str, "trainable": bool}]]
    data format: list[str]
    meta format: list[dict] of `meta_template`, len(meta) == len(raw)
    """
    raw_items = json.load(open(raw_path, "r", encoding="utf-8"))
    if not isinstance(raw_items, list):
        raise ValueError(f"Expected {raw_path} to contain a JSON list.")

    texts: list[str] = []
    for dialog in raw_items:
        if not isinstance(dialog, list):
            raise ValueError(
                f"Expected each item in {raw_path} to be a list of messages."
            )

        acc: list[str] = []
        for m in dialog:
            if not isinstance(m, dict):
                continue

            content = m.get("content")
            if content is None or content == "" or content == "nan" or _is_nan(content):
                continue

            role = m.get("role", "unknown")
            if "trainable" in m:
                trainable_sign = " 🟢" if m.get("trainable") else " 🔵"
            else:
                trainable_sign = ""

            acc.append(f"—{trainable_sign} [{role}] {content}")

        texts.append("\n\n".join(acc))

    meta = [dict(meta_template) for _ in range(len(raw_items))]

    json.dump(
        texts,
        open(data_out_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    json.dump(
        meta,
        open(meta_out_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


def escape_data_file(*, data_in_path: Path, data_out_path: Path) -> None:
    texts = json.load(open(data_in_path, "r", encoding="utf-8"))
    if not isinstance(texts, list) or (texts and not isinstance(texts[0], str)):
        raise ValueError(f"Expected {data_in_path} to be a JSON list of strings.")

    escaped = [escape_nonvalid_html_tags(t) for t in texts]
    json.dump(
        escaped,
        open(data_out_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


# %% 
def download_history(*, sbs_id: str, out_dir: Path, address: str) -> None:
    """Downloads comments/actions history and saves JSON files."""
    out_dir.mkdir(parents=True, exist_ok=True)

    comments = gm.sbs.get_comments(sbs_guid=sbs_id, address=address)
    actions = gm.sbs.get_actions(sbs_guid=sbs_id, address=address)

    json.dump(
        comments,
        open(out_dir / f"comments_{sbs_id}.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    json.dump(
        actions,
        open(out_dir / f"actions_{sbs_id}.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


# %% 
here = Path(__file__).resolve().parent
test_data = here / "test_data"

raw = test_data / "example_items_raw.json"

data = test_data / "example_items.json"
meta = test_data / "example_items_meta.json"
escaped_data = test_data / "example_items_escaped.json"

# 1) Preparation
build_data_and_meta_from_raw(
    raw_path=raw,
    data_out_path=data,
    meta_out_path=meta,
    meta_template=META_TEMPLATE,
)
escape_data_file(data_in_path=data, data_out_path=escaped_data)
print(f"Prepared upload files:\n- {escaped_data}\n- {meta}\n- {raw}")

#%%

# 2) Create
first_model = {
    "name": MODEL_NAME,
    "data": str(escaped_data),
    "meta": str(meta),
    "raw": str(raw),
}

res = gm.sbs.create(
    name="example_one",
    first=first_model,
    address=ADDRESS,
    type="single",
)
print(res)

sbs_id = res["id"]
print(f"\nCheck UI: http://{ADDRESS}/data/check/{sbs_id}")
time.sleep(1)

#%%

# 3) Download results: actions/comments history (may be empty if run isn't finished yet)
out_dir = here / "results"
download_history(sbs_id=sbs_id, out_dir=out_dir, address=ADDRESS)
print(f"Saved history JSONs to: {out_dir}")

# %%
