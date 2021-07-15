@echo off

set working_path=%~dp0..\

python --version 3>NUL

if not errorlevel 0 GOTO :NOPYTHON

pip install -r %working_path%requirements.txt

python %working_path%source\Merge.py --print %1

pause


:NOPYTHON
echo.
echo Error^: Python not installed