import logging
import os
import pathlib
import json
from warnings import simplefilter
import constants as con
import sys
import datetime
import re


def format_event(event_id):
    """Format event"""
    if event_id == con.EVENT_GET:
        return "get"
    elif event_id == con.EVENT_MODEL_1_BETTER:
        return "first_better"
    elif event_id == con.EVENT_MODEL_2_BETTER:
        return "second_better"
    elif event_id == con.EVENT_BOTH_GOOD:
        return "both_good"
    elif event_id == con.EVENT_BOTH_BAD:
        return "both_bad"
    elif event_id == con.EVENT_COMMENT_BAD_PROMPT:
        return "bad_prompt"
    elif event_id == con.EVENT_COMMENT_OTHER:
        return "other_comment"


def check_folder(folder):
    """Check if folder exists"""
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)


def create_folders(hash):
    """Create folders for a new user"""
    if hash:
        pathlib.Path(os.path.join(con.DATA_FOLDER, hash)).mkdir(
            parents=True, exist_ok=True
        )


def db_exists(sbs_guid):
    """Check if DB exists"""
    path = get_sbs_path(sbs_guid)
    if os.path.isfile(path):
        return True
    return False


def get_curr_time():
    """Get formatted time"""
    return datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")


def get_sbs_path(guid):
    """Get SBS DB path"""
    return os.path.join(con.DATA_FOLDER, guid, f"{guid}.db")


def check_data(items_1, items_2):
    """Check SBS data"""
    assert len(items_1) == len(items_2)

    # TODO add additional data


def try_parse_int(value):
    """Try parse int"""
    try:
        return int(value), True
    except ValueError:
        return value, False


def parse_json_array(json_str):
    """Parse JSON string array"""
    if not json_str:
        return []
    try:
        return json.loads(json_str)
    except:
        return []


def format_message(messages, field_name="content"):
    """Format message"""
    acc = []
    for m in messages:
        if field_name not in m:
            continue
        if m[field_name] is None or m[field_name] == "" or m[field_name] == "nan" or (isinstance(m[field_name], float) and m[field_name] != m[field_name]):
            continue
        if "trainable" in m:
            traniable_sign = " 🟢" if m["trainable"] else " 🔵"
        else:
            traniable_sign = ""
        acc.append(f"—{traniable_sign} [{m['role']}] {m[field_name]}")
    text = "\n\n".join(acc)
    return text


def get_corrected(task, db_version):
    """Get corrected messages"""
    if db_version >= 0.5:
        meta = json.loads(task[6])
        return format_message(meta["raw"], "content_corrected")
    else:
        return None


def get_html_diff(task, db_version):
    """Get html diff"""
    if db_version >= 0.5:
        meta = json.loads(task[6])
        html_diff = format_message(meta["raw"], "spell_check_html_diff")

        # dirty hacks
        
        html_diff = html_diff.replace('<span class="diff-deleted">\n</span><span class="diff-added"> </span>', '\n')
        html_diff = html_diff.replace('<span class="diff-deleted">\n\n</span><span class="diff-added"> </span>', '\n\n')
        html_diff = html_diff.replace('<span class="diff-deleted">:\n\n</span><span class="diff-added">. </span>', '.\n')

        html_diff = re.sub(r'<span class="diff-deleted">(\n+)</span>', r'\1', html_diff, flags=re.DOTALL)

        return html_diff
    else:
        return None
    

def get_corrected_from_diff(task, db_version):
    """Get corrected from diff"""
    if db_version >= 0.5:
        html_diff = get_html_diff(task, db_version)
        if not html_diff:
            return None

        print('***', html_diff)

        # delete <span class="diff-deleted"> and inside text, consider linebreaks
        html_diff = re.sub(r'<span class="diff-deleted">(.*?)</span>', '', html_diff, flags=re.DOTALL)

        #delete <span class="diff-added"> and leave inside text, consider linebreaks
        html_diff = re.sub(r'<span class="diff-added">(.*?)</span>', r'\1', html_diff, flags=re.DOTALL)
        return html_diff
    else:
        return None
    

def configure_logging(level=logging.INFO):
    """ "Configure logging module"""
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    simplefilter(action="ignore", category=FutureWarning)
    # logging.basicConfig(level=level, filename='app.log', filemode='a', format='%(asctime)s [%(levelname)s] - %(process)d: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        filemode="a",
        format="%(asctime)s [%(levelname)s] - %(process)d: %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.getLogger("matplotlib.font_manager").disabled = True


def lazy_property(func):
    """ "Lazy initialization attribute"""
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property
