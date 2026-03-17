@echo off
echo ====================================
echo Power BI Documentation Generator v3.0
echo Instalador de Dependencias - Red Corporativa YPF
echo ====================================
echo.

echo Configurando proxy corporativo YPF...
set HTTPS_PROXY=http://proxy-azure
set HTTP_PROXY=http://proxy-azure

echo.
echo Instalando dependencias desde requirements.txt...
echo (Esto puede tardar varios minutos)
echo.

pip install -r requirements.txt

echo.
if %errorlevel% equ 0 (
    echo ====================================
    echo ✅ Instalacion completada exitosamente
    echo ====================================
) else (
    echo ====================================
    echo ❌ Error durante la instalacion
    echo Verifica la conexion al proxy y reintenta
    echo ====================================
)

echo.
pause
