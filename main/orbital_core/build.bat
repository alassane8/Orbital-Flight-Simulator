@echo off
setlocal enabledelayedexpansion
REM =====================================================================
REM  Recompile orbital_core (C++) and place the .pyd next to main.py
REM  Place this file in:  main\orbital_core\   then double-click it.
REM =====================================================================

REM --- 1. Choose the Python you RUN main.py with (must match!) ----------
set PY=py -3.13

REM Resolve the full path to that interpreter
for /f "delims=" %%i in ('%PY% -c "import sys;print(sys.executable)" 2^>nul') do set PYEXE=%%i
if not defined PYEXE (
  echo [ERREUR] Python 3.13 introuvable.
  echo          Installe-le, ou change la ligne "set PY=..." ci-dessus.
  pause & exit /b 1
)
echo Python utilise : %PYEXE%

REM --- 2. Make sure pybind11 is installed, grab its CMake folder --------
%PY% -m pip install --quiet --upgrade pybind11
for /f "delims=" %%i in ('%PY% -m pybind11 --cmakedir 2^>nul') do set PYBIND_DIR=%%i
if not defined PYBIND_DIR (
  echo [ERREUR] pybind11 introuvable apres installation.
  pause & exit /b 1
)
echo pybind11 : %PYBIND_DIR%

REM --- 3. Move to this script's folder (where CMakeLists.txt lives) -----
cd /d "%~dp0"

REM --- 4. Configure + build (Release) -----------------------------------
cmake -S . -B build -DPython_EXECUTABLE="%PYEXE%" -Dpybind11_DIR="%PYBIND_DIR%"
if errorlevel 1 (echo [ERREUR] Configuration CMake echouee. & pause & exit /b 1)

cmake --build build --config Release
if errorlevel 1 (echo [ERREUR] Compilation echouee. & pause & exit /b 1)

REM --- 5. Copy the new .pyd next to main.py (the parent "main" folder) --
copy /y "build\Release\orbital_core*.pyd" "..\" >nul
if errorlevel 1 (echo [ERREUR] Copie du .pyd impossible. & pause & exit /b 1)

echo.
echo [OK] orbital_core recompile et copie dans le dossier main\ .
echo      Tu peux relancer main.py.
pause
endlocal
