import os
import json
import subprocess
import winreg

APP_FILE = "apps.json"

def load_apps():
    if not os.path.exists(APP_FILE):
        return {}
    with open(APP_FILE, "r") as f:
        return json.load(f)

def save_apps(apps):
    with open(APP_FILE, "w") as f:
        json.dump(apps, f, indent=4)

def open_app(app_name, speak):
    apps = load_apps()
    app_name = app_name.lower()

    # Already saved?
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}")
        return True

    # Try auto-detect
    detected_path = auto_detect_app(app_name)
    if detected_path:
        remember_app(app_name, detected_path, speak)
        subprocess.Popen(detected_path)
        speak(f"Opening {app_name}")
        return True

    # Still not found → ask user to type once
    speak(f"Sorry, I couldn’t find {app_name}. Please type the path once so I can remember it.")
    app_path = input(f"Enter full path for {app_name}.exe: ").strip()

       #Normalize path so you can paste directly from Explorer
    app_path = os.path.normpath(app_path.strip('"'))

    if os.path.exists(app_path):
        remember_app(app_name, app_path, speak)
        subprocess.Popen(app_path)
        speak(f"Opening {app_name}")
        return True

    speak("That path doesn’t exist. Try again later.")
    return False

def remember_app(app_name, app_path, speak=None):
    apps = load_apps()
    apps[app_name.lower()] = app_path
    save_apps(apps)
    if speak:
        speak(f"Got it! I’ll remember {app_name} for next time.")

def list_apps():
    return list(load_apps().keys())

def auto_detect_app(app_name):
    app_name = app_name.lower()
    common_paths = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expanduser(r"~\AppData\Local"),
        os.path.expanduser(r"~\AppData\Roaming")
    ]

    # Search common folders
    for base in common_paths:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower().startswith(app_name) and file.endswith(".exe"):
                    return os.path.join(root, file)

    # Search registry uninstall keys
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey) as sk:
                    try:
                        display_name = winreg.QueryValueEx(sk, "DisplayName")[0].lower()
                        install_loc = winreg.QueryValueEx(sk, "InstallLocation")[0]
                        if app_name in display_name and install_loc:
                            exe_path = find_exe_in_folder(install_loc, app_name)
                            if exe_path:
                                return exe_path
                    except FileNotFoundError:
                        pass
    except Exception:
        pass

    return None

def find_exe_in_folder(folder, app_name):
    if not os.path.exists(folder):
        return None
    for root, dirs, files in os.walk(folder):
        for file in files:
            if app_name in file.lower() and file.endswith(".exe"):
                return os.path.join(root, file)
    return None
