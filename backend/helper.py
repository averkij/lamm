import logging
import os
import pathlib
import json
from warnings import simplefilter
import constants as con
import sys


def check_folder(folder):
    """Check if folder exists"""
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)


def create_folders(hash):
    """Create folders for a new user"""
    if hash:
        pathlib.Path(os.path.join(con.DATA_FOLDER, hash)).mkdir(
            parents=True, exist_ok=True
        )


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
