import os
import subprocess
import shutil
from colorama import Fore, init
import sys
from pathlib import Path

import modules.file_manager as manager

init(autoreset=True)

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def build_exe(main_file, app_name, gui: bool):
    try:
        base_path = Path.cwd()
        source_folder = (base_path / "YourApp" / "source").absolute()
        product_folder = (base_path / "YourApp" / "products").absolute()
        
        product_folder.mkdir(parents=True, exist_ok=True)
        source_folder.mkdir(parents=True, exist_ok=True)

        pure_file_name = os.path.basename(main_file)
        main_py_path = source_folder / pure_file_name
        
        if not main_py_path.exists():
            print(f"{Fore.RED}[ERROR] Script bulunamadı: {main_py_path}")
            return

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Packaging is starting: {product_folder / app_name}.exe")

        console_param = "--noconsole" if gui else "--console"
        
        command = [
            sys.executable, "-m", "PyInstaller",
            str(main_py_path),
            "--onefile",
            "--clean",
            console_param,
            "--name", str(app_name),
            "--distpath", str(product_folder),
            "--workpath", str(source_folder / "build"),
            "--specpath", str(source_folder)
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] EXE converted: {product_folder / app_name}.exe")
        else:
            print(f"{Fore.RED}[ERROR - {get_module_name()}] PyInstaller error: {result.stderr}")
            return

        build_dir = source_folder / "build"
        spec_file = source_folder / f"{app_name}.spec"

        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'build' removed.")

        if spec_file.exists():
            os.remove(spec_file)
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] 'spec' removed.")

    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
