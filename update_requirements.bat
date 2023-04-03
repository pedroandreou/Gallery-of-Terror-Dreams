@echo off
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
for /d %%i in (src\back-end src\front-end) do type "%%i\pinned_requirements.txt" >> pinned_requirements_temp.txt
%VENV%\Scripts\pip install -r pinned_requirements_temp.txt
del pinned_requirements_temp.txt

:: Add a comment line to the requirements.txt file
echo # Created automatically by make update-requirements-txt. Do not update manually! > requirements.txt

:: List installed packages and filter out pkg_resources, then append the list to requirements.txt
%VENV%\Scripts\pip freeze | findstr /v pkg_resources >> requirements.txt
