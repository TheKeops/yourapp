import os
from colorama import Fore, init
import json
from cryptography.fernet import Fernet

import modules.version_control as version

init(autoreset=True)

def create_app_files():
    try:
        os.makedirs("YourApp", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp' folder has created!")
        os.makedirs("YourApp/data", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data' folder has created!")
        os.makedirs("YourApp/data/app", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/app' folder has created!")
        os.makedirs("YourApp/data/key", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/key' folder has created!")
        os.makedirs("YourApp/data/api", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/api' folder has created!")
        os.makedirs("YourApp/data/app/temp", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/app/temp' folder has created!")
        os.makedirs("YourApp/products", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/products' folder has created!")
        os.makedirs("YourApp/languages", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/languages' folder has created!")
        os.makedirs("YourApp/source", exist_ok=True)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/source' folder has created!")

        open("YourApp/data/app/settings.json", "x", encoding="utf-8")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/app/settings.json' file has created!")
        open("YourApp/data/key/key.json", "x", encoding="utf-8")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/key/key.json' file has created!")
        open("YourApp/data/key/key-backup.json", "x", encoding="utf-8")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/key/key-backup.json' file has created!")
        open("YourApp/data/api/api-backup.json", "x", encoding="utf-8")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/api/api-backup.json' file has created!")
        open("YourApp/data/api/api.json", "x", encoding="utf-8")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'YourApp/data/api/api.json' file has created!")

        with open("YourApp/data/app/settings.json", "w", encoding="utf-8") as f:
            data = {
                "theme":"system",
                "ui_color":"blue",
                "language":"ENG",
                "ai-model":None,
                "programming-lang":"python",
                "api-key-insert":False,
                "version":f"{version.check_version()}"
            }

            json.dump(data, f, indent=4)

        with open("YourApp/data/key/key.json", "w", encoding="utf-8") as f:
            data = {
                "key":None
            }

            json.dump(data, f, indent=4)

        with open("YourApp/data/key/key-backup.json", "w", encoding="utf-8") as f:
            data = {
                "key":None
            }

            json.dump(data, f, indent=4)

        with open("YourApp/data/api/api-backup.json", "w", encoding="utf-8") as f:
            data = {
                "api-key":None
            }

            json.dump(data, f, indent=4)

        with open("YourApp/data/api/api.json", "w", encoding="utf-8") as f:
            data = {
                "api-key":None
            }

            json.dump(data, f, indent=4)

    except FileExistsError as f:
        print(f"{Fore.YELLOW}[WARNING - {get_module_name()}] {f}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")

def clear_temp_folder():
    path = "YourApp/data/app/temp"

    if os.path.exists(path):
        for i in os.listdir(path):
            result_path = path + "/" + i
            if os.path.isfile(result_path):
                os.remove(result_path)
                print(Fore.GREEN + f"[DEBUG - {get_module_name()}] '{result_path}' file removed successfully!")
    else:
        pass

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def create_key():
    return Fernet.generate_key()

def encrypt(metin, anahtar):
    f = Fernet(anahtar)
    sifreli_metin = f.encrypt(metin.encode())
    return sifreli_metin

def decrypt(sifreli_metin, anahtar):
    f = Fernet(anahtar)
    cozulmus_metin = f.decrypt(sifreli_metin).decode()
    return cozulmus_metin
