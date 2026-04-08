import json
import os
from system.errorcontrol.error import er

CWD_FILE = "system/config/cwd.json"


def update_cwd(cwd):
    try:
        with open(CWD_FILE, "w") as f:
            json.dump({"cwd": cwd}, f)
    except Exception as e:
        er("failed to save cwd", e)


def load_cwd():
    try:
        if not os.path.exists(CWD_FILE):
            return ["home", "user"]  # default

        with open(CWD_FILE, "r") as f:
            data = json.load(f)

        return data.get("cwd", ["home", "user"])

    except Exception as e:
        er("failed to load cwd, resetting", e)
        return ["home", "user"]