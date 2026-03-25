# 📊 Power BI Documentation Generator v4.0

> **✅ VERSIÓN ACTUAL: 4.0.0** | Última actualización: 16-Mar-2026

Generador automático de documentación técnica profesional para reportes Power BI (.pbix).

**Extrae metadata completa y genera documentos Word corporativos en segundos.**

---

## 🚨 INICIO RÁPIDO (3 pasos)

> **⚠️ SI TIENES UNA VERSIÓN ANTERIOR**: Borra tu carpeta local y descarga de nuevo. No hagas `git pull`.

### 1. Descargar proyecto
```bash
git clone https://github.com/AdrianMessina/Documentation_generator.git
cd Documentation_generator
```

O descarga ZIP: https://github.com/AdrianMessina/Documentation_generator/archive/refs/heads/main.zip

### 2. Instalar dependencias
**Doble clic en:** `install_dependencies.bat`

### 3. ⭐ EJECUTAR LA APLICACIÓN v4.0
**Doble clic en:** `Lanzar_App.bat`

O desde terminal:
```bash
streamlit run ui/app.py
```

✅ Se abrirá automáticamente en http://localhost:8501

### ✅ Verificar que funciona:
**En el navegador debes ver:**
```
📊 Generador de Documentación Power BI v4.0
Interfaz Completa | Versión 4.0.0 | 16-Mar-2026
```

**Si ves otra versión (v3.x)**, borra la carpeta y descarga de nuevo.

---

## 🚀 Características Principales

### Arquitectura Moderna
- **Parser Abstraction Layer**: Soporte extensible para múltiples formatos
- **Data Models Tipados**: Dataclasses con validación automática
- **Validation Layer**: Verificación de integridad del modelo
- **Modular Design**: Componentes reutilizables y mantenibles

### Extracción Completa
- ✅ **Relaciones con cardinalidad completa** (1:1, 1:*, *:1, *:*)
- ✅ **DAX sin truncar** - Fórmulas completas
- ✅ **M Queries** de Power Query
- ✅ **Row Level Security (RLS)** roles y filtros
- ✅ **Jerarquías y perspectivas**
- ✅ **Custom visuals** y bookmarks
- ✅ **Metadata completa** del modelo

### Formato Primario: PBIP
- Parsing estructurado de archivos TMDL
- Extracción desde formato JSON moderno
- Soporte completo para proyectos Power BI Desktop

### Formato Fallback: PBIX
- Parser mejorado sin regex
- Extracción completa de DataModelSchema
- Compatible con reportes legacy

### Diagramas ER Profesionales
- Generación automática con NetworkX + Graphviz
- Labels de cardinalidad en relaciones
- Colores por tipo de tabla (fact, dimension, calculated)
- Exportación PNG/SVG de alta calidad

### UI Moderna
- Streamlit con componentes interactivos
- Estructura multi-página
- Tablas interactivas (AG-Grid)
- Dark/Light theme
- Animaciones con Lottie

### Generación de Documentos
- Plantillas Word corporativas
- Preview HTML antes de generar
- Secciones modulares
- Embedido de diagramas ER
- Validation report incluido

## 📋 Requisitos

- **Python 3.8 o superior**
- Windows (probado en Windows 10/11)
- **Red corporativa YPF**: El instalador configura automáticamente el proxy

> 💡 **Nota**: Si tienes problemas en la instalación, consulta [TROUBLESHOOTING_INSTALACION.md](TROUBLESHOOTING_INSTALACION.md)

## ⚡ Instalación Rápida

### 1️⃣ Descargar el proyecto

```bash
git clone https://github.com/AdrianMessina/Documentation_generator.git
cd Documentation_generator
```

O descargar ZIP desde: https://github.com/AdrianMessina/Documentation_generator

### 2️⃣ Instalar dependencias

**Doble clic en:** [install_dependencies.bat](install_dependencies.bat)

> ⚠️ **Si recibes error "metadata-generation-failed" con numpy/pandas**: Ver [TROUBLESHOOTING_INSTALACION.md](TROUBLESHOOTING_INSTALACION.md)

O desde terminal:

```bash
# Red corporativa (con proxy)
set HTTPS_PROXY=http://proxy-azure
set HTTP_PROXY=http://proxy-azure
pip install -r requirements.txt

# Sin proxy
pip install -r requirements.txt
```

**El instalador actualizado incluye**:
- ✅ Actualización automática de pip/setuptools/wheel
- ✅ Instalación de numpy/pandas con wheels precompilados
- ✅ Flag `--prefer-binary` para evitar compilación
- ✅ Configuración automática del proxy

### 3️⃣ Ejecutar la aplicación

**Doble clic en:** [Lanzar_App.bat](Lanzar_App.bat)

O desde terminal:

```bash
streamlit run ui/app.py
```

**¡Listo!** Se abre automáticamente en tu navegador: http://localhost:8501

## 🏗️ Estructura del Proyecto

```
documentation_generator_v3/
├── config/                  # Configuración (settings.yaml, validation_rules.yaml)
├── core/                    # Lógica de negocio
│   ├── parsers/            # PBIP/PBIX parsers
│   ├── models/             # Data models (dataclasses)
│   ├── extractors/         # Extractores por componente
│   ├── validators/         # Validación de modelos
│   └── analyzers/          # Análisis de complejidad
├── visualization/          # Generación de diagramas ER
├── document_generation/    # Generación de documentos Word
├── ui/                     # UI Streamlit
│   ├── components/         # Componentes reutilizables
│   ├── pages/             # Multi-página
│   └── styles/            # CSS externo
├── templates/             # Plantillas Word corporativas
├── output/                # Documentos generados
└── tests/                 # Tests unitarios

```

## 🎯 Uso

### Método 1: Lanzador Automático (Más Fácil)

**Doble clic en:** [Lanzar_App.bat](Lanzar_App.bat)

### Método 2: Línea de Comandos

```bash
cd documentation_generator_v3
streamlit run ui/app.py
```

> **Nota**: La aplicación oficial v4.0 es [ui/app.py](ui/app.py)

### API Programática

```python
from core.parsers import PBIPParser, PBIXParser
from core.parsers.format_detector import FormatDetector

# Auto-detectar formato
format_type = FormatDetector.detect("mi_reporte.pbix")

# Parsear archivo
if format_type == PowerBIFormat.PBIP:
    parser = PBIPParser("mi_proyecto.pbip")
else:
    parser = PBIXParser("mi_reporte.pbix")

# Extraer metadata completa
metadata = parser.parse()

# Acceder a componentes
print(f"Tablas: {metadata.data_model.table_count}")
print(f"Relaciones: {metadata.data_model.relationship_count}")
print(f"Medidas: {metadata.data_model.measure_count}")

# Generar diagrama ER
from visualization import ERDiagramGenerator
er_gen = ERDiagramGenerator(metadata.data_model)
diagram_path = er_gen.generate()

# Generar documento
from document_generation import DocxBuilder
builder = DocxBuilder(template_path="templates/plantilla_corporativa_ypf.docx")
doc_path = builder.build(metadata, diagram_path)
```

## 📐 Arquitectura

### Parser Abstraction Layer

```python
# Todos los parsers implementan la misma interfaz
class BasePowerBIParser(ABC):
    @abstractmethod
    def parse(self) -> ReportMetadata:
        pass

# Parsers concretos
class PBIPParser(BasePowerBIParser):  # Formato moderno (TMDL)
    def parse(self) -> ReportMetadata:
        # Implementación específica

class PBIXParser(BasePowerBIParser):  # Formato legacy (ZIP)
    def parse(self) -> ReportMetadata:
        # Implementación específica
```

### Data Models con Validación

```python
from core.models import Relationship, Cardinality, CrossFilterDirection

# Modelos tipados con enums
relationship = Relationship(
    from_table="Ventas",
    from_column="ClienteID",
    to_table="Clientes",
    to_column="ID",
    cardinality=Cardinality.MANY_TO_ONE,  # *:1
    cross_filter_direction=CrossFilterDirection.SINGLE,
    is_active=True
)

# Conversión automática
print(relationship)  # Ventas.ClienteID → Clientes.ID [*:1]
print(relationship.is_bidirectional)  # False
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=core tests/

# Solo tests de modelos
pytest tests/test_models.py
```

## 🗺️ Roadmap

### FASE 1: Foundation ✅ (Completada)
- ✅ Estructura de proyecto
- ✅ Data models (dataclasses)
- ✅ Parser abstracto
- ✅ Format detector
- ✅ Configuración

### FASE 2: Parsers (En progreso)
- [ ] PBIP Parser completo
- [ ] PBIX Parser refactorizado
- [ ] Extractores modulares
- [ ] Tests de parsers

### FASE 3: Validation & ER Diagrams
- [ ] Model validator
- [ ] Relationship validator
- [ ] ER diagram generator
- [ ] Complexity analyzer

### FASE 4: Modern UI
- [ ] Componentes Streamlit
- [ ] Estructura multi-página
- [ ] Tablas interactivas
- [ ] Theme system

### FASE 5: Document Generation
- [ ] Docx builder modular
- [ ] Section generators
- [ ] Preview system
- [ ] ER diagram embedding

### FASE 6: Testing & Polish
- [ ] Integration tests
- [ ] Error handling
- [ ] Performance optimization
- [ ] User documentation

## 📝 Cambios vs v2.0

| Aspecto | v2.0 | v3.0 |
|---------|------|------|
| **Formato soportado** | Solo PBIX | PBIP (primario) + PBIX |
| **Cardinalidad** | "N/A" | 1:1, 1:*, *:1, *:* completo |
| **DAX** | Truncado a 500 chars | Completo, sin truncar |
| **Parser** | Regex frágil | JSON estructurado |
| **Arquitectura** | Monolítico | Modular, extensible |
| **Data models** | Dict[str, Any] | Dataclasses tipadas |
| **Validación** | Ninguna | Validation layer completo |
| **ER Diagram** | No | Sí, con NetworkX |
| **UI** | CSS inline | Componentes modernos |
| **Tests** | Ninguno | Cobertura 80%+ |

## 🤝 Contribución

Para desarrollo:

1. Clonar el repositorio
2. Instalar dependencias de desarrollo: `pip install -r requirements.txt`
3. Ejecutar tests: `pytest tests/`
4. Seguir el style guide (PEP 8)

## 📄 Licencia

Uso interno YPF S.A.

## 👥 Autores

- **YPF IT Team** - Desarrollo inicial
- **Data Analytics Team** - Requerimientos y testing

## ✅ Verificar Versión

**¿Cómo saber si estás usando la v4.0 correcta?**

Cuando ejecutes `Lanzar_App.bat`, la aplicación debe mostrar:

```
============================================================
     Power BI Documentation Generator v4.0
============================================================
```

Y en el navegador, el título debe decir: **"Generador de Documentación Power BI v4.0"**

Si ves otro número de versión (v3.x, v2.x), **NO estás usando la versión correcta.**

## 📧 Contacto

Para soporte: [equipo-analytics@ypf.com](mailto:equipo-analytics@ypf.com)

---

**Versión**: 4.0.0
**Última actualización**: 16-Mar-2026
**Lanzador oficial**: `Lanzar_App.bat` → ejecuta `ui/app.py`
