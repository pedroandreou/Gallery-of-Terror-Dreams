@echo off
setlocal enabledelayedexpansion

for %%d in (src\back-end src\front-end) do (
    set "input_file=%%~d\unpinned_requirements.txt"
    set "output_file=%%~d\pinned_requirements.txt"
    del !output_file! 2>nul
    for /f "tokens=2 delims=: " %%i in ('pip show -f !input_file! ^| findstr /r "^Name: ^Version:"') do (
        set "package=%%i"
        set "version=%%j"
        echo !package!==!version!>>!output_file!
    )
)
