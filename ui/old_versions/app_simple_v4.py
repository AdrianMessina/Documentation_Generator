"""
Power BI Documentation Generator v4.0 - SIMPLE & CLEAN
Interfaz simplificada, solo PBIP, todo en español
"""

import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.parsers import FormatDetector, PowerBIFormat
from core.parsers.tmdl_parser_v2 import TMDLParserV2
from document_generation.docx_builder_v3 import DocxBuilderV3

# Page config
st.set_page_config(
    page_title="Generador de Documentación Power BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Clean and modern
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }

    /* Step cards */
    .step-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .step-card.active {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102,126,234,0.2);
    }

    .step-card h3 {
        color: #667eea;
        margin-top: 0;
    }

    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .success-box {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }

    /* Forms */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border-color: #e0e0e0;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Generador de Documentación Power BI v4.0</h1>
    <p>Documentación técnica automática desde archivos PBIP | Versión 4.0.0</p>
</div>
""", unsafe_allow_html=True)

# Helper function
def clean_path(path_str: str) -> str:
    """Remove quotes and extra spaces from path"""
    if not path_str:
        return ""
    return path_str.strip().strip('"').strip("'").strip()

# STEP 1: Select File
st.markdown('<div class="step-card active">', unsafe_allow_html=True)
st.markdown("### 📁 Paso 1: Selecciona tu Proyecto PBIP")

st.markdown("""
<div class="info-box">
    <strong>💡 ¿Cómo obtener la ruta?</strong>
    <ol style="margin: 0.5rem 0 0 0;">
        <li>Abre el Explorador de Windows</li>
        <li>Navega hasta tu proyecto Power BI (.pbip)</li>
        <li>Haz clic en la barra de direcciones</li>
        <li>Copia la ruta completa (Ctrl+C)</li>
        <li>Pégala en el campo de abajo</li>
    </ol>
</div>
""", unsafe_allow_html=True)

pbip_input = st.text_input(
    "Ruta del proyecto PBIP:",
    placeholder=r"C:\Users\TuNombre\Documents\PowerBI\MiProyecto.pbip",
    help="Pega aquí la ruta completa de tu proyecto",
    key="pbip_path_input"
)

file_ready = False

if pbip_input:
    cleaned_path = clean_path(pbip_input)
    path_obj = Path(cleaned_path)

    if path_obj.exists():
        st.success(f"✅ Proyecto encontrado: **{path_obj.name}**")
        st.session_state.file_path = path_obj
        file_ready = True

        with st.expander("📂 Ver estructura del proyecto"):
            if path_obj.is_file():
                parent = path_obj.parent
                st.write(f"**Carpeta del proyecto:** `{parent}`")
            else:
                st.write(f"**Carpeta del proyecto:** `{path_obj}`")

            report_folders = list(path_obj.parent.glob("*.Report")) if path_obj.is_file() else list(path_obj.glob("*.Report"))
            model_folders = list(path_obj.parent.glob("*.SemanticModel")) if path_obj.is_file() else list(path_obj.glob("*.SemanticModel"))

            if report_folders:
                st.write(f"✅ Carpeta .Report: `{report_folders[0].name}`")
            if model_folders:
                st.write(f"✅ Carpeta .SemanticModel: `{model_folders[0].name}`")
    else:
        st.error(f"❌ No se encontró el archivo: `{cleaned_path}`")

st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: Configure
if file_ready:
    st.markdown('<div class="step-card active">', unsafe_allow_html=True)
    st.markdown("### ✏️ Paso 2: Completa la Información del Documento")

    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ Campos opcionales:</strong> Los campos marcados con (*) son opcionales.
        Si los dejas vacíos, se generarán automáticamente usando los datos del PBIP.
    </div>
    """, unsafe_allow_html=True)

    with st.form("config_form"):
        st.markdown("#### 📋 Información Básica")

        # Título del reporte
        titulo_reporte = st.text_input(
            "Título del Reporte",
            placeholder="Ejemplo: Análisis de Ventas Regionales Q1 2026",
            help="Nombre que aparecerá en la portada del documento. Si se deja vacío, se usará el nombre del archivo PBIP"
        )

        col1, col2 = st.columns(2)
        with col1:
            version = st.text_input("Versión del documento", value="1.0", help="Ejemplo: 1.0, 2.1")
        with col2:
            autor = st.text_input("Autor", value="YPF IT Analytics Team", help="Responsable del documento")

        observaciones = st.text_input(
            "Observaciones de la versión",
            value="Generación inicial de documentación técnica",
            help="Descripción de los cambios"
        )

        st.markdown("---")
        st.markdown("#### 🎯 Información del Reporte (Opcional)")

        objetivo = st.text_area(
            "Objetivo del reporte (*)",
            placeholder="Ejemplo: Proporcionar análisis de ventas regionales del Q1 2026...",
            help="Se generará automáticamente si se deja vacío",
            height=100
        )

        alcance = st.text_area(
            "Alcance del análisis (*)",
            placeholder="Ejemplo: Incluye datos de ventas desde enero 2024, todas las regiones...",
            help="Se detectará automáticamente si se deja vacío",
            height=100
        )

        col1, col2 = st.columns(2)
        with col1:
            administrador = st.text_input(
                "Administrador del reporte (*)",
                placeholder="Ejemplo: María González - Analytics Team",
                help="Opcional"
            )
        with col2:
            solicitante = st.text_input(
                "Solicitante (*)",
                placeholder="Ejemplo: Dirección Comercial",
                help="Opcional"
            )

        st.markdown("---")
        st.markdown("#### 🔄 Configuración Técnica (Opcional)")

        col1, col2 = st.columns(2)
        with col1:
            frecuencia = st.selectbox(
                "Frecuencia de actualización (*)",
                ["No especificada", "Diaria", "Semanal", "Mensual", "Tiempo real"]
            )
        with col2:
            horario = st.text_input(
                "Horario de actualización (*)",
                placeholder="Ejemplo: 06:00 AM (GMT-3)",
                help="Opcional"
            )

        if frecuencia != "No especificada" and horario:
            frecuencia_completa = f"{frecuencia} - {horario}"
        else:
            frecuencia_completa = frecuencia

        st.markdown("")
        analyze_button = st.form_submit_button(
            "🚀 Analizar y Generar Documentación",
            use_container_width=True
        )

    if analyze_button:
        # Save user inputs
        st.session_state.user_inputs = {
            'titulo_reporte': titulo_reporte if titulo_reporte.strip() else None,
            'version': version,
            'autor': autor,
            'observaciones': observaciones,
            'objetivo': objetivo if objetivo.strip() else None,
            'alcance': alcance if alcance.strip() else None,
            'administrador': administrador if administrador.strip() else None,
            'solicitante': solicitante if solicitante.strip() else None,
            'frecuencia': frecuencia_completa
        }

        try:
            with st.spinner("🔄 Analizando proyecto Power BI..."):
                progress = st.progress(0)

                # Detect format
                file_path = st.session_state.file_path
                format_detector = FormatDetector()
                detected_format = format_detector.detect(str(file_path))

                progress.progress(20)

                # Parse PBIP
                if detected_format == PowerBIFormat.PBIP:
                    if file_path.is_file():
                        parent = file_path.parent
                    else:
                        parent = file_path

                    model_folders = list(parent.glob("*.SemanticModel"))
                    if not model_folders:
                        raise Exception("No se encontró la carpeta .SemanticModel en el proyecto")

                    definition_path = model_folders[0] / "definition"
                    if not definition_path.exists():
                        raise Exception(f"No se encontró la carpeta definition: {definition_path}")

                    progress.progress(40)

                    parser = TMDLParserV2(definition_path)
                    metadata = parser.parse_all()

                    st.session_state.metadata = metadata
                    progress.progress(80)
                else:
                    raise Exception("Solo se soportan archivos PBIP (no PBIX)")

                st.session_state.analysis_done = True
                progress.progress(100)

            # Show summary
            if isinstance(metadata, dict):
                tables = metadata.get('tables', [])
                # Count tables excluding LocalDateTable
                num_tables = 0
                num_measures = 0
                for t in tables:
                    # Get table name (works for both dict and object)
                    if isinstance(t, dict):
                        table_name = t.get('name', '')
                        measures = t.get('measures', [])
                    else:
                        table_name = getattr(t, 'name', '')
                        measures = getattr(t, 'measures', [])

                    # Skip LocalDateTable
                    if 'LocalDateTable' not in table_name:
                        num_tables += 1

                    # Count measures
                    num_measures += len(measures)

                num_relationships = len(metadata.get('relationships', []))
                num_roles = len(metadata.get('roles', []))

            st.markdown(f"""
            <div class="success-box">
                <h3>✅ ¡Análisis Completado!</h3>
                <p><strong>Datos extraídos exitosamente:</strong></p>
                <ul>
                    <li>📊 <strong>{num_tables}</strong> tablas</li>
                    <li>🔗 <strong>{num_relationships}</strong> relaciones</li>
                    <li>📐 <strong>{num_measures}</strong> medidas DAX</li>
                    <li>🔒 <strong>{num_roles}</strong> roles RLS</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


        except Exception as e:
            st.error(f"❌ Error al analizar el archivo: {str(e)}")
            with st.expander("🔍 Detalles técnicos"):
                st.code(traceback.format_exc())

    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3: Generate
if st.session_state.analysis_done and st.session_state.metadata:
    st.markdown('<div class="step-card active">', unsafe_allow_html=True)
    st.markdown("### 📄 Paso 3: Generar Documento Word")

    st.markdown("""
    <div class="info-box">
        <strong>📄 Documento corporativo YPF</strong><br>
        El documento se generará con el template oficial, completando automáticamente todas las secciones
        con los datos reales extraídos del PBIP.
    </div>
    """, unsafe_allow_html=True)

    if st.button("📄 Generar Documento Word", use_container_width=True, type="primary"):
        try:
            with st.spinner("Generando documentación..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(step, message):
                    progress_bar.progress(step)
                    status_text.write(f"[{step}%] {message}")

                # Find template
                template_path = Path(r"C:\Users\SE46958\1 - Claude - Proyecto viz\Plantilla Documentacion Técnica Funcional Power Bi.docx")

                if not template_path.exists():
                    template_path = Path("../Plantilla Documentacion Técnica Funcional Power Bi.docx")

                if not template_path.exists():
                    st.error("❌ No se encontró el template corporativo")
                    st.stop()

                builder = DocxBuilderV3(str(template_path))

                output_path = builder.build(
                    metadata=st.session_state.metadata,
                    user_inputs=st.session_state.user_inputs,
                    er_diagram_path=None,
                    progress_callback=update_progress
                )

                progress_bar.progress(100)
                status_text.empty()

            st.success(f"✅ ¡Documento generado exitosamente!")
            st.markdown(f"**Ubicación:** `{output_path}`")

            # Download button
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Descargar Documento",
                    data=f,
                    file_name=Path(output_path).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )


        except Exception as e:
            st.error(f"❌ Error al generar el documento: {e}")
            with st.expander("Detalles técnicos"):
                st.code(traceback.format_exc())

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Generador de Documentación Power BI v4.0</strong></p>
    <p>YPF S.A. | IT Analytics Team | 2026</p>
</div>
""", unsafe_allow_html=True)
