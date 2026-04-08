import os 
import json
import uuid
from system.filesystem.data import add_data, get_data, update_data, delete_data

from system.errorcontrol.error import er

def load_fs():
    try:
        with open("system/config/fs.json", "r") as f:
            data = json.load(f)
            return data.get("fs")
    except Exception as e:
        er("state corrupted, resetting data",e)
        data = {
    "/": {"type": "dir", "children": {
        "home": {"type": "dir", "children": {
          "user" : {"type": "dir", "children": {}
          }
        }},
        "bin": {"type": "dir", "children": {}},
        "etc": {"type": "dir", "children": {}},
        "var": {"type": "dir", "children": {}}
    }}
}
        with open("system/config/fs.json", "w") as f:
            json.dump({"fs": data}, f)
        return data

fs = load_fs()

def save_fs():
    with open("system/config/fs.json", "w") as f:
        json.dump({"fs": fs}, f)

cwd = ["home","user"]

def get_path():
    if not cwd:
        return "/"
    return "/" + "/".join(cwd)

def dict_info():
    current = fs.get("/")
    if not current:
        er("root missing")
        return None
    try:
        for folder in cwd:
            current = current["children"][folder]
        return current
    except KeyError:
        er("invalid path")
        return None
        
def create_file(name, file_type="file", data=""):
    current = dict_info()

    if name in current["children"]:
        er("already exists")
        return False

    loc = str(uuid.uuid4())
    size = len(data.encode()) if isinstance(data, str) else len(data)

    current["children"][name] = {
        "type": file_type,
        "size": size,
        "location": loc
    }

    add_data(loc, data)
    save_fs()
    return True
    
def read_file(name):
    current = dict_info()

    if name not in current["children"]:
        er("file not found")
        return None

    file = current["children"][name]

    if file["type"] == "dir":
        er("not a file")
        return None

    return get_data(file["location"]) 
    
def update_file(name, new_data):
    current = dict_info()

    if name not in current["children"]:
        er("file not found")
        return False

    file = current["children"][name]

    if file["type"] == "dir":
        er("not a file")
        return False

    update_data(file["location"], new_data)
    file["size"] = len(new_data.encode()) if isinstance(new_data, str) else len(new_data)

    save_fs()
    return True
    
def delete_file(name):
    current = dict_info()

    if name not in current["children"]:
        er("not found")
        return False

    file = current["children"][name]

    if file["type"] == "dir" and file["children"]:
        er("directory not empty")
        return False

    if file["type"] != "dir":
        delete_data(file["location"])

    del current["children"][name]
    save_fs()
    return True
    