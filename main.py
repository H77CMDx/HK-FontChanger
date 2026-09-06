import tkinter as tk
from tkinter import ttk, messagebox, font
import winreg
import ctypes
import sys

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
    try:
        path1 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path1, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Segoe UI (TrueType)", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(key, "Segoe UI Bold (TrueType)", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(key, "Segoe UI Italic (TrueType)", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(key, "Segoe UI Bold Italic (TrueType)", 0, winreg.REG_SZ, "")
        
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
            for val in ["Segoe UI (TrueType)", "Segoe UI Bold (TrueType)", "Segoe UI Italic (TrueType)", "Segoe UI Bold Italic (TrueType)"]:
                try: winreg.DeleteValue(key, val)
                except: pass
                
        path2 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path2, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, "Segoe UI")
            
        messagebox.showinfo("Success", "Default font restored.\nReboot to apply.")
    except Exception as e:
        messagebox.showerror("Registry Error", str(e))

def update_preview(*args):
    preview_label.config(font=(font_var.get(), 14))

# UI Setup
root = tk.Tk()
root.title("System Font Changer")
root.geometry("400x250")
root.resizable(False, False)

font_var = tk.StringVar(value="Segoe UI")
font_var.trace_add("write", update_preview)

ttk.Label(root, text="Select System Font:", font=("Segoe UI", 10)).pack(pady=(20, 5))
ttk.Combobox(root, textvariable=font_var, values=sorted(list(font.families())), state="readonly", width=30).pack()

preview_label = ttk.Label(root, text="Preview Text (AaBbCcYyZz 123)", font=("Segoe UI", 14))
preview_label.pack(pady=20)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Apply Font", command=lambda: apply_font(font_var.get()), width=15).pack(side=tk.LEFT, padx=10)
ttk.Button(btn_frame, text="Restore Default", command=restore_default, width=15).pack(side=tk.LEFT, padx=10)

root.mainloop()