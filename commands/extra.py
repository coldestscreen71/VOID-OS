import time
import os
import random
import sys
import platform
import json

from system.errorcontrol.error import er

def login():
    print("Login")
    with open("system/config/user.json","r") as file:
            data = json.load(file)
    attempts = 3
    while attempts > 0 :
        name = input("Enter your name you have entered at first: ")
        password = input("Enter your password you have entered at first: ")
        if data["name"] == name and data["password"] == password:
            break
        else:
            attempts -= 1
            er("try again")
            if attempts == 0:
                print("too many tries")
                print("system is locked for 10 seconds")
                time.sleep(10)
                er("system lock expired. you can try again.")
                attempts = 3

def register():
    data ={}
    name = input("Enter name: ")
    password = input("Enter password: ")
    data["name"] = name
    data["password"] = password
    while True:
        Q = input("would you like to add any externel infromation about you? [y/n]").lower()
        if Q == "y":
            about_user = input(": ")
            data["information"] = about_user
            break
        elif Q == "n":
            break
        else:
            er("choose a option between: [y/n] ")
    with open("system/config/user.json","w") as file:
        json.dump(data,file)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def shutdown():
    print("\033[0m[SHUTING DOWN]\033[0m")
    exit()

def uni_pass():
    with open("system/config/unipass.json","r") as file:
        data = json.load(file)
        password = data["unipass"]
    while True:
        i = input("ENTER THE UNIVERSEL PASSWORD: ")
        if i == password:
            time.sleep(0.5)
            break
        else:
            clear()

def echo(*args):
    print(" ".join(args))

start_time = time.time()

def about():
    with open("system/config/version.json","r") as file:
        data = json.load(file)
        v = data["version"]
    uptime = int(time.time() - start_time)
    mins, secs = divmod(uptime, 60)
    hrs, mins = divmod(mins, 60)
    
    print("\033[32m(VOID-OS)\033[0m")
    print("Version :" ,f"{v}")
    print("Author :", " Rimon")
    print("Main purpose :" ,"")
    print()
    print("status :", "Online")
    print("Uptime   :", f"{hrs:02d}:{mins:02d}:{secs:02d}")
    print("Platform :", platform.system())
    print("Runtime :", sys.version.split()[0])

def whoami():
    try:
        with open("system/config/user.json", "r") as file:
            data = json.load(file)
            print("current user:", data["name"])
    except:
        er("no user data")
        
def booting():
    clear()
    print("welcome to")
    print(r"""  __      ______ _____ _____          ____   _____ 
 \ \    / / __ \_   _|  __ \        / __ \ / ____|
  \ \  / / |  | || | | |  | |______| |  | | (___  
   \ \/ /| |  | || | | |  | |______| |  | |\___ \ 
    \  / | |__| || |_| |__| |      | |__| |____) |
     \/   \____/_____|_____/        \____/|_____/ 
                                                  
                                                   """)
                                                   
def matrix(d):
    try:
        duration = float(d)
    except:
        er("only numbers")
        return
    width = os.get_terminal_size().columns
    chars = "01abcdefghijklmnopqrstuvwxyz@#$%&*"

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            line = "".join(
                random.choice(chars) if random.random() > 0.05 else " "
                for _ in range(width)
            )
            print("\033[32m" + line + "\033[0m")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Matrix stopped.")