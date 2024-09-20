@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python to continue.
    exit /b
)

REM Check Python version (assuming you need Python 3.x)
for /f "tokens=2 delims=." %%i in ('python --version 2^>^&1') do (
    if %%i LSS 3 (
        echo Python 3.x is required. Please upgrade your Python version.
        exit /b
    )
)

REM Check if required modules are installed
python -c "import sys; import PyQt5; import requests" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Required Python modules are not installed. Installing now...
    python -m pip install PyQt5 requests
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install required modules. Please check your Python and pip installation.
        exit /b
    )
)

REM Inform the user and countdown before minimizing
echo The console window will be minimized while the script runs.
echo Launching main.pyw in 5 seconds...

REM Countdown loop
set /a counter=5
:countdown
echo %counter%...
set /a counter=%counter%-1
if %counter% geq 0 (
    timeout /t 1 >nul
    goto countdown
)

REM Minimize the console window
powershell -command "& {Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Win32ShowWindow { [DllImport(\"user32.dll\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }'; [Win32ShowWindow]::ShowWindow([System.Diagnostics.Process]::GetCurrentProcess().MainWindowHandle, 6)}"

REM Launch the Python script without opening a console window
start "" /b pythonw main.pyw