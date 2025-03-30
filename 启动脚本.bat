@echo off
start "" cmd /k "cd /d "%~dp0/.venv/Scripts" && call activate.bat &&python ../GUI.py"