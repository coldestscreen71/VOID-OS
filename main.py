#(VOID-OS)
import time
import os
import random
import sys
import platform
import json
import uuid

from commands.extra import echo, about, clear, shutdown, uni_pass, register, login, whoami, booting, matrix
from media.img_to_text import img, view
from media.video_to_text import vid, play
from commands.animation import down_ani
from system.errorcontrol.error import er
from commands.terminal import terminal, run
from system.filesystem.data import add_data, get_data, update_data
from system.filesystem.file_control import save_fs, cwd, get_path, dict_info, create_file, read_file, update_file, delete_file
from system.filesystem.state import update_cwd, load_cwd
#commands(START)
#core commands(START)

def help_cmd():
    print("Available commands:")
    for c in commands:
        print("-", c)

def reboot():
    default()
    clear()
    login()
    booting()

def default():
    cwd[:] = ["home", "user"]

#commands ( START )

def edit(name):
    current = dict_info()
    
    if not current or name not in current["children"]:
        er("file not found")
        return
    
    file = current["children"][name]
    
    if file["type"] == "dir" or file["type"] == "img" or file["type"] == "vid":
        er("not a editable")
        return
    
    content = get_data(file["location"]) or ""
    
    print("---- EDITOR ----")
    print("Commands: :save , :exit")
    print("----------------")
    
    if content:
      print("\n--- existing content ---")
      print(content)
      print("------------------------\n")
    
    lines = content.split("\n") if content else []
    
    while True:
        line = input("> ")
        
        if line == ":exit":
            break
        
        if line == ":save":
            new_content = "\n".join(lines)
            update_data(file["location"], new_content)
            file["size"] = len(new_content)
            save_fs()
            print("saved")
            continue
        
        lines.append(line)

def pwd():
    print(get_path())

def mkdir(name):
    current = dict_info()

    if not current or current["type"] != "dir":
        er("not a directory")
        return

    if "/" in name or name == "":
        er("invalid name")
        return

    if name in current["children"]:
        er("already exists")
        return

    current["children"][name] = {
        "type": "dir",
        "children": {}
    }

    save_fs()

def touch(name):
    if "/" in name or name == "":
        er("invalid name")
        return
    
    file_type = "exe" if name.endswith(".exe") else "file"
    create_file(name, file_type, "")

def cat(name):
    current = dict_info()
    
    if not current or name not in current["children"]:
        er("file not found")
        return
    
    file = current["children"][name]
    
    if file["type"] == "dir":
        er("not a file")
        return
    
    if file["type"] == "img":
        er("not a file")
        return
    
    data = get_data(file["location"])
    print(data if data else "")

def cd(name):
    global cwd

    current = dict_info()

    if name == "..":
        if cwd:
            cwd.pop()
            update_cwd(cwd)
        return

    if not current:
        return

    if name in current["children"] and current["children"][name]["type"] == "dir":
        cwd.append(name)
        update_cwd(cwd)
    else:
        er("no such directory")

def ls():
    current = dict_info()

    if not current:
        return

    VIOLET = "\033[95m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    for name, item in current["children"].items():
        if item["type"] == "dir":
            print(f"{VIOLET}{name}{RESET}")
        elif item["type"] == "exe":
            print(f"{GREEN}{name}{RESET}")
        elif item["type"] == "img":
            print(f"{CYAN}{name}{RESET}")
        elif item["type"] == "vid":
            print(f"{YELLOW}{name}{RESET}")
        else:
            print(name)


def rm(name):
    delete_file(name)

def execute(name):
    current = dict_info()
    
    if not current or name not in current["children"]:
        er("file not found")
        return
    
    file = current["children"][name]
    
    if file["type"] != "exe":
        er("not executable")
        return
    
    content = get_data(file["location"])
    
    if not content:
        return
    
    lines = content.split("\n")
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        if not line or line.startswith("#"):
            continue
        
        result = run(line, commands)
        
        if not result:
            er(f"[line {i}] error",line)
            break

def write(name, *data):
    current = dict_info()
    
    if not current or current["type"] != "dir":
        er("not a directory")
        return
    
    if "/" in name or name == "":
        er("invalid name")
        return
    
    if not data:
        er("no data provided")
        return
    
    content = " ".join(data)
    
    if name not in current["children"]:
        if name.endswith(".exe"):
            er("use touch to create executable files")
            return
        touch(name)
        file = current["children"][name]

        update_data(file["location"], content)
        file["size"] = len(content)
        save_fs()
        print("created and written")
        return
    
    file = current["children"][name]
    
    if file["type"] == "dir":
        er("not a file")
        return
    
    if file["type"] == "exe":
        er("cannot write directly to executable")
        return
    
    file["size"] = len(content)
    update_data(file["location"], content)
    save_fs()

#coammands ( END )

#file system( START )
#dict

def enter_screen():
    uni_pass()
    clear()
    if os.path.exists("system/config/user.json"):
        login()
    else:
        register()
    clear()
    booting()
    
commands = {
    "write": {"func": write, "args": True},
    "rm": {"func": rm, "args": True},
    "vid": {"func": vid, "args": True},
    "play": {"func": play, "args": True},
    "view": {"func": view, "args": True},
    "img": {"func": img, "args": True},
    "execute": {"func": execute, "args": True},
    "cat": {"func": cat, "args": True},
    "cd": {"func": cd, "args": True},
    "edit": {"func": edit, "args": True},
    "pwd": {"func": pwd, "args": False},
    "ls": {"func": ls, "args": False},
    "touch": {"func": touch, "args": True},
    "mkdir": {"func": mkdir, "args": True},
    "matrix": {"func": matrix, "args": True},
    "echo": {"func": echo, "args": True},
    "whoami": {"func": whoami, "args": False},
    "about": {"func": about, "args": False},
    "clear": {"func": clear, "args": False},
    "help": {"func": help_cmd, "args": False},
    "reboot": {"func": reboot, "args": False},
    "shutdown": {"func": shutdown, "args": False}
}

def main_menu(commands):
    enter_screen()
    terminal(commands, get_path)
    
main_menu(commands)