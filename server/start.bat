@echo off
for /f "tokens=2 delims= " %%a in ('tasklist ^| findstr "py.exe"') do (
    taskkill /PID %%a /F
)
start cmd /k py performa.py
