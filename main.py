import modules.ai as ai
import modules.file_manager as manager
import modules.get as get
import modules.launcher as launcher
import modules.version_control as version_control

import time
import datetime
import os
import json
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from colorama import Fore, init
import requests
import subprocess
import webbrowser

init(autoreset=True)

def download_data():
    global temp_message
    global start
    global check_repo_flag

    try:
        temp_message = ""
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] File manager is starting...")
        manager.create_app_files()

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Cleaning the application's temporary files...")
        manager.clear_temp_folder()

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Network checking...")
        try:
            requests.get("https://1.1.1.1", timeout=2, stream=True)
        except Exception as e:
            print(f"{Fore.RED}[ERROR - {get_module_name()}] No internet connection!")

            try:
                messagebox.showerror("YourApp", f"{lang_text['ErrMessages']['NotInternet']}", detail=f"{e}")
                temp_message = "[!] No Internet"
                exit(0)
            except:
                messagebox.showerror("YourApp", f"No internet connection!", detail=f"{e}")
                temp_message = "[!] No Internet"
                exit(0)

            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Application shutdown.")
            root.destroy()

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Checking the resource repository...")
        check_repo = requests.get("https://github.com/TheKeops/yourapp")

        check_repo_flag = False

        if check_repo.status_code == 200:
            check_repo_flag = False
        else:
            print(f"{Fore.YELLOW}[WARNING - {get_module_name()}] Source repository not found!")
            check_repo_flag = True
            try:
                temp_message = f"{lang_text['ErrMessages']['RepoNotFound']}"
            except:
                temp_message = "[!] Repo not found!"

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Retrieving language pack data...")
        get.get_language_packets()

        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Application is starting")

        start = datetime.datetime.now()

    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
        messagebox.showerror("YourApp", f"{e}")

def on_closing():

    if messagebox.askokcancel("Exit", f"{lang_text['AskMessages']['ExitMessage']}"):
        end = datetime.datetime.now()
        manager.clear_temp_folder()
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Temporary files are being deleted....")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Application shutdown.")
        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] {end-start} spend time.")
        root.destroy()

def upload_screen():
    splash_root = ctk.CTkToplevel(root)
    splash_root.geometry("300x200")
    splash_root.overrideredirect(True)
    splash_root.attributes("-topmost", True)

    x = splash_root.winfo_screenwidth() // 2 - 150
    y = splash_root.winfo_screenheight() // 2 - 100

    splash_root.geometry(f"+{x}+{y}")

    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    loading_text = ctk.CTkLabel(splash_root, text=f"", font=ctk.CTkFont(size=80))
    loading_text.place(x=120,y=40)

    loading_text_label = ctk.CTkLabel(splash_root, text=f"{lang_text['GlobalText']['loading']}", font=ctk.CTkFont(size=18, weight="bold"))
    loading_text_label.pack(pady=70)
    loading_text_label.place(y=130, relx=0.5, anchor="center")

    for i in range(2):
        for k in spinner_chars:
            loading_text.configure(text=f"{k}")
            splash_root.update()
            time.sleep(0.1)
    
    splash_root.destroy()

def get_module_name():
    file_name = os.path.basename(__file__)
    name_without_ext = os.path.splitext(file_name)[0]
    return name_without_ext.replace("_", " ").upper()

def main():
    global root
    global settings
    global lang_text

    try:
        with open("YourApp/data/app/settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)

        with open(f"YourApp/languages/{settings['language']}_lang.json", "r", encoding="utf-8") as f:
            lang_text = json.load(f)

        ctk.set_appearance_mode(f"{settings['theme']}")
        ctk.set_default_color_theme(f"{settings['ui_color']}")
        ctk.set_widget_scaling(1.0)

        def loading_screen():
            for i in root.winfo_children():
                i.destroy()

            loading = ctk.CTkLabel(root, text=f"{lang_text['GlobalText']['loading_screen']}", font=ctk.CTkFont(size=50, weight="bold"))
            loading.place(relx=0.5, rely=0.4, anchor="center")

            loading_sub = ctk.CTkLabel(root, text=f"{lang_text['GlobalText']['loading_screen_subtitle']}", font=ctk.CTkFont(size=30))
            loading_sub.place(relx=0.5, rely=0.5, anchor="center")

        def settings_page():

            def submit_settings():
                settings["theme"] = theme.get().lower().strip()
                settings["ui_color"] = ui_color.get().lower().strip()
                settings["language"] = language.get().upper().strip()
                settings["ai-model"] = ai_model.get().lower().strip()

                if str(settings["ai-model"]).strip() == "":
                    settings["ai-model"] = None
                
                if api_key.get().strip() == "":
                    settings["api-key-insert"] = False
                else:
                    settings["api-key-insert"] = True
                
                val_api = api_key.get().strip()

                generated_key = manager.create_key()
                print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] new key created")

                dump_text_key = {"key":generated_key.decode("utf-8")}

                with open("YourApp/data/key/key.json", "w", encoding="utf-8") as f:
                    json.dump(dump_text_key, f, indent=4)
                with open("YourApp/data/key/key-backup.json", "w", encoding="utf-8") as f:
                    json.dump(dump_text_key, f, indent=4)

                encrypted_api = manager.encrypt(val_api, generated_key)
                print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Api encrypted")

                dump_text = {"api-key":encrypted_api.decode("utf-8")}

                with open("YourApp/data/api/api.json", "w", encoding="utf-8") as f:
                    
                    json.dump(dump_text, f, indent=4)
                with open("YourApp/data/api/api-backup.json", "w", encoding="utf-8") as f:
                    json.dump(dump_text, f, indent=4)

                with open("YourApp/data/app/settings.json", "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=4)

                print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Settings saved.")
                ctk.set_appearance_mode(f"{settings['theme']}")
                ctk.set_default_color_theme(f"{settings['ui_color']}")

                main_page()
                settings_page()
                print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Settings applied.")

                messagebox.showinfo("YourApp", f"{lang_text['InfoMessages']['SettingsSaved']}")

            def open_ai_google():
                webbrowser.open("https://aistudio.google.com")

            with open("YourApp/data/api/api.json", "r", encoding="utf-8") as f:
                api = json.load(f)

            with open("YourApp/data/key/key.json", "r", encoding="utf-8") as f:
                key = json.load(f)

            for i in root.winfo_children():
                i.destroy()

            root.title(f"YourApp | {lang_text['SettingsPage']['window_title']}")

            title = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['title']}", font=ctk.CTkFont(size=40, weight="bold"))
            title.pack(pady=20)

            back = ctk.CTkButton(root, text="⭠", font=ctk.CTkFont(size=20, weight="bold"), width=30, command=main_page)
            back.place(x=10, y=30)

            theme_title = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['theme_label']}", font=ctk.CTkFont(size=25))
            theme_title.place(x=100, y=120)

            theme = ctk.CTkComboBox(root, values=["system", "dark", "light"], font=ctk.CTkFont(size=20), width=200, justify="center")
            theme.place(x=50, y=160)
            theme.set(settings["theme"])

            ui_color_label = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['color_theme_label']}", font=ctk.CTkFont(size=25))
            ui_color_label.place(x=70, y=220)

            ui_color = ctk.CTkComboBox(root, values=["blue", "green"], font=ctk.CTkFont(size=20), width=200, justify="center")
            ui_color.place(x=50, y=260)
            ui_color.set(settings["ui_color"])

            languages_label = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['language_label']}", font=ctk.CTkFont(size=25))
            languages_label.place(x=90, y=320)

            values = []

            for i in os.listdir("YourApp/languages"):
                file_first = i.split(".")[0]
                lang_file = file_first.split("_")[0]
                values.append(lang_file)

            language = ctk.CTkComboBox(root, values=values, font=ctk.CTkFont(size=20), width=200, justify="center")
            language.place(x=50, y=360)
            language.set(settings["language"])

            programming_lang_label = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['coding_lang_label']}", font=ctk.CTkFont(size=25))
            programming_lang_label.place(x=80, y=420)

            programming_lang = ctk.CTkComboBox(root, values=["Python"], font=ctk.CTkFont(size=20), width=200, justify="center")
            programming_lang.place(x=50, y=460)
            programming_lang.set(settings["programming-lang"])
            programming_lang.configure(state="disabled")

            api_key_label = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['api_key_label']}", font=ctk.CTkFont(size=25))
            api_key_label.place(x=800, y=120)

            api_key = ctk.CTkEntry(root, placeholder_text=f"{lang_text['SettingsPage']['placeholder_api']}", font=ctk.CTkFont(size=23), width=250, corner_radius=30)
            api_key.place(x=720, y=160)

            if settings['api-key-insert'] == True:
                api_key_encrypted = manager.decrypt(api['api-key'], key['key'])
                api_key.insert(tk.END, f"{api_key_encrypted}")
            else:
                pass

            get_api_key = ctk.CTkButton(root, text=f"{lang_text['SettingsPage']['GetApiKey']}", font=ctk.CTkFont(size=20), width=200, corner_radius=30, command=open_ai_google)
            get_api_key.place(x=750, y=220)

            ai_model_label = ctk.CTkLabel(root, text=f"{lang_text['SettingsPage']['ai_model_label']}", font=ctk.CTkFont(size=25))
            ai_model_label.place(x=800, y=280)

            ai_model = ctk.CTkEntry(root, placeholder_text=f"{lang_text['SettingsPage']['placeholder_aimodel']}", font=ctk.CTkFont(size=23), width=250, corner_radius=30)
            ai_model.place(x=720, y=320)

            if settings['ai-model'] != None or str(settings['ai-model']).strip() != "":
                ai_model.insert(tk.END, f"{settings['ai-model']}")
            else:
                ai_model.configure(placeholder_text=f"{lang_text['SettingsPage']['placeholder_aimodel']}")

            submit = ctk.CTkButton(root, text=f"{lang_text['SettingsPage']['submit_button']}", width=250, font=ctk.CTkFont(size=22), corner_radius=30, command=submit_settings)
            submit.place(x=370, y=600)

            version = ctk.CTkLabel(root, text=f"2026 Keops Studios | YourApp {settings['version']}", font=ctk.CTkFont(size=15), text_color="#757575")
            version.place(x=390, y=660)

        def how_to_use_page():
            for i in root.winfo_children():
                i.destroy()

            root.title(f"YourApp | {lang_text['AboutPage']['window_title']}")

            title = ctk.CTkLabel(root, text=f"{lang_text['AboutPage']['title']}", font=ctk.CTkFont(size=40, weight="bold"))
            title.pack(pady=20)

            back = ctk.CTkButton(root, text="⭠", font=ctk.CTkFont(size=20, weight="bold"), width=30, command=main_page)
            back.place(x=10, y=30)
                
            about_text = ctk.CTkTextbox(root, height=530, width=750, font=("consolas", 20))
            about_text.pack(pady=20)
            about_text.configure(state="normal")
            about_text.delete("1.0", tk.END)
            about_text.insert(tk.END, lang_text['AboutPage']['about_text'])

            about_text.insert(tk.END, "https://github.com/thekeops/yourapp\n", "link")
            about_text.insert(tk.END, "https://github.com/thekeops\n", "link")
            about_text.insert(tk.END, "https://linktr.ee/thekeops\n\n", "link")
            about_text.insert(tk.END, f"YourApp {settings['version']}", "red_text")

            about_text.tag_config("link", foreground="#246DFF", underline=True)
            about_text.tag_config("red_text", foreground="#FF3737")
            about_text.configure(state="disabled")

            version = ctk.CTkLabel(root, text=f"2026 Keops Studios | YourApp {settings['version']}", font=ctk.CTkFont(size=15), text_color="#757575")
            version.place(x=390, y=660)

        def main_page():
            def reload_list():
                loading_text.configure(text="Loading Products...")
                root.update()
                products_list.delete(0, tk.END)
                root.update()
                for i in os.listdir("YourApp/products"):
                    products_list.insert(tk.END, i)
                    root.update()
                    time.sleep(0.1)
                loading_text.configure(text="")
                root.update()

            def delete_app():
                ask = messagebox.askyesno("YourApp", f"{lang_text['AskMessages']['DeleteMessage']}")
                
                if ask:
                    exe_path = f"YourApp/products/{name_app}"
                    source_path = f"YourApp/source/{str(name_app).replace('.exe', '.py')}"
                    
                    if os.path.exists(exe_path):
                        os.remove(exe_path)
                        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] {exe_path} deleted!")
                        
                    if os.path.exists(source_path):
                        os.remove(source_path)
                        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] {source_path} deleted!")

                    products_list.delete(0, tk.END)
                    for i in os.listdir("YourApp/products"):
                        products_list.insert(tk.END, i)

            def selected_products(event):
                global name_app
                global indexs

                name_app = None

                index = products_list.curselection()

                if index:
                    indexs = index[0]
                    name_app = products_list.get(indexs)

                    start_my_app_button.configure(state="normal")
                    delete_app_button.configure(state="normal")
                else:
                    start_my_app_button.configure(state="disabled")
                    delete_app_button.configure(state="normal")

            def launch_app():
                try:
                    if not name_app:
                        print(f"{Fore.RED}[ERROR - {get_module_name()}] Please choose an app!")
                        messagebox.showerror("YourApp", f"{lang_text['ErrMessages']['ChooseApp']}")
                        return
                    else:
                        loading_progress = ctk.CTkProgressBar(root, width=710, height=7, corner_radius=10,progress_color="#FF6600",fg_color="#555555")
                        loading_progress.place(x=280,y=685)
                        loading_progress.set(0)
                        root.update()

                        exe_path = f"YourApp/products/{name_app}"

                        for i in range(1, 16):
                            loading_progress.set(i / 15)
                            root.update()
                            time.sleep(0.05)

                        subprocess.Popen([exe_path], shell=False)
                        loading_progress.destroy()
                        root.update()
                        print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] {name_app} opening...")
                except Exception as e:
                    print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
                    
            for i in root.winfo_children():
                i.destroy()
            
            root.update()
            root.title(f"YourApp | {lang_text['MainPage']['window_title']}")

            sidemenu_canvas = ctk.CTkFrame(root, width=int(round(260)), height=int(round(750)), fg_color="#333333", corner_radius=0)
            sidemenu_canvas.pack(side="left", fill="y")
            sidemenu_canvas.pack_propagate(False)

            title = ctk.CTkLabel(root, text=f"{lang_text['MainPage']['title']}", font=("Century Gotcih", 32, "bold"), bg_color="#333333")
            title.place(x=60, y=10)

            subtitle = ctk.CTkLabel(root, text=f"{lang_text['MainPage']['subtitle']}", font=("Century Gotcih", 20), bg_color="#333333")
            subtitle.place(x=30, y=50)

            create_app_button = ctk.CTkButton(root, text=f"{lang_text['MainPage']['create_button']}", font=("century gothic", 22, "bold"), corner_radius=30, bg_color="#333333", fg_color="green", hover_color="#005306", width=210, cursor="hand2", command=create_app_page)
            create_app_button.place(x=25, y=200)

            settings_button = ctk.CTkButton(root, text=f"{lang_text['MainPage']['settings_button']}", font=("century gothic", 22, "bold"), corner_radius=30, bg_color="#333333", fg_color="#404040", hover_color="#292929", width=210, cursor="hand2", command=settings_page)
            settings_button.place(x=25, y=250)

            about_button = ctk.CTkButton(root, text=f"{lang_text['MainPage']['about_button']}", font=("century gothic", 22, "bold"), corner_radius=30, bg_color="#333333", fg_color="#FFA600", hover_color="#BA7900", width=210, cursor="hand2", command=how_to_use_page)
            about_button.place(x=25, y=300)

            start_my_app_button = ctk.CTkButton(root, text=f"{lang_text['MainPage']['launch_app_button']}", font=("century gothic", 22, "bold"), corner_radius=30, bg_color="#333333", fg_color="#0044FF", hover_color="#002A9E", width=210, cursor="hand2", command=launch_app)
            start_my_app_button.place(x=25, y=350)
            start_my_app_button.configure(state="disabled")

            delete_app_button = ctk.CTkButton(root, text=f"{lang_text['MainPage']['delete_app_button']}", font=("century gothic", 22, "bold"), corner_radius=30, bg_color="#333333", fg_color="red", hover_color="#7F0000", width=210, cursor="hand2", command=delete_app)
            delete_app_button.place(x=25, y=400)
            delete_app_button.configure(state="disabled")

            products_list = tk.Listbox(root, width=40, height=19, font=("century gothic", 20, "bold"), activestyle="none", justify="center", foreground="white", background="#212121", borderwidth=0, border=0, selectbackground="orange")
            products_list.place(x=330, y=40)
            products_list.bind("<<ListboxSelect>>", selected_products)

            loading_text = ctk.CTkLabel(root, text="Loading Products...", font=ctk.CTkFont(size=15))
            loading_text.place(relx=0.65, rely=0.03, anchor="center")

            root.after(2000, reload_list)

            message = ctk.CTkLabel(root, text=f"{temp_message}", font=("consolas", 15), bg_color="#333333", text_color="#FFCA29")
            message.place(x=10, y=640)

            version = ctk.CTkLabel(root, text=f"2026 Keops Studios | YourApp {settings['version']}", font=ctk.CTkFont(size=15), bg_color="#333333", text_color="#757575")
            version.place(x=10, y=670)

            if settings["theme"] == "light":
                products_list.config(foreground="black", background="#DEDEDE")
                sidemenu_canvas.configure(fg_color="#E0E0E0")
                title.configure(bg_color="#E0E0E0")
                subtitle.configure(bg_color="#E0E0E0")
                version.configure(bg_color="#E0E0E0")
                create_app_button.configure(bg_color="#E0E0E0")
                about_button.configure(bg_color="#E0E0E0")
                settings_button.configure(bg_color="#E0E0E0")
                start_my_app_button.configure(bg_color="#E0E0E0")
                delete_app_button.configure(bg_color="#E0E0E0")
                message.configure(bg_color="#E0E0E0", text_color="#FF9F29")
            else:
                pass

        def create_app_page():
            def create_app_functions():
                type = app_type.get().strip().lower()
                title = app_title.get().strip()
                os = platform.get().strip()
                ui = ui_library.get().strip()
                lang = language.get().strip()
                user_input = user_input_text.get("1.0", tk.END)
                gui = 0

                if gui_switch.get() == 1:
                    gui = 1
                else:
                    gui = 0

                if title == "" or user_input == "":
                    messagebox.showerror("YourApp", f"{lang_text['ErrMessages']['BlankError']}")
                    print(f"{Fore.RED}[ERROR - {get_module_name()}] Entries are empty.")
                else:
                    try:
                        loading_screen()
                        try:
                            root.update()
                            ai.prompt(app_type=type, app_title_param=title, gui_param=gui, 
                                    user_input=user_input, platform=os, ui_library=ui, language=lang)
                            root.update()
                            ai.create_app()
                            root.update()
                            messagebox.showinfo("YourApp",f"{lang_text['InfoMessages']['RestartApp']}")
                            root.destroy()

                        except Exception as inner_e:
                            print(f"{Fore.RED}[ERROR - {get_module_name()}] {inner_e}")
                            root.update()
                            messagebox.showinfo(f"YourApp", f"{lang_text['InfoMessages']['RestartApp']}")
                            root.destroy()

                    except Exception as e:
                        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
                        messagebox.showerror("YourApp", f"{e}")
                        main_page()

            if settings["api-key-insert"] == False or settings["ai-model"] == None:
                messagebox.showwarning("YourApp", f"{lang_text['WarningMessages']['ApiNotFound']}")
            else:
                for i in root.winfo_children():
                    i.destroy()

                root.title(f"YourApp | {lang_text['CreateAppPage']['window_title']}")

                title = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['title']}", font=ctk.CTkFont(size=40, weight="bold"))
                title.pack(pady=20)

                back = ctk.CTkButton(root, text="⭠", font=ctk.CTkFont(size=20, weight="bold"), width=30, command=main_page)
                back.place(x=10, y=30)

                app_type_label = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['app_type_label']}", font=ctk.CTkFont(size=22))
                app_type_label.place(x=100,y=100)

                app_type = ctk.CTkComboBox(root, width=200, values=["Computer Program"] ,font=ctk.CTkFont(size=22))
                app_type.place(x=50,y=140)

                app_title_label = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['app_title_label']}", font=ctk.CTkFont(size=22))
                app_title_label.place(x=100,y=200)

                app_title = ctk.CTkEntry(root, placeholder_text=f"{lang_text['CreateAppPage']['app_title_label']}", width=200, font=ctk.CTkFont(size=22))
                app_title.place(x=50,y=240)
                app_title.insert(tk.END, "My app")

                platform_label = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['platform_label']}", font=ctk.CTkFont(size=22))
                platform_label.place(x=100,y=300)

                platform = ctk.CTkComboBox(root, width=200, values=["Windows", "MacOS", "Linux"] ,font=ctk.CTkFont(size=22))
                platform.place(x=50,y=340)

                ui_library_label = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['ui_library_label']}", font=ctk.CTkFont(size=22))
                ui_library_label.place(x=100,y=400)

                ui_library = ctk.CTkComboBox(root, width=200, values=["Tkinter", "Customtkinter"], font=ctk.CTkFont(size=22))
                ui_library.place(x=50, y=440)

                language_label = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['language_label']}", font=ctk.CTkFont(size=22))
                language_label.place(x=450,y=100,)

                values = []

                for i in os.listdir("YourApp/languages"):
                    file_first = i.split(".")[0]
                    lang_file = file_first.split("_")[0]
                    values.append(lang_file)

                language = ctk.CTkComboBox(root, width=200, values=values ,font=ctk.CTkFont(size=22))
                language.place(x=400,y=140)
                language.set(settings["language"])

                gui_switch = ctk.CTkSwitch(root, text=f"{lang_text['CreateAppPage']['gui_switch']}", font=ctk.CTkFont(size=24, weight="bold"), variable=ctk.BooleanVar(value=0))
                gui_switch.place(x=450, y=200)

                user_input_label = ctk.CTkLabel(root, text=f"{lang_text['CreateAppPage']['user_input_label']}", font=ctk.CTkFont(size=22))
                user_input_label.place(x=450, y=260)

                user_input_text = ctk.CTkTextbox(root, height=280, width=320, font=("consolas", 18))
                user_input_text.place(x=350, y=300)

                information_text = ctk.CTkTextbox(root, height=480, width=260, font=("consolas", 21))
                information_text.place(x=700, y=100)
                information_text.configure(state="normal")
                information_text.delete("1.0", tk.END)
                information_text.insert(tk.END, lang_text["CreateAppPage"]["information_text"])
                information_text.configure(state="disabled")

                create_app_button = ctk.CTkButton(root, text=f"{lang_text['CreateAppPage']['create_app_button']}", width=250, font=ctk.CTkFont(size=20), corner_radius=30, command=create_app_functions)
                create_app_button.place(x=380, y=600)

                version = ctk.CTkLabel(root, text=f"2026 Keops Studios | YourApp {settings['version']}", font=ctk.CTkFont(size=15), text_color="#757575")
                version.place(x=390, y=660)

        root = ctk.CTk()
        root.title(f"YourApp | {lang_text['MainPage']['window_title']}")
        root.geometry("1000x700")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        root.attributes("-topmost", False)
        root.focus()
        root.protocol("WM_DELETE_WINDOW", on_closing)

        if str(settings["version"]).strip().lower() == version_control.check_version().strip().lower():
            print(f"{Fore.GREEN}[DEBUG - {get_module_name()}] Version up to date.")
            temp_message = ""
        else:
            print(f"{Fore.YELLOW}[WARNING - {get_module_name()}] The version is out of date!")
            messagebox.showwarning("YourApp", f"YourApp version {version_control.check_version().strip().lower()} has been released! Updating is recommended.")
            temp_message = "[!] Update Available"
            
        upload_screen()

        x = root.winfo_screenwidth() // 2 - 500
        y = root.winfo_screenheight() // 2 - 350

        root.geometry(f"+{x}+{y}")

        main_page()

        root.mainloop()
    except Exception as e:
        print(f"{Fore.RED}[ERROR - {get_module_name()}] {e}")
        messagebox.showerror("YourApp", f"{e}")

if __name__ == "__main__":
    download_data()
    main()
