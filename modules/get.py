import os
import requests
from colorama import Fore, init

init(autoreset=True)

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def get_language_packets():
    try:
        url = f"https://api.github.com/repos/TheKeops/yourapp/contents/Packages"
        raw_link = f"https://raw.githubusercontent.com/TheKeops/yourapp/main/Packages/"
        response = requests.get(url)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Get github api.")

        if response.status_code == 200:

            data = response.json()

            for i in range(len(data)):
                name = data[i]["name"]

                check_lang_file = name.split("_")

                if check_lang_file[1] == "lang.json":

                    raw = requests.get(raw_link + name)

                    if raw.status_code == 200:
                        with open(f"YourApp/languages/{name}", "w", encoding="utf-8") as f:
                            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] {name} file has created.")
                            f.write(str(raw.text).replace("\n", ""))
                            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] {name} writed.")
                    else:
                        print(f"{Fore.RED}[ERROR - {get_module_name()}] Language pack data retrieval failed.")
                else:
                    print(f"{Fore.RED}[ERROR - {get_module_name()}] Unknown file: {name}")
        else:
            print(f"{Fore.RED}[ERROR - {get_module_name()}] Language pack data retrieval failed.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
