@echo off
setlocal

REM Uninstall all the requirements that are currently in the virtual env
pip freeze | xargs pip uninstall -y

REM Install packages from unpinned_requirements.txt
pip install -r unpinned_requirements.txt

REM Create a new requirements.txt file with pinned dependencies
echo # Created automatically by update_requirements.bat. Do not update manually! > requirements.txt
pip freeze | findstr /V "pkg_resources" >> requirements.txt
