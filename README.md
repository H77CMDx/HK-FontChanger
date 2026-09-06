# Windows System Font Changer

A lightweight, GUI-based Python utility to easily change the default system font on Windows. Built with `tkinter` and `winreg`, it requires no external dependencies and automatically handles Administrator elevation. 

## Features

* **Live Font Preview:** Instantly see how your chosen font looks before applying it.
* **Auto-Elevation:** Automatically prompts for Windows UAC (Administrator) permissions on startup.
* **One-Click Restore:** Easily revert back to the default Windows font (Segoe UI).
* **Zero Dependencies:** Uses only Python's built-in standard library.

## Installing
Go into [releases] (https://github.com/H77CMDx/HK-FontChanger/releases) and install the zip archive. Or click [here](https://github.com/H77CMDx/HK-FontChanger/releases/download/Release/HK.Font.Changer.zip)

## Important Warnings

* **Windows Only:** This script specifically modifies the Windows Registry and uses Windows UAC. It will not work on macOS or Linux.
* **System Reboot Required:** You must restart your computer after applying or restoring a font for the changes to take effect across the entire OS.
* **Registry Modifications:** While safe, it is highly recommended to **create a System Restore Point** before modifying core registry keys. Stick to standard, pre-installed fonts to avoid UI rendering glitches.

## Getting Started

### Prerequisites
* Windows 10 or 11
* Python 3.x (if running from source)

### Running the EXE
* Open the "App" folder, then _internal, then the .exe file. 

### Running from Source
1. Clone or download this repository.
2. Open your terminal or command prompt.
3. Run the script (main.py)