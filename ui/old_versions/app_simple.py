"""
Power BI Documentation Generator v3.0 - Simplified Version
Upload → Generate → Download
"""

import streamlit as st
import sys
from pathlib import Path
import traceback

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.parsers import create_parser
from utils.file_helper import save_uploaded_file
from core.validators import ModelValidator, RelationshipValidator
from core.analyzers import ComplexityAnalyzer
from visualization import ERDiagramGenerator
from document_generation import DocxBuilder

# Page config
st.set_page_config(
    page_title="Power BI Documentation Generator",
    page_icon="📊",
    layout="centered"
)

# Initialize session state
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'validation_report' not in st.session_state:
    st.session_state.validation_report = None
if 'er_diagram' not in st.session_state:
    st.session_state.er_diagram = None

# Simple CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    h1, h2, h3, h4, h5, h6, p, li, span, div, label {
        color: white !important;
    }
    .stTextInput label, .stFileUploader label, .stTextArea label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 📊 Power BI Documentation Generator")
st.markdown("### Sube tu archivo PBIX o PBIP y genera la documentación automáticamente")
st.markdown("---")

# Helper function
def clean_path(path_str: str) -> str:
    if not path_str:
        return ""
    return path_str.strip().strip('"').strip("'").strip()

# Step 1: File Selection
st.markdown("## 📁 Paso 1: Selecciona tu archivo")

format_type = st.radio(
    "Tipo de archivo:",
    ["PBIX (.pbix)", "PBIP (carpeta)"],
    horizontal=True
)

file_path = None

if format_type == "PBIX (.pbix)":
    uploaded_file = st.file_uploader(
        "Arrastra o selecciona tu archivo .pbix",
        type=['pbix']
    )

    if uploaded_file:
        st.success(f"✅ Archivo cargado: **{uploaded_file.name}**")
        file_path = save_uploaded_file(uploaded_file)
        st.session_state.file_path = file_path

else:  # PBIP
    pbip_input = st.text_input(
        "Ruta del proyecto PBIP:",
        placeholder=r"C:\Users\...\MyProject.pbip",
        help="Pega la ruta completa (las comillas se limpiarán automáticamente)"
    )

    if pbip_input:
        cleaned_path = clean_path(pbip_input)
        path_obj = Path(cleaned_path)

        if path_obj.exists():
            st.success(f"✅ Ruta validada: **{path_obj.name}**")
            file_path = path_obj
            st.session_state.file_path = file_path
        else:
            st.error(f"❌ Ruta no encontrada: `{cleaned_path}`")

st.markdown("---")

# Step 2: Generate Button
st.markdown("## 📄 Paso 2: Genera el documento")

if file_path:
    # Metadata inputs (simplified)
    col1, col2 = st.columns(2)
    with col1:
        report_name = st.text_input(
            "Nombre del Reporte *",
            value=st.session_state.file_path.stem if st.session_state.file_path else ""
        )
    with col2:
        author = st.text_input("Autor *", value="YPF IT Team")

    if st.button("🚀 **GENERAR DOCUMENTO**", type="primary", use_container_width=True):
        if not report_name or not author:
            st.error("❌ Por favor completa todos los campos obligatorios (*)")
        else:
            try:
                # Progress container
                progress_container = st.container()
                with progress_container:
                    progress = st.progress(0, text="Iniciando análisis...")

                    # Parse file
                    progress.progress(10, text="📖 Leyendo archivo...")
                    parser = create_parser(str(st.session_state.file_path))

                    progress.progress(30, text="🔍 Extrayendo metadatos...")
                    metadata = parser.parse()
                    st.session_state.metadata = metadata

                    # Validation
                    progress.progress(40, text="✅ Validando modelo...")
                    model_validator = ModelValidator(metadata.data_model)
                    model_report = model_validator.validate_all()

                    relationship_validator = RelationshipValidator(metadata.data_model)
                    rel_report = relationship_validator.validate_all()

                    combined_report = model_report
                    for issue in rel_report.issues:
                        combined_report.add_issue(issue)
                    combined_report.quality_score = (model_report.quality_score + rel_report.quality_score) / 2
                    st.session_state.validation_report = combined_report

                    # DAX analysis
                    progress.progress(50, text="📐 Analizando DAX...")
                    if metadata.data_model.measures:
                        complexity_analyzer = ComplexityAnalyzer(metadata.data_model.measures)
                        complexity_report = complexity_analyzer.analyze_all()

                    # ER Diagram (usando spring siempre, no requiere scipy)
                    progress.progress(60, text="🎨 Generando diagrama ER...")
                    try:
                        er_gen = ERDiagramGenerator(metadata.data_model)
                        # Pre-generate con spring layout (no requiere scipy)
                        er_gen.generate_plotly_figure(layout_algorithm='spring')
                        st.session_state.er_diagram = er_gen
                    except Exception as e:
                        st.warning(f"⚠️ Diagrama ER omitido: {str(e)}")
                        st.session_state.er_diagram = None

                    # Generate Document
                    progress.progress(70, text="📝 Generando documento Word...")

                    template_path = r"C:\Users\SE46958\1 - Claude - Proyecto viz\Plantilla Documentacion Técnica Funcional Power Bi.docx"

                    # Check if template exists
                    if not Path(template_path).exists():
                        st.warning(f"⚠️ Plantilla no encontrada en: {template_path}")
                        st.info("Usando documento en blanco...")
                        template_path = "templates/plantilla_corporativa_ypf.docx"

                    builder = DocxBuilder(template_path)

                    def update_progress(step, message):
                        progress.progress(step, text=message)

                    output_path = builder.build(
                        metadata=metadata,
                        validation_report=combined_report,
                        er_diagram_generator=st.session_state.er_diagram,
                        progress_callback=update_progress
                    )

                    progress.progress(100, text="✅ ¡Documento generado!")

                # Success message
                st.success("✅ **¡Documento generado exitosamente!**")
                st.markdown(f"**Archivo generado:** `{Path(output_path).name}`")

                # Download button
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ **DESCARGAR DOCUMENTO**",
                        data=f,
                        file_name=Path(output_path).name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary",
                        use_container_width=True
                    )

                st.balloons()

            except Exception as e:
                st.error(f"❌ **Error generando documento**")
                st.error(f"**Detalle:** {str(e)}")
                with st.expander("🔍 Detalles técnicos"):
                    st.code(traceback.format_exc())

else:
    st.info("👆 Por favor selecciona un archivo primero")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.4); padding: 1rem 0;">
    <p style="margin: 0;">Power BI Documentation Generator v3.0 | YPF S.A. © 2026</p>
</div>
""", unsafe_allow_html=True)
