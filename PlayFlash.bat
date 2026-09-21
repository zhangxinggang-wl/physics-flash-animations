@echo off
rem ============================================================
rem  Flash Physics Animation Player - Launcher
rem  Zhang Xinggang Studio
rem
rem  Finds a Python interpreter that has tkinter, then starts the
rem  GUI launcher (FlashAnimationPlayer.pyw) without a console.
rem ============================================================
setlocal enabledelayedexpansion

set "BASE=%~dp0"
set "GUI=%BASE%FlashAnimationPlayer.pyw"

if not exist "%GUI%" (
  echo.
  echo  [ERROR] FlashAnimationPlayer.pyw not found in this folder.
  echo          Please keep this .bat next to the .pyw file.
  echo.
  pause
  exit /b 1
)

rem ---------- 1) preferred: user-scope Python 3.14 with tkinter ----------
set "P1=%LOCALAPPDATA%\Python\bin\pythonw.exe"
if exist "%P1%" (
  start "" "%P1%" "%GUI%"
  exit /b 0
)

set "P2=%LOCALAPPDATA%\Python\bin\python.exe"
if exist "%P2%" (
  "%P2%" "%GUI%"
  exit /b 0
)

rem ---------- 2) python on PATH ----------
where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw "%GUI%"
  exit /b 0
)
where python >nul 2>nul
if %errorlevel%==0 (
  python "%GUI%"
  exit /b 0
)

rem ---------- 3) common install directories ----------
for %%D in (
  "%LOCALAPPDATA%\Programs\Python\Python314"
  "%LOCALAPPDATA%\Programs\Python\Python313"
  "%LOCALAPPDATA%\Programs\Python\Python312"
  "%LOCALAPPDATA%\Programs\Python\Python311"
  "%LOCALAPPDATA%\Programs\Python\Python310"
  "C:\Python314"
  "C:\Python313"
  "C:\Python312"
) do (
  if exist "%%~D\pythonw.exe" (
    start "" "%%~D\pythonw.exe" "%GUI%"
    exit /b 0
  )
  if exist "%%~D\python.exe" (
    "%%~D\python.exe" "%GUI%"
    exit /b 0
  )
)

rem ---------- 4) give up ----------
echo.
echo  [ERROR] No suitable Python (with tkinter) was found.
echo.
echo   Option A  Install Python from https://www.python.org/downloads/
echo             Check "Add python.exe to PATH" and "tcl/tk and IDLE".
echo.
echo   Option B  Do not use this launcher at all:
echo             open the chapter folder in File Explorer and
echo             double-click any .swf file.
echo             The player association is already configured.
echo.
pause
exit /b 1
