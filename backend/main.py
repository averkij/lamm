"""Main module"""

import difflib
import json
import logging
import os
import re
import uuid
import requests

import config
import constants as con
import db_helper
import helper
from flask import Flask, abort, request, send_file
from flask_cors import CORS

import qrcode

helper.configure_logging()

# - /sbs/create
# - /sbs/list
# - /sbs/task/get
# - /sbs/task/vote
# - /sbs/get

# from mlflow import log_metric

app = Flask(__name__)
CORS(app)


@app.route("/sbs/create", methods=["POST"])
def sbs_create():
    """Upload data and create sbs object"""

    sbs_type = request.form.get("type", con.SBS_TYPE_DOUBLE)
    sbs_guid = uuid.uuid4().hex

    sbs_name = request.form.get("name", "SBS")
    model_name_1 = request.form.get("model_1", "model_1")

    # temp hack
    model_name_2 = request.form.get("model_1", "model_1")
    filename_1 = request.form["filename_1"]
    extra_data = request.form.get("extra_data", "{}")

    filename_meta_1 = request.form.get("filename_meta_1", None)
    filename_meta_2 = request.form.get("filename_meta_2", None)

    if sbs_type == con.SBS_TYPE_DOUBLE:
        model_name_2 = request.form.get("model_2", "model_2")
        filename_2 = request.form["filename_2"]

    upload_folder = os.path.join(con.DATA_FOLDER, sbs_guid)
    helper.check_folder(upload_folder)

    for model in request.files:
        file = request.files[model]
        filename = file.filename

        logging.info(f"Loading document {file.filename}.")
        upload_path = os.path.join(upload_folder, filename)

        file.save(upload_path)

        logging.info(f"Success. {filename} is loaded.")

    with open(
            os.path.join(upload_folder, filename_1), mode="r", encoding="utf-8"
        ) as file_1:
            items_1 = json.load(file_1) # flat list

    if filename_meta_1:
        with open(
            os.path.join(upload_folder, filename_meta_1), mode="r", encoding="utf-8"
        ) as file_meta_1:
            meta_1 = json.load(file_meta_1)
            meta_1 = [json.dumps(x, ensure_ascii=False) for x in meta_1]
    else:
        meta_1 = ["{}"] * len(items_1)

    if sbs_type == con.SBS_TYPE_SINGLE:
        # temp hack
        items_1 = [[x, "", y] for x, y in zip(items_1, meta_1)]
        items_2 = items_1
    else:
        if filename_meta_2:
            with open(
                os.path.join(upload_folder, filename_meta_2), mode="r", encoding="utf-8"
            ) as file_meta_2:
                meta_2 = json.load(file_meta_2)
                meta_2 = [json.dumps(x, ensure_ascii=False) for x in meta_2]
        else:
            meta_2 = ["{}"] * len(items_2)

        with open(
            os.path.join(upload_folder, filename_1), mode="r", encoding="utf-8"
        ) as file_1:
            with open(
                os.path.join(upload_folder, filename_2), mode="r", encoding="utf-8"
            ) as file_2:
                items_1 = json.load(file_1)
                items_1 = [[x[0], x[1], y] for x, y in zip(items_1, meta_1)]
                items_2 = json.load(file_2)
                items_2 = [[x[0], x[1], y] for x, y in zip(items_2, meta_2)]

    helper.check_data(items_1, items_2)

    db_helper.create_db(sbs_guid, sbs_name, model_name_1, model_name_2, extra_data)
    db_helper.fill_db(sbs_guid, items_1, items_2)

    img = qrcode.make(f"http://gm.pp.ru/data/check/{sbs_guid}")
    img.save(f"static/img/{sbs_guid}.png")

    return {"id": sbs_guid}


@app.route("/sbs/list", methods=["GET"])
def get_sbs_list():
    """Get list of SBS"""

    return {"ok": 1}


@app.route("/sbs/task/get/<sbs_guid>/<user_guid>/<try_id>", methods=["GET"])
def get_task(sbs_guid, user_guid, try_id):
    """Get task"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    logging.info(f"Getting task for SBS. sbs_guid: {sbs_guid}.")

    db_version = db_helper.get_version(sbs_guid)

    db_helper.ensure_user_exists(sbs_guid, user_guid)
    tasks = db_helper.get_tasks(sbs_guid, user_guid, try_id)

    res = [
        (
            x[0],
            x[1],
            x[2],
            x[3],
            x[4],
            x[5],
            x[6] if db_version >= 0.4 else '{"meta": -1}',
            x[7] if db_version >= 0.4 else '{"meta": -1}',
        )
        for x in tasks
    ]

    return {"items": res}


@app.route("/sbs/task/resolve", methods=["POST"])
def resolve_task():
    """Resolve task"""

    sbs_guid = request.form.get("sbs_guid", None)
    user_guid = request.form.get("user_guid", None)
    task_id = request.form.get("task_id", None)
    try_id = request.form.get("try_id", None)
    event_id, _ = helper.try_parse_int(request.form.get("event_id", -1))
    comment = request.form.get("comment", None)

    if not sbs_guid or not user_guid or not task_id or not event_id:
        return ("Please, provide valid parameters", 400)

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    db_helper.resolve_task(sbs_guid, user_guid, task_id, try_id, event_id, comment)

    return ("", 200)


@app.route("/sbs/info/<sbs_guid>", methods=["GET"])
def get_info(sbs_guid):
    """Get SBS state"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    data, info = db_helper.get_info(sbs_guid)
    total_tasks = len(data)
    answer_ids = [x for x in data if x[1] > 0]
    solved_tasks = len(answer_ids)
    extra_data = json.loads(info[6])

    res = {
        "model_1": info[2],
        "model_2": info[3],
        "comment": info[1],
        "create_ts": info[5],
        "total_tasks": total_tasks,
        "solved_tasks": solved_tasks,
        "extra_data": extra_data,
        "answer_ids": answer_ids,
        "state": info[4],
    }

    return res


@app.route("/sbs/stat/<sbs_guid>", methods=["GET"])
def get_stat(sbs_guid):
    """Get full SBS statistics"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    data = db_helper.get_stat(sbs_guid)
    result = {1: 0, 2: 0, 3: 0, 4: 0}
    for x in data:
        result[x[1]] += 1

    res = {"data": data, "res": result}

    return res


@app.route("/sbs/history/actions/<sbs_guid>", methods=["GET"])
def get_actions(sbs_guid):
    """Get SBS history (target actions only)"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    data = db_helper.get_history(sbs_guid, event_ids=con.ACTION_EVENTS)

    res = [
        {
            "id": x[0],
            "user_id": x[1],
            "prompt_1": x[2],
            "prompt_2": x[3],
            "model_1": x[4],
            "model_2": x[5],
            "res": helper.format_event(x[6]),
        }
        for x in data
    ]

    return {"data": res}


@app.route("/sbs/history/comments/<sbs_guid>", methods=["GET"])
def get_comments(sbs_guid):
    """Get SBS history (comments actions only)"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    db_version = db_helper.get_version(sbs_guid)
    data = db_helper.get_history(sbs_guid, event_ids=con.COMMENT_EVENTS)

    res = [
        {
            "id": x[0],
            "user_id": x[1],
            "prompt_1": x[2],
            "prompt_2": x[3],
            "model_1": x[4],
            "model_2": x[5],
            "res": helper.format_event(x[6]),
            "ts": x[7],
            "comment": x[8] if db_version >= 0.3 else None,
        }
        for x in data
    ]

    return {"data": res}


@app.route("/sbs/version/<sbs_guid>", methods=["GET"])
def get_version(sbs_guid):
    """Get SBS DB version"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    data = db_helper.get_version(sbs_guid)

    return {"version": data}


@app.route("/sbs/debug/state/set/<sbs_guid>/<state_id>", methods=["GET"])
def set_sbs_state(sbs_guid, state_id):
    """[DEBUG METHOD] Set SBS state"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    db_helper.update_sbs_state(sbs_guid, state_id)

    return ("", 200)


@app.route(
    "/sbs/debug/counter/answer/set/<sbs_guid>/<task_id>/<count>", methods=["GET"]
)
def set_answer_counter(sbs_guid, task_id, count):
    """[DEBUG METHOD] Set answer counter for task"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    db_helper.set_answer_counter(sbs_guid, task_id, count)

    return ("", 200)


@app.route("/sbs/debug/patch/<sbs_guid>", methods=["GET"])
def patch_db(sbs_guid):
    """[DEBUG METHOD] Patch SBS DB schema to the latest version"""

    if not helper.db_exists(sbs_guid):
        return ("SBS not found", 404)

    db_helper.patch_db(sbs_guid)

    return ("", 200)


@app.route("/api/spell-check", methods=["POST"])
def spell_check_text():
    """Spell check API endpoint"""
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return {"success": False, "error": "No text provided"}, 400
    
    if len(text) <= 1000:
        res = spell_check(text)
        if res.get('success'):
            # Generate HTML diff for single chunk too
            html_diff = generate_html_diff(res['origin'], res['predictions'])
            res['html_diff'] = html_diff
    else:
        res = spell_check_long_text(text)

    return res


def split_text_into_chunks(text, max_chunk_size=900):
    """
    Split a long text into chunks, trying to break at sentence boundaries.
    Uses a slightly smaller chunk size (900) to ensure we stay under the 1000 char limit.
    """
    chunks = []
    current_chunk = ""
    
    # Split text into sentences (simple approximation)
    sentences = text.replace("! ", "! SENTENCE_BREAK")\
                   .replace("? ", "? SENTENCE_BREAK")\
                   .replace(". ", ". SENTENCE_BREAK")\
                   .split("SENTENCE_BREAK")
    
    for sentence in sentences:
        # If adding this sentence would exceed the chunk size
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence
            
        # If current chunk is already too large, split it at the max_chunk_size
        while len(current_chunk) > max_chunk_size:
            chunks.append(current_chunk[:max_chunk_size].strip())
            current_chunk = current_chunk[max_chunk_size:]
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def generate_html_diff(original_text, corrected_text):
    """
    Generate HTML-formatted diff between original and corrected text
    with appropriate highlighting.
    """
    
    matcher = difflib.SequenceMatcher(None, original_text, corrected_text)
    html_diff = []
    
    for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
        if opcode == 'equal':
            html_diff.append(original_text[i1:i2])
        elif opcode == 'delete':
            deleted_text = original_text[i1:i2]
            html_diff.append(f'<span class="diff-deleted" style="background-color: #ffe6e6; text-decoration: line-through;">{deleted_text}</span>')
        elif opcode == 'insert':
            inserted_text = corrected_text[j1:j2]
            html_diff.append(f'<span class="diff-added" style="background-color: #e6ffe6;">{inserted_text}</span>')
        elif opcode == 'replace':
            deleted_text = original_text[i1:i2]
            inserted_text = corrected_text[j1:j2]
            html_diff.append(f'<span class="diff-deleted" style="background-color: #ffe6e6; text-decoration: line-through;">{deleted_text}</span>')
            html_diff.append(f'<span class="diff-added" style="background-color: #e6ffe6;">{inserted_text}</span>')

    res = "".join(html_diff)
    res = res.replace(con.SPELL_FIX, '\n\n')

    return res


def spell_check_long_text(text):
    """
    Process a long text by splitting it into chunks and combining the results.
    """
    chunks = split_text_into_chunks(text)
    logging.info(f"Splitting text into {len(chunks)} chunks for spell checking")
    
    # Process each chunk
    original_chunks = []
    corrected_chunks = []
    all_comments = []
    
    for chunk in chunks:
        result = spell_check(chunk)
        
        if not result.get('success', False):
            # If any chunk fails, return the error
            return result
        
        original_chunks.append(result.get('origin', chunk))
        corrected_chunks.append(result.get('predictions', chunk))
        all_comments.extend(result.get('comment', ['OK']))
    
    # Combine results
    original_text = ''.join(original_chunks)
    corrected_text = ''.join(corrected_chunks)
    
    # Generate HTML diff
    html_diff = generate_html_diff(original_text, corrected_text)
    
    return {
        'origin': original_text,
        'predictions': corrected_text,
        'html_diff': html_diff,
        'comment': all_comments,
        'success': True,
        'version': '1.1.3',
        'chunks_processed': len(chunks)
    }


def spell_check(text):
    """
    returns:
    {'origin': 'Carrect tixt',
     'comment': ['OK'],
     'predictions': 'Correct text',
     'success': True,
     'version': '1.1.3'}
    """
    headers = {
        "x-api-key": "924875b53cc94dad9d7ddb047b4a2703",
        "X-Workspace-Id": "1db1c352-96a2-4e9d-b53c-376fb9957da3",
        'content-Type': 'application/json'
    }
    payload = {"instances": [{"text": text}]}
    url = "https://mlspace.ai.cloud.ru/deployments/dgx2-inf-001/kfserving-1697487248/v1/models/kfserving-1697487248:predict"
    return requests.post(url, json=payload, headers=headers).json()


# Not API calls treated like static queries
@app.route("/<path:path>")
def route_frontend(path):
    """Route static requests"""
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=config.API_PORT)
