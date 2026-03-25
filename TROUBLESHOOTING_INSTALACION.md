# 🔧 Solución de Problemas - Instalación

## ⚠️ Error: "metadata-generation-failed" con numpy/pandas

### Síntoma
```
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> numpy
note: This is an issue with the package mentioned above, not pip.
ERROR: Failed to build 'pandas' when installing build dependencies for pandas
```

### Causa
Pip intenta compilar numpy/pandas desde código fuente, lo que requiere herramientas de compilación C++ que no están instaladas.

### ✅ SOLUCIÓN 1: Ejecutar el instalador actualizado (RECOMENDADO)

El archivo `install_dependencies.bat` ya está actualizado con la solución. Simplemente:

1. Doble clic en `install_dependencies.bat`
2. Espera a que termine (5-10 minutos)

El script actualizado:
- ✅ Actualiza pip/setuptools/wheel primero
- ✅ Instala numpy y pandas con wheels precompilados
- ✅ Usa `--prefer-binary` para evitar compilación
- ✅ Configura el proxy automáticamente

### ✅ SOLUCIÓN 2: Instalación manual paso a paso

Si el instalador automático falla, ejecuta estos comandos en CMD:

```bash
# 1. Configurar proxy (red corporativa YPF)
set HTTPS_PROXY=http://proxy-azure
set HTTP_PROXY=http://proxy-azure

# 2. Actualizar herramientas base
python -m pip install --upgrade pip setuptools wheel --proxy=http://proxy-azure

# 3. Instalar numpy y pandas con wheels precompilados
pip install --only-binary :all: numpy pandas --proxy=http://proxy-azure

# 4. Instalar el resto de dependencias
pip install -r requirements.txt --proxy=http://proxy-azure --prefer-binary
```

### ✅ SOLUCIÓN 3: Versiones específicas

Si persisten los errores, usa versiones específicas compatibles:

```bash
set HTTPS_PROXY=http://proxy-azure
set HTTP_PROXY=http://proxy-azure

pip install numpy==1.26.4 --only-binary :all: --proxy=http://proxy-azure
pip install pandas==2.0.3 --only-binary :all: --proxy=http://proxy-azure
pip install streamlit==1.31.0 --proxy=http://proxy-azure --prefer-binary
pip install -r requirements.txt --proxy=http://proxy-azure --prefer-binary
```

---

## 🔍 Otros Problemas de Instalación

### Error: "No matching distribution found"

**Causa**: No hay conexión al proxy o PyPI no es accesible.

**Solución**:
```bash
# Verificar conexión al proxy
curl https://pypi.org --proxy http://proxy-azure --max-time 10

# Si falla, verificar configuración de proxy
echo %HTTPS_PROXY%
echo %HTTP_PROXY%
```

### Error: "Could not find a version that satisfies the requirement"

**Causa**: Versión de pip desactualizada.

**Solución**:
```bash
python -m pip install --upgrade pip --proxy=http://proxy-azure
```

### Error: Importación falla después de instalar

**Causa**: Múltiples versiones de Python o entorno virtual no activado.

**Solución**:
```bash
# Verificar versión de Python
python --version

# Verificar paquetes instalados
pip list | findstr "numpy pandas streamlit"

# Reinstalar en caso necesario
pip uninstall numpy pandas -y
pip install --only-binary :all: numpy pandas --proxy=http://proxy-azure
```

---

## 📋 Verificación Post-Instalación

Después de instalar, verifica que todo funcione:

```bash
# Verificar paquetes críticos
pip list | findstr "streamlit pandas numpy"
```

Deberías ver:
```
numpy         1.26.x
pandas        2.0.x
streamlit     1.31.x
```

Luego ejecuta:
```bash
python -c "import streamlit; import pandas; import numpy; print('Todo OK!')"
```

Si no hay errores, ¡la instalación fue exitosa!

---

## 🌐 Instalación Fuera de Red Corporativa

Si instalas fuera de la red YPF (sin proxy):

```bash
# NO configurar proxy
python -m pip install --upgrade pip setuptools wheel
pip install --only-binary :all: numpy pandas
pip install -r requirements.txt --prefer-binary
```

---

## 💡 Flags Importantes

| Flag | Propósito |
|------|-----------|
| `--only-binary :all:` | Fuerza el uso de wheels precompilados (NO compila desde fuente) |
| `--prefer-binary` | Prefiere wheels cuando estén disponibles |
| `--proxy=http://proxy-azure` | Usa el proxy corporativo de YPF |
| `--upgrade` | Actualiza a la última versión |
| `--no-cache-dir` | No usa caché (útil si hay corrupción) |

---

## 📞 Contacto y Soporte

Si los problemas persisten después de intentar estas soluciones:

1. Ejecuta este comando de diagnóstico:
```bash
python --version
pip --version
pip list | findstr "numpy pandas streamlit"
```

2. Comparte:
   - El mensaje de error completo
   - La salida del comando de diagnóstico
   - Si estás en red corporativa o no

---

## 🔄 Última Actualización

**Fecha**: 25-Mar-2026
**Versión**: v4.0
**Autor**: YPF IT Analytics Team
