import os
from deep_translator import GoogleTranslator
from google import genai
import json
from colorama import Fore, init
from tkinter import messagebox
import random

import modules.file_manager as manager
import modules.launcher as launcher

init(autoreset=True)

file_id = random.randint(100000, 999999)
folder_path = "YourApp/data/app/temp"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def translator(text: str, source="tr", target="en"):
    translated = GoogleTranslator(source, target).translate(text)
    return translated

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def prompt(app_type="Bilgisayar Uygulaması", coding_lang="Python", gui_param=False, user_input: str = "Uygulama hesap makinesi olsun.", app_title_param="hesap-makinesi", platform="Windows", ui_library="Tkinter", language="İngilizce"):
    global app_title
    global gui

    gui = bool(gui_param)

    app_title = app_title_param.replace(" ", "-").strip()

    try:
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Prompt is being preparing...")
        if gui:
            gui = f"arayüzü olsun, arayüz kütüphanesi : {ui_library}"
        else:
            gui = "arayüze sahip olmasın terminalden çalışsın"

        task_prompt_no_translated = f"Merhaba, {coding_lang.strip()} dilini kullanarak bana {platform.strip()} platformuna {app_type.strip()} geliştirebilir misin? Uygulamada {gui}, {user_input.strip()}. Uygulamanın başlığı : {app_title.strip()}, Uygulama Dili : {language.strip()}"
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] The prompt has been prepared and the translation process is starting...")
        task_prompt = translator(task_prompt_no_translated)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Prompt translated.")

        prompt = f"""ROLE: Senior Software Architect (Expert in Python).
    
OBJECTIVE:
Generate production-ready, clean, and bug-free code for the following task. Just write the code, don't say anything else. Write plain text, code without adding any markup or anything like that. Just code.
    
CONSTRAINTS & STYLE:
- ARCHITECTURE: Use functional programming. Avoid Classes unless strictly necessary.
- UI: Modern, Minimalist.
- SECURITY: For simple tasks, please don't use cryptography. Use cryptography only if you're developing applications that need to remain confidential, such as APIs.
- ERROR HANDLING: Use try-except, but don't use try-except inside the `if __name__ == "__main__"` code. Allow an error to be thrown when called with the `exec` function within a module.
- READABILITY: Follow PEP 8. Add concise comments for complex logic.

INPUT TASK:
{task_prompt}
"""
        with open(f"{folder_path}/prompt-{file_id}.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Prompt written to file.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")

def create_app():
    try:
        with open("YourApp/data/api/api.json", "r") as f:
            encrypting_api = json.load(f)
        with open("YourApp/data/key/key.json", "r") as f:
            key = json.load(f)
        with open(f"YourApp/data/app/temp/prompt-{file_id}.txt", "r") as f:
            prompt = f.read().strip()
        with open("YourApp/data/app/settings.json", "r") as f:
            settings = json.load(f)
        with open(f"YourApp/languages/{settings['language']}_lang.json", "r") as f:
            lang_text = json.load(f)

        api = manager.decrypt(encrypting_api["api-key"], key["key"])
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Api decrypted.")

        client = genai.Client(api_key=api.strip())
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Connected client.")

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Generate content starting...")
        response = client.models.generate_content(
            model=f"{settings['ai-model']}",
            contents=f"{prompt}"
        )

        with open(f"YourApp/source/{app_title}.py", "w", encoding="utf-8") as f:
            f.write(str(response.text).replace("```", ""))

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Generate content sucsessful.")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Code writed.")

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] The process of converting to an exe file is starting...")
        launcher.build_exe(main_file=f"YourApp/source/{app_title}.py", app_name=f"{app_title}", gui=gui)
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] The file has been created as an .exe .")

    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
        messagebox.showerror("YourApp", f"{lang_text['ErrMessages']['CreationFailed']}", detail=f"{e}")
