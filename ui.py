import colored
import os
import shutil   

def clear():
    os.system("cls")
    cols = shutil.get_terminal_size().columns
    print(colored.fg(9))
    print("https://discord.gg/acee".center(cols))
    print(" _____    ___    ____    ____   ".center(cols))
    print("|  _  |  / __|  | ___|  |  __|  ".center(cols))
    print("| |_| | | |     | |__   | |__   ".center(cols))
    print("|  _  | | |     |  __|  |  __|  ".center(cols))
    print("| | | | | |__   | |__   | |__   ".center(cols))
    print("|_| |_|  \___|  |____|  |____|  ".center(cols))
    print(f"                      {colored.fg(255)}".center(cols))

def log(string):
    print(f"{colored.fg(41)}[{colored.fg(255)}+{colored.fg(41)}] {string} {colored.fg(255)}")

def error(string):
    print(f"{colored.fg(9)}[{colored.fg(255)}+{colored.fg(9)}] {string} {colored.fg(255)}")

def user_info(header, string):
    print(f"{colored.fg(246)}=>{colored.fg(255)} {header} {colored.fg(246)}=>{colored.fg(255)} {string} {colored.fg(255)}")

def get_info(string):
    return input(f"{colored.fg(246)}=>{colored.fg(255)} {string} {colored.fg(255)}")