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
echo Paso 1: Actualizando pip, setuptools y wheel...
python -m pip install --upgrade pip setuptools wheel --proxy=http://proxy-azure

echo.
echo Paso 2: Instalando numpy y pandas con wheels precompilados...
echo (Esto previene errores de compilacion)
pip install --only-binary :all: numpy pandas --proxy=http://proxy-azure

echo.
echo Paso 3: Instalando dependencias restantes desde requirements.txt...
echo (Esto puede tardar varios minutos)
echo.

pip install -r requirements.txt --proxy=http://proxy-azure --prefer-binary

echo.
if %errorlevel% equ 0 (
    echo ====================================
    echo Instalacion completada exitosamente
    echo ====================================
    echo.
    echo Verificando instalacion...
    pip list | findstr "streamlit pandas numpy"
) else (
    echo ====================================
    echo Error durante la instalacion
    echo.
    echo Si el error persiste con numpy/pandas:
    echo 1. Ejecuta: python -m pip install --upgrade pip
    echo 2. Ejecuta: pip install numpy==1.26.4 --only-binary :all: --proxy=http://proxy-azure
    echo 3. Ejecuta: pip install pandas==2.0.3 --only-binary :all: --proxy=http://proxy-azure
    echo 4. Vuelve a ejecutar este instalador
    echo ====================================
)

echo.
pause
