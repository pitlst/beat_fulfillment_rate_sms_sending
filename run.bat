@echo off
cd /d "%~dp0"
uv run python main.py
if %errorlevel% neq 0 (
    echo [%date% %time%] 执行失败，错误码: %errorlevel% >> error.log
)
