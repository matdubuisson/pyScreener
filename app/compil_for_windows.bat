@echo off

pyinstaller --onefile client_gui_pyScreener.py
move dist\client_gui_pyScreener.exe ..\installer\executables\windows\.