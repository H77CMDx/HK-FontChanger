import tkinter as tk
from tkinter import ttk, messagebox, font
import winreg
import ctypes
import sys
from pathlib import Path

ICON_FILE = "HK Font Changer.ico"
DEFAULT_FONT = "Segoe UI"
DEFAULT_FONT_OPTION = "Default (Segoe UI)"
SEGOE_UI_REGISTRY_VALUES = {
    "Segoe UI (TrueType)": "segoeui.ttf",
    "Segoe UI Bold (TrueType)": "segoeuib.ttf",
    "Segoe UI Italic (TrueType)": "segoeuii.ttf",
    "Segoe UI Bold Italic (TrueType)": "segoeuiz.ttf",
}

def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / relative_path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Auto-elevate to Administrator on startup
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
    sys.exit()

def apply_font(selected_font):
    if selected_font == DEFAULT_FONT_OPTION:
        restore_default()
        return

    try:
        path1 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path1, 0, winreg.KEY_WRITE) as key:
            for registry_name in SEGOE_UI_REGISTRY_VALUES:
                winreg.SetValueEx(key, registry_name, 0, winreg.REG_SZ, "")
        
        path2 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path2, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, selected_font)
            
        messagebox.showinfo("Success", f"System font set to '{selected_font}'.\nReboot to apply.")
    except Exception as e:
        messagebox.showerror("Registry Error", str(e))

def restore_default():
    try:
        path1 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path1, 0, winreg.KEY_WRITE) as key:
            for registry_name, font_file in SEGOE_UI_REGISTRY_VALUES.items():
                winreg.SetValueEx(key, registry_name, 0, winreg.REG_SZ, font_file)
                
        path2 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path2, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, DEFAULT_FONT)

        font_var.set(DEFAULT_FONT_OPTION)
            
        messagebox.showinfo("Success", "Default font restored.\nReboot to apply.")
    except Exception as e:
        messagebox.showerror("Registry Error", str(e))

def update_preview(*args):
    selected_font = DEFAULT_FONT if font_var.get() == DEFAULT_FONT_OPTION else font_var.get()
    preview_label.config(font=(selected_font, 14))

# UI Setup
root = tk.Tk()
root.title("System Font Changer")
root.geometry("400x250")
root.resizable(False, False)
try:
    root.iconbitmap(str(resource_path(ICON_FILE)))
except tk.TclError:
    pass

font_var = tk.StringVar(value=DEFAULT_FONT_OPTION)
font_var.trace_add("write", update_preview)

ttk.Label(root, text="Select System Font:", font=("Segoe UI", 10)).pack(pady=(20, 5))
font_options = [DEFAULT_FONT_OPTION] + sorted(f for f in font.families() if f != DEFAULT_FONT_OPTION)
ttk.Combobox(root, textvariable=font_var, values=font_options, state="readonly", width=30).pack()

preview_label = ttk.Label(root, text="Preview Text (AaBbCcYyZz 123)", font=("Segoe UI", 14))
preview_label.pack(pady=20)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Apply Font", command=lambda: apply_font(font_var.get()), width=15).pack(side=tk.LEFT, padx=10)
ttk.Button(btn_frame, text="Reset Default", command=restore_default, width=15).pack(side=tk.LEFT, padx=10)

root.mainloop()
