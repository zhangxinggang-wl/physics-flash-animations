@echo off
setlocal enabledelayedexpansion
chcp 437 >nul
cd /d "%~dp0"

echo ============================================================
echo   Push - High School Physics Flash Animation Library
echo ============================================================
echo.
echo   Files to upload : 1393
echo   Total size      : about 129 MB
echo   Branch          : main
echo.
echo   STEP 1 - Create an EMPTY repository on GitHub first:
echo.
echo       https://github.com/new
echo.
echo       Repository name : physics-flash-animations   (or any name)
echo       Visibility      : Public    - required for free GitHub Pages
echo       Initialize      : leave ALL checkboxes unchecked
echo                         do NOT add README / .gitignore / license
echo.
echo ------------------------------------------------------------
echo.

set /p REPO=STEP 2 - Paste the repo URL here, e.g. https://github.com/USER/REPO.git :

if "!REPO!"=="" (
  echo.
  echo   No URL entered. Aborted.
  pause
  exit /b 1
)

echo.
git remote remove origin 2>nul
git remote add origin "!REPO!"
if errorlevel 1 (
  echo   ERROR: could not set remote. Check the URL and try again.
  pause
  exit /b 1
)
echo   Remote origin set to: !REPO!
echo.

echo ------------------------------------------------------------
echo   STEP 3 - Pushing now. 129 MB upload, please be patient.
echo.
echo   When Git asks for credentials:
echo     Username : your GitHub username
echo     Password : a Personal Access Token, NOT your account password
echo.
echo   Create a token at: https://github.com/settings/tokens
echo     - Generate new token - classic
echo     - Tick the box   repo
echo     - Copy the token and paste it as the password
echo ------------------------------------------------------------
echo.

git push -u origin main

if errorlevel 1 (
  echo.
  echo ============================================================
  echo   PUSH FAILED
  echo ============================================================
  echo   Most common causes:
  echo.
  echo     1. Password rejected - you must use a Personal Access Token.
  echo        Create one at https://github.com/settings/tokens with scope: repo
  echo.
  echo     2. Repository not empty - it must be created with no README.
  echo.
  echo     3. Network or proxy problem - try again later.
  echo.
  echo   Fix the cause, then simply run this script again.
  echo.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo   PUSH OK
echo ============================================================
echo.
echo   STEP 4 - Enable GitHub Pages:
echo.
echo     Open your repo - Settings - Pages
echo     Source : Deploy from a branch
echo     Branch : main      Folder : / (root)
echo     Click Save, wait about 1 minute.
echo.
echo   Your site will be live at:
echo     https://YOUR-NAME.github.io/YOUR-REPO-NAME/
echo.
echo   The entry page is index.html - click any card to play.
echo.
pause
