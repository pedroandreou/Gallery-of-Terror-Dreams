@echo off
setlocal enabledelayedexpansion

:: Set variables for the virtual environment
set VENV=.venv

:: Remove existing virtual environment if it exists
if exist %VENV% rmdir /s /q %VENV%

:: Create a new virtual environment directory
mkdir %VENV%

:: Create a new virtual environment using the system's Python
python -m venv %VENV%

:: Set the Python executable variable to the one inside the virtual environment
set PYTHON=%VENV%\Scripts\python.exe

:: Upgrade pip to the specified version
%VENV%\Scripts\pip install --upgrade pip==22.2.2

:: Install packages from the pinned_requirements.txt files from both front-end and back-end dirs
for /d %%i in (src\back-end src\front-end) do type "%%i\unpinned_requirements.txt" >> unpinned_requirements_temp.txt
%VENV%\Scripts\pip install -r unpinned_requirements_temp.txt
del unpinned_requirements_temp.txt

:: Add a comment line to the requirements.txt file
echo # Created automatically by make update-and-pin-requirements-txt. Do not update manually! > requirements.txt

:: List installed packages and filter out pkg_resources, then append the list to requirements.txt
%VENV%\Scripts\pip freeze | findstr /v pkg_resources >> requirements.txt

:: Pin the versions of the packages in the unpinned_requirements.txt files
set dirs=src\back-end src\front-end
set input_file=unpinned_requirements.txt
set tempfile=temp_output.txt

for %%G in (%dirs%) do (
    if exist %%G\pinned_requirements.txt (
        del /Q %%G\pinned_requirements.txt
    )
    for /F "delims=" %%L in (%%G\%input_file%) do (
        for /F "tokens=1,2 delims=: " %%A in ('pip show %%L ^| findstr /R "^Name: ^Version:"') do (
            if "%%A"=="Name" (
                set name=%%B
            ) else (
                echo !name!==%%B>> %tempfile%
            )
        )
    )
    type %tempfile% | sort | uniq > %%G\pinned_requirements.txt
    if exist %tempfile% (
        del /Q %tempfile%
    )
)
