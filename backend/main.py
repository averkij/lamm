"""Main module"""

import datetime
import logging
import os
import tempfile
import uuid

import config
import constants as con
import db_helper
import helper
import json

from flask import Flask, abort, request, send_file
from flask_cors import CORS


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

    sbs_name = request.form.get("name", "SBS")
    model_name_1 = request.form.get("model_1", "model_1")
    model_name_2 = request.form.get("model_2", "model_2")
    filename_1 = request.form["filename_1"]
    filename_2 = request.form["filename_2"]

    sbs_guid = uuid.uuid4().hex

    upload_folder = os.path.join(con.DATA_FOLDER, sbs_guid)
    helper.check_folder(upload_folder)

    for model in request.files:
        file = request.files[model]
        filename = file.filename
        # direction = request.form.get("direction", "from")

        logging.info(f"Loading document {file.filename}.")
        upload_path = os.path.join(upload_folder, filename)

        # print(file)
        # print(upload_path)

        file.save(upload_path)

        logging.info(f"Success. {filename} is loaded.")

    with open(
        os.path.join(upload_folder, filename_1), mode="r", encoding="utf-8"
    ) as file_1:
        with open(
            os.path.join(upload_folder, filename_2), mode="r", encoding="utf-8"
        ) as file_2:
            items_1 = json.load(file_1)
            items_2 = json.load(file_2)

    helper.check_data(items_1, items_2)

    db_helper.create_db(sbs_guid, sbs_name, model_name_1, model_name_2)
    db_helper.fill_db(sbs_guid, items_1, items_2)

    return {"id": sbs_guid}


@app.route("/sbs/list", methods=["GET"])
def get_sbs_list():
    """Get list of SBS"""

    return {"ok": 1}


@app.route("/sbs/task/get/<sbs_guid>/<user_guid>", methods=["GET"])
def get_task(sbs_guid, user_guid):
    """Get task"""

    logging.info(f"Getting task for SBS. sbs_guid: {sbs_guid}.")

    db_helper.ensure_user_exists(sbs_guid, user_guid)
    tasks = db_helper.get_tasks(sbs_guid, user_guid)

    return {"items": tasks}


@app.route("/sbs/task/resolve", methods=["POST"])
def resolve_task():
    """Resolve task"""

    sbs_guid = request.form.get("sbs_guid", None)
    user_guid = request.form.get("user_guid", None)
    task_id = request.form.get("task_id", None)
    event_id = request.form.get("event_id", None)

    if not sbs_guid or not user_guid or not task_id or not event_id:
        return ("Please, provide valid parameters", 400)

    db_helper.resolve_task(sbs_guid, user_guid, task_id, event_id)

    return ("", 200)


@app.route("/sbs/info/<sbs_guid>", methods=["GET"])
def get_info(sbs_guid):
    """Get SBS state"""

    data, info = db_helper.get_info(sbs_guid)
    total_tasks = len(data)
    solved_tasks = len([x for x in data if x[1] > 0])

    res = {
        "model_1": info[2],
        "model_2": info[3],
        "comment": info[1],
        "create_ts": info[5],
        "total_tasks": total_tasks,
        "solved_tasks": solved_tasks,
    }

    return res


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
