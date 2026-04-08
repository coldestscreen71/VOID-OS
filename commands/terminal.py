import shlex
import json
import readline
import os

from system.errorcontrol.error import er

def run(command_line,commands):
    try:
        parts = shlex.split(command_line)
    except ValueError:
        er("invalid syntax")
        return False
    if not parts:
        return False
    current = commands
    for i, part in enumerate(parts):
        if part not in current:
            er("command not found",part)
            return False
        cmd = current[part]
        if "sub" in cmd and i + 1 < len(parts) and parts[i+1] in cmd["sub"]:
            current = cmd["sub"]
            continue

        if "func" in cmd:
            args = parts[i+1:]
            if cmd["args"]:
                if not args:
                    er("this command takes arguments",cmd)
                    return False
                cmd["func"](*args)
                return True
            else:
                if len(args) > 0:
                    er("this command takes 0 arguments", cmd)
                    return False
                cmd["func"]()
                return True
        er("invalid command path")
        return False
    er("incomplete command")
    return False
        
def terminal(commands, get_path):

    readline.set_history_length(100)

    with open("system/config/user.json", "r") as file:
        user = json.load(file)

    try:
        while True:
            cmd = input(f"\033[32m{user['name']}@terminal:{get_path()}$ \033[0m")

            if cmd.strip():
                last = readline.get_history_item(readline.get_current_history_length())
                if last != cmd:
                    readline.add_history(cmd)

            run(cmd, commands)

    except KeyboardInterrupt:
        print("\n[EXIT]")

