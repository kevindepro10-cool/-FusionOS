@echo off
title FusionOS 1.0
cd /d "%~dp0"
python main.py
if errorlevel 1 (
  echo.
  echo FusionOS konnte nicht gestartet werden. Ist Python installiert?
  echo Download: https://www.python.org/downloads/  (bei Installation "Add to PATH" ankreuzen)
  pause
)
