import requests
import json
from colorama import init, Fore
import os
from tkinter import messagebox

init(autoreset=True)

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def check_version():
    url = "https://raw.githubusercontent.com/thekeops/yourapp/main/Packages/version.txt"

    response = requests.get(url)

    VERSION = response.text

    return VERSION
