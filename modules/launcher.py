import os
import subprocess
import modules.file_manager as manager
import shutil
import pip
from colorama import Fore, init

init(autoreset=True)

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def build_exe(main_file, app_name, gui: bool):
    try:
        pip.main(["install", "pyinstaller"])
        ana_dosya = main_file
        uygulama_adi = app_name
        hedef_klasor = os.path.abspath("YourApp/products")
        kaynak_klasoru = os.path.abspath("YourApp/source")

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Packaging begins: {ana_dosya}")

        if gui == True:
            command_gui = [
                "pyinstaller",
                "--onefile",
                "--clean",
                "--distpath", hedef_klasor,
                f"{app_name}.py"
            ]
            os.chdir(kaynak_klasoru)
            subprocess.run(command_gui, check=True)

        else:
            command_console = [
                "pyinstaller",
                "--onefile",
                "--clean",
                "--noconsole",
                "--distpath", hedef_klasor,
                f"{app_name}.py"
            ]
            os.chdir(kaynak_klasoru)
            subprocess.run(command_console, check=True)

        if os.path.exists("build"):
            shutil.rmtree("build")
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'build' removed.")

        spec_path = os.path.join(kaynak_klasoru, f"{uygulama_adi}.spec")
        if os.path.exists(spec_path):
            os.remove(spec_path)
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] '{uygulama_adi}.spec' removed.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
