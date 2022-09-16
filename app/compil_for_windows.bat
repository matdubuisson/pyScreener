@echo off

:: Author : matdubuisson
:: Source : https://github.com/matdubuisson/pyScreener
:: Licence : Apache (2)

pyinstaller --onefile client_gui_pyScreener.py
move dist\client_gui_pyScreener.exe ..\installer\executables\windows\.
