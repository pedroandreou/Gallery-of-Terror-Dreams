@echo off
setlocal enabledelayedexpansion

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
