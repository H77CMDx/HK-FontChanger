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

def require_admin():
    """Return whether the current process can write the system font registry keys."""
    if is_admin():
        return True

    messagebox.showwarning(
        "Administrator access required",
        "The font picker is running normally, but changing the Windows system font "
        "requires administrator access.\n\n"
        "Restart this app with 'Run as administrator' before applying a font.",
    )
    return False

def apply_font(selected_font):
    if not require_admin():
        return

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
    if not require_admin():
        return

    try:
        path1 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path1, 0, winreg.KEY_WRITE) as key:
            for registry_name, font_file in SEGOE_UI_REGISTRY_VALUES.items():
                winreg.SetValueEx(key, registry_name, 0, winreg.REG_SZ, font_file)

        path2 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path2, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, DEFAULT_FONT)

        select_font_by_name(DEFAULT_FONT_OPTION)

        messagebox.showinfo("Success", "Default font restored.\nReboot to apply.")
    except Exception as e:
        messagebox.showerror("Registry Error", str(e))


def update_preview(*args):
    selected_font = DEFAULT_FONT if font_var.get() == DEFAULT_FONT_OPTION else font_var.get()
    try:
        preview_label.config(font=(selected_font, 14))
    except tk.TclError:
        preview_label.config(font=(DEFAULT_FONT, 14))


def populate_listbox(filter_text=""):
    """Refill the listbox with fonts matching filter_text, each rendered in its own font."""
    filter_text = filter_text.strip().lower()

    matches = [f for f in font_options if filter_text in f.lower()]
    visible_font_options[:] = matches

    font_listbox.configure(state=tk.NORMAL)
    font_listbox.delete("1.0", tk.END)

    if not matches:
        font_listbox.insert(tk.END, "No fonts found", "empty")
        font_listbox.configure(state=tk.DISABLED)
        return

    for idx, name in enumerate(matches):
        tag = f"font_{idx}"
        display_font = DEFAULT_FONT if name == DEFAULT_FONT_OPTION else name
        try:
            font_listbox.tag_configure(tag, font=(display_font, 11))
        except tk.TclError:
            # Some fonts can't be instantiated at this size/style; fall back quietly
            font_listbox.tag_configure(tag, font=(DEFAULT_FONT, 11))
        font_listbox.insert(tk.END, f"{name}\n", tag)

    # Keep current selection highlighted if still present
    current = font_var.get()
    if current in matches:
        i = matches.index(current)
        start = f"{i + 1}.0"
        end = f"{i + 1}.end"
        font_listbox.tag_add("selected", start, end)
        font_listbox.see(start)

    font_listbox.configure(state=tk.DISABLED)


def select_font_by_name(name):
    font_var.set(name)
    # refresh listbox (clears any active filter so selection is visible) and highlight
    search_var.set("")
    populate_listbox("")
    update_preview()


def on_search_change(*args):
    populate_listbox(search_var.get())


def on_listbox_select(event):
    line = int(font_listbox.index(f"@{event.x},{event.y}").split(".")[0]) - 1
    if line < 0 or line >= len(visible_font_options):
        return

    name = visible_font_options[line]
    font_var.set(name)
    font_listbox.configure(state=tk.NORMAL)
    font_listbox.tag_remove("selected", "1.0", tk.END)
    font_listbox.tag_add("selected", f"{line + 1}.0", f"{line + 1}.end")
    font_listbox.configure(state=tk.DISABLED)
    update_preview()


# UI Setup
root = tk.Tk()
root.title("System Font Changer")
root.geometry("420x480")
root.resizable(False, False)
try:
    root.iconbitmap(str(resource_path(ICON_FILE)))
except tk.TclError:
    pass

font_var = tk.StringVar(value=DEFAULT_FONT_OPTION)
search_var = tk.StringVar()
search_var.trace_add("write", on_search_change)
visible_font_options = []

ttk.Label(root, text="Search Fonts:", font=("Segoe UI", 10)).pack(pady=(15, 5), padx=15, anchor="w")
search_entry = ttk.Entry(root, textvariable=search_var, width=40)
search_entry.pack(padx=15, fill="x")

list_frame = ttk.Frame(root)
list_frame.pack(padx=15, pady=(8, 10), fill="both", expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
font_listbox = tk.Text(
    list_frame,
    yscrollcommand=scrollbar.set,
    height=12,
    width=40,
    wrap="none",
    cursor="hand2",
    padx=6,
    pady=4,
    spacing1=2,
    borderwidth=1,
    relief="solid",
)
font_listbox.tag_configure("selected", background="#dbeafe", foreground="#111827")
font_listbox.tag_configure("empty", foreground="#777777", font=(DEFAULT_FONT, 11, "italic"))
scrollbar.config(command=font_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
font_listbox.pack(side=tk.LEFT, fill="both", expand=True)
font_listbox.bind("<Button-1>", on_listbox_select)

font_options = [DEFAULT_FONT_OPTION] + sorted(f for f in font.families() if f != DEFAULT_FONT_OPTION)

preview_label = ttk.Label(root, text="Preview Text (AaBbCcYyZz 123)", font=("Segoe UI", 14))
preview_label.pack(pady=15)

populate_listbox("")
select_font_by_name(DEFAULT_FONT_OPTION)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=(0, 15))

ttk.Button(btn_frame, text="Apply Font", command=lambda: apply_font(font_var.get()), width=15).pack(side=tk.LEFT, padx=10)
ttk.Button(btn_frame, text="Reset Default", command=restore_default, width=15).pack(side=tk.LEFT, padx=10)

root.mainloop()
