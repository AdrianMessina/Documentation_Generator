@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ============================================================
echo      Power BI Documentation Generator v4.0
echo ============================================================
echo.
echo VERSION: 4.0.0 (16-Mar-2026)
echo Aplicacion: ui/app.py (v4.0)
echo.
echo ============================================================
echo.
echo Iniciando aplicacion...
echo.
echo La aplicacion se abrira en tu navegador automaticamente
echo URL: http://localhost:8501
echo.
echo Para detener: presiona Ctrl+C
echo ============================================================
echo.

REM Set proxy for corporate network (if needed)
set HTTPS_PROXY=http://proxy-azure
set HTTP_PROXY=http://proxy-azure

cd /d "%~dp0"

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the v4.0 application
streamlit run "ui/app.py"

pause
