call ".venv\Scripts\activate.bat"
pyinstaller --onedir --noconsole --icon "HK Font Changer.ico" --add-data "HK Font Changer.ico;." "main.py"
pause