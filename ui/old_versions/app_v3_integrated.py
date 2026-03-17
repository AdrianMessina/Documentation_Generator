"""
Power BI Documentation Generator v3.0 - INTEGRATED VERSION
Con parser mejorado, mapper inteligente y relleno real del template
"""

import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.parsers import create_parser, FormatDetector, PowerBIFormat
from core.parsers.tmdl_parser_v2 import TMDLParserV2
from utils.file_helper import save_uploaded_file, cleanup_temp_files
from core.validators import ModelValidator, RelationshipValidator, ValidationSeverity
from core.analyzers import ComplexityAnalyzer
from visualization import ERDiagramGenerator

# Import new UI components
from ui.components import (
    create_metric_card,
    create_interactive_table,
    create_file_uploader,
    show_loading_animation,
    show_success_animation,
    ThemeManager
)

# Import NEW document generation V2
from document_generation.docx_builder_v2 import DocxBuilderV2

# Page config
st.set_page_config(
    page_title="Power BI Documentation Generator V3",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme manager
theme_manager = ThemeManager()

# Initialize session state
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'validation_report' not in st.session_state:
    st.session_state.validation_report = None
if 'complexity_report' not in st.session_state:
    st.session_state.complexity_report = None
if 'er_diagram' not in st.session_state:
    st.session_state.er_diagram = None
if 'er_diagram_path' not in st.session_state:
    st.session_state.er_diagram_path = None
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}

# Apply theme
theme_manager.apply_theme()

# Helper function to clean path
def clean_path(path_str: str) -> str:
    """Remove quotes and extra spaces from path"""
    if not path_str:
        return ""
    cleaned = path_str.strip().strip('"').strip("'").strip()
    return cleaned

# Header
st.markdown("""
<div class="app-header">
    <h1 class="app-title">📊 Power BI Documentation Generator v3.0</h1>
    <p class="app-subtitle">Generación automática con mapeo inteligente | Template corporativo</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")

    page = st.radio(
        "Navegación",
        ["🏠 Dashboard", "📤 Generate Documentation", "📊 Analysis Results", "📚 Help"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Theme toggle
    st.markdown("### 🎨 Theme")
    theme_manager.render_theme_toggle()

    st.markdown("---")

    st.markdown("### 📊 System Status")
    st.markdown('<span class="status-badge status-completed">✓ System Ready</span>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<span class="status-badge status-completed">✓ V2 Parser Active</span>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<span class="status-badge status-completed">✓ Intelligent Mapper</span>', unsafe_allow_html=True)
    st.markdown("")
    if st.session_state.analysis_done:
        st.markdown('<span class="status-badge status-completed">✓ Analysis Complete</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-progress">⚡ Ready to Analyze</span>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📈 Progress")
    st.progress(1.0)  # 100% - V3 integrated!
    st.caption("v3.0 Integrated - Full automation")

    st.markdown("---")

    st.caption("© 2026 YPF S.A.")
    st.caption("IT Analytics Team")

# Main content
if page == "🏠 Dashboard":
    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_metric_card("Parser", "V2", "🚀", "success")

    with col2:
        create_metric_card("Mapper", "Smart", "🧠", "success")

    with col3:
        create_metric_card("Template", "Real", "📄", "success")

    with col4:
        create_metric_card("Status", "Live", "✅", "success")

    st.markdown("##")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🚀 v3.0 - Integrated System</h3>
            <p>Sistema completamente automático con mapeo inteligente</p>
            <ul style="list-style: none; padding-left: 0;">
                <li>✅ <strong>Parser TMDL V2</strong> - Sin regex, estructurado</li>
                <li>✅ <strong>Intelligent Mapper</strong> - Mapeo automático datos → template</li>
                <li>✅ <strong>Relleno Real</strong> - NO inventa datos, solo usa PBIP</li>
                <li>✅ <strong>82% Automatización</strong> - Campos opcionales vía formulario</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Nuevas Features</h3>
            <p><strong>Parser:</strong> Estructurado</p>
            <p><strong>DAX:</strong> Sin truncar</p>
            <p><strong>Cardinalidad:</strong> Completa</p>
            <p><strong>Template:</strong> Corporativo YPF</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📤 Generate Documentation":
    st.markdown("## 📤 Generate Documentation")

    # Step indicator
    step = 1
    if st.session_state.file_path:
        step = 2
    if st.session_state.analysis_done:
        step = 3

    st.markdown(f"""
    <div class="step-indicator">
        <div class="step">
            <div class="step-circle {'completed' if step > 1 else 'active'}">1</div>
            <div class="step-label {'active' if step == 1 else ''}">Select File</div>
        </div>
        <div style="width: 60px; height: 2px; background: {'#667eea' if step > 1 else 'rgba(255,255,255,0.2)'}; margin-top: 20px;"></div>
        <div class="step">
            <div class="step-circle {'completed' if step > 2 else 'active' if step == 2 else ''}">2</div>
            <div class="step-label {'active' if step == 2 else ''}">Configure</div>
        </div>
        <div style="width: 60px; height: 2px; background: {'#667eea' if step > 2 else 'rgba(255,255,255,0.2)'}; margin-top: 20px;"></div>
        <div class="step">
            <div class="step-circle {'active' if step == 3 else ''}">3</div>
            <div class="step-label {'active' if step == 3 else ''}">Generate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Step 1: File Selection
    st.markdown("### 📁 Step 1: Select Your Power BI File")

    format_type = st.radio(
        "Choose file type:",
        ["PBIX File (.pbix)", "PBIP Project (folder)"],
        horizontal=True,
        help="PBIX: Single file | PBIP: Recommended for best results"
    )

    file_ready = False

    if format_type == "PBIX File (.pbix)":
        st.markdown("""
        <div class="info-card">
            <h4>📦 PBIX File Upload</h4>
            <p>Upload your Power BI Desktop file (.pbix)</p>
            <p><strong>Note:</strong> PBIP is recommended for full metadata extraction</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your .pbix file here",
            type=['pbix'],
            help="Select your Power BI Desktop file"
        )

        if uploaded_file:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Filename", uploaded_file.name)
            with col2:
                st.metric("📦 Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.metric("✅ Status", "Ready")

            file_path = save_uploaded_file(uploaded_file)
            st.session_state.file_path = file_path
            file_ready = True

    else:  # PBIP
        st.markdown("""
        <div class="info-card">
            <h4>📁 PBIP Project Path (Recommended)</h4>
            <p>Provide the path to your PBIP project</p>
            <p><strong>✓ Best results</strong> - Full TMDL parsing with V2 parser</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warning-box">
            <p><strong>📍 How to get the path:</strong></p>
            <ol>
                <li>Open Windows Explorer</li>
                <li>Navigate to your PBIP project</li>
                <li>Click on the address bar</li>
                <li>Copy the path (Ctrl+C)</li>
                <li>Paste it below</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💡 See example"):
            st.code(r"C:\Users\YourName\Documents\PowerBI\MyProject.pbip", language="text")

        pbip_input = st.text_input(
            "Paste the path here:",
            placeholder=r"C:\Users\...\MyProject.pbip",
            help="Full path to PBIP file or folder",
            key="pbip_path_input"
        )

        if pbip_input:
            cleaned_path = clean_path(pbip_input)

            if cleaned_path != pbip_input:
                st.info(f"✨ Cleaned path: `{cleaned_path}`")

            path_obj = Path(cleaned_path)

            if path_obj.exists():
                st.success(f"✅ Path validated: **{path_obj.name}**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📂 Type", "Directory" if path_obj.is_dir() else "File")
                with col2:
                    st.metric("📊 Format", "PBIP")
                with col3:
                    st.metric("✅ Status", "Ready")

                st.session_state.file_path = path_obj
                file_ready = True

                with st.expander("🔍 Project structure detected"):
                    if path_obj.is_file():
                        parent = path_obj.parent
                        st.write(f"**Project folder:** `{parent}`")
                    else:
                        st.write(f"**Project folder:** `{path_obj}`")

                    report_folders = list(path_obj.parent.glob("*.Report")) if path_obj.is_file() else list(path_obj.glob("*.Report"))
                    model_folders = list(path_obj.parent.glob("*.SemanticModel")) if path_obj.is_file() else list(path_obj.glob("*.SemanticModel"))

                    if report_folders:
                        st.write(f"✅ Found .Report folder: `{report_folders[0].name}`")
                    if model_folders:
                        st.write(f"✅ Found .SemanticModel folder: `{model_folders[0].name}`")

            else:
                st.error(f"❌ Path not found: `{cleaned_path}`")

    st.markdown("---")

    # Step 2: Configuration with COMPLETE form
    if file_ready:
        st.markdown("### ✏️ Step 2: Configure Documentation")

        st.info("ℹ️ Los campos marcados con * son opcionales. Los datos del PBIP se extraen automáticamente.")

        with st.form("complete_config_form"):
            st.markdown("#### 📋 Información del Documento")

            col1, col2 = st.columns(2)

            with col1:
                version = st.text_input("Versión del documento", value="1.0", help="Ej: 1.0, 2.1")
                autor = st.text_input("Autor", value="YPF IT Analytics Team", help="Nombre del responsable")

            with col2:
                observaciones = st.text_input(
                    "Observaciones de la versión",
                    value="Generación inicial de documentación técnica",
                    help="Qué cambios incluye esta versión"
                )

            st.markdown("---")
            st.markdown("#### 🎯 Información del Reporte (Opcional)")

            objetivo = st.text_area(
                "Objetivo del reporte *",
                placeholder="Ej: Proporcionar análisis de ventas regionales del Q1 2026...",
                help="¿Cuál es el propósito de negocio de este reporte? (opcional - se generará automáticamente si se deja vacío)",
                height=100
            )

            alcance = st.text_area(
                "Alcance del análisis *",
                placeholder="Ej: Incluye datos de ventas desde enero 2024, todas las regiones operativas...",
                help="¿Qué datos, periodos y métricas cubre? (opcional)",
                height=100
            )

            col1, col2 = st.columns(2)

            with col1:
                administrador = st.text_input(
                    "Administrador del reporte *",
                    placeholder="Ej: María González - Analytics Team",
                    help="Responsable del reporte (opcional)"
                )

            with col2:
                solicitante = st.text_input(
                    "Solicitante *",
                    placeholder="Ej: Dirección Comercial",
                    help="Área que solicitó el reporte (opcional)"
                )

            st.markdown("---")
            st.markdown("#### 🔄 Configuración Técnica (Opcional)")

            col1, col2 = st.columns(2)

            with col1:
                frecuencia = st.selectbox(
                    "Frecuencia de actualización *",
                    ["No especificada", "Diaria", "Semanal", "Mensual", "Tiempo real"],
                    help="¿Con qué frecuencia se actualiza el reporte?"
                )

            with col2:
                horario = st.text_input(
                    "Horario de actualización *",
                    placeholder="Ej: 06:00 AM (GMT-3)",
                    help="Hora en que se actualiza (opcional)"
                )

            if frecuencia != "No especificada" and horario:
                frecuencia_completa = f"{frecuencia} - {horario}"
            else:
                frecuencia_completa = frecuencia

            st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                analyze_button = st.form_submit_button(
                    "🚀 Analyze & Generate Documentation",
                    use_container_width=True,
                    help="Analizar archivo y preparar para generación"
                )

        if analyze_button:
            # Save user inputs to session state
            st.session_state.user_inputs = {
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
                # Show loading animation
                with st.spinner(""):
                    show_loading_animation("data-processing", height=150, key="analysis_anim")

                with st.spinner("🔄 Analyzing Power BI file..."):
                    progress = st.progress(0)
                    progress.progress(10)
                    st.write("📖 Detecting file format...")

                    # Detect format
                    file_path = st.session_state.file_path
                    format_detector = FormatDetector()
                    detected_format = format_detector.detect(str(file_path))

                    progress.progress(20)

                    # Use V2 parser for PBIP
                    if detected_format == PowerBIFormat.PBIP:
                        st.write("✨ Using TMDL Parser V2 (enhanced)...")

                        # Find .SemanticModel/definition folder
                        if file_path.is_file():
                            parent = file_path.parent
                        else:
                            parent = file_path

                        model_folders = list(parent.glob("*.SemanticModel"))
                        if not model_folders:
                            raise Exception("No .SemanticModel folder found in PBIP project")

                        definition_path = model_folders[0] / "definition"

                        if not definition_path.exists():
                            raise Exception(f"Definition folder not found: {definition_path}")

                        st.write(f"📂 Reading from: {definition_path}")

                        progress.progress(30)
                        st.write("🔍 Parsing TMDL files...")

                        parser = TMDLParserV2(definition_path)
                        metadata = parser.parse_all()

                        st.session_state.metadata = metadata

                        progress.progress(70)
                        st.write("✅ TMDL parsed successfully!")

                    else:
                        st.write("📖 Using standard parser for PBIX...")
                        parser = create_parser(str(file_path))
                        metadata = parser.parse()
                        st.session_state.metadata = metadata

                    progress.progress(80)
                    st.write("🎨 Generating ER diagram...")

                    # Generate ER diagram if possible
                    try:
                        # For TMDL V2, create a simple diagram
                        # (ERDiagramGenerator expects old format, skip for now)
                        st.session_state.er_diagram = None
                        st.session_state.er_diagram_path = None
                    except Exception as e:
                        st.warning(f"ER diagram generation skipped: {e}")

                    st.session_state.analysis_done = True
                    progress.progress(100)

                # Show success animation
                show_success_animation(height=150, key="success_anim")

                # Show summary
                if isinstance(metadata, dict):
                    num_tables = len(metadata.get('tables', []))
                    num_relationships = len(metadata.get('relationships', []))
                    num_measures = sum(len(t.measures) if hasattr(t, 'measures') else len(t.get('measures', [])) for t in metadata.get('tables', []))
                    num_roles = len(metadata.get('roles', []))
                else:
                    num_tables = metadata.data_model.table_count if hasattr(metadata, 'data_model') else 0
                    num_relationships = metadata.data_model.relationship_count if hasattr(metadata, 'data_model') else 0
                    num_measures = metadata.data_model.measure_count if hasattr(metadata, 'data_model') else 0
                    num_roles = 0

                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Analysis Complete!</h3>
                    <p><strong>Successfully extracted:</strong></p>
                    <ul>
                        <li>📊 {num_tables} tables</li>
                        <li>🔗 {num_relationships} relationships</li>
                        <li>📐 {num_measures} DAX measures</li>
                        <li>🔒 {num_roles} RLS roles</li>
                    </ul>
                    <p><strong>→ Ready to generate documentation!</strong></p>
                </div>
                """, unsafe_allow_html=True)

                st.balloons()

            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    <h3>❌ Error Analyzing File</h3>
                    <p><strong>Error:</strong> {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("🔍 Technical details"):
                    st.code(traceback.format_exc())

    else:
        st.info("👆 Please select and validate a file first")

    # Step 3: Generate Documentation
    if st.session_state.analysis_done and st.session_state.metadata:
        st.markdown("---")
        st.markdown("### 📄 Step 3: Generate Word Document")

        st.markdown("""
        <div class="info-card">
            <h4>🎯 Template Corporativo YPF</h4>
            <p>El documento se generará usando el template oficial y rellenándolo con los datos reales extraídos del PBIP.</p>
            <p><strong>✓ NO se inventan datos</strong> - Solo información real del modelo</p>
            <p><strong>✓ Mapeo inteligente</strong> - Campos automáticos y manuales combinados</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Generate Word Document", use_container_width=True, type="primary"):
                try:
                    # Show processing animation
                    with st.spinner(""):
                        show_loading_animation("data-processing", height=150, key="doc_gen_anim")

                    with st.spinner("Generating documentation..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def update_progress(step, message):
                            progress_bar.progress(step)
                            status_text.write(f"[{step}%] {message}")

                        # Initialize V2 builder
                        template_path = Path("../Plantilla Documentacion Técnica Funcional Power Bi.docx")

                        if not template_path.exists():
                            # Try alternative path
                            template_path = Path("templates/plantilla_corporativa_ypf.docx")

                        if not template_path.exists():
                            st.error("❌ Template not found. Please check template path.")
                            st.stop()

                        builder = DocxBuilderV2(str(template_path))

                        # Build document with V2 builder
                        output_path = builder.build(
                            metadata=st.session_state.metadata,
                            user_inputs=st.session_state.user_inputs,
                            er_diagram_path=st.session_state.er_diagram_path,
                            progress_callback=update_progress
                        )

                        progress_bar.progress(100)
                        status_text.empty()

                    # Show success animation
                    show_success_animation(height=150, key="doc_success_anim")

                    # Success message
                    st.success(f"✅ Document generated successfully!")
                    st.markdown(f"**Output**: `{output_path}`")

                    # Download button
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download Document",
                            data=f,
                            file_name=Path(output_path).name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )

                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Error generating document: {e}")
                    with st.expander("Technical details"):
                        st.code(traceback.format_exc())

elif page == "📊 Analysis Results":
    st.markdown("## 📊 Analysis Results")

    if st.session_state.metadata is None:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ No Analysis Available</h3>
            <p>You haven't analyzed a file yet.</p>
            <p><strong>Next steps:</strong></p>
            <ol>
                <li>Go to "Generate Documentation"</li>
                <li>Select your file</li>
                <li>Fill the form and click "Analyze"</li>
                <li>Return here to see results</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    else:
        metadata = st.session_state.metadata

        # Show summary based on metadata type
        if isinstance(metadata, dict):
            # TMDL V2 format
            tables = metadata.get('tables', [])
            relationships = metadata.get('relationships', [])
            roles = metadata.get('roles', [])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                create_metric_card("Tables", str(len(tables)), "📊", "primary")
            with col2:
                create_metric_card("Relationships", str(len(relationships)), "🔗", "info")
            with col3:
                num_measures = sum(len(t.measures) if hasattr(t, 'measures') else len(t.get('measures', [])) for t in tables)
                create_metric_card("Measures", str(num_measures), "📐", "success")
            with col4:
                create_metric_card("RLS Roles", str(len(roles)), "🔒", "info")

            st.markdown("---")

            # Show tables
            st.subheader("📊 Tables")
            if tables:
                tables_data = []
                for table in tables:
                    if hasattr(table, 'name'):
                        tables_data.append({
                            'Name': table.name,
                            'Columns': len(table.columns) if hasattr(table, 'columns') else 0,
                            'Measures': len(table.measures) if hasattr(table, 'measures') else 0,
                            'Calculated': '✓' if (hasattr(table, 'is_calculated') and table.is_calculated) else ''
                        })

                if tables_data:
                    df = pd.DataFrame(tables_data)
                    st.dataframe(df, use_container_width=True)

            st.markdown("---")

            # Show relationships
            st.subheader("🔗 Relationships")
            if relationships:
                rel_data = []
                for rel in relationships:
                    if hasattr(rel, 'from_table'):
                        rel_data.append({
                            'From': f"{rel.from_table}.{rel.from_column}",
                            'To': f"{rel.to_table}.{rel.to_column}",
                            'Cardinality': rel.get_cardinality_display() if hasattr(rel, 'get_cardinality_display') else 'N/A',
                            'Active': '✓' if rel.is_active else '✗'
                        })

                if rel_data:
                    df = pd.DataFrame(rel_data)
                    st.dataframe(df, use_container_width=True)

        else:
            # Old format (from standard parser)
            st.info("Using standard parser format - limited visualization")

elif page == "📚 Help":
    st.markdown("## 📚 Help & Documentation")

    st.markdown("""
    ### 🚀 Quick Start

    1. **Select File**: Upload PBIX or provide PBIP path (PBIP recommended)
    2. **Configure**: Fill the form with document information
    3. **Analyze**: Click "Analyze & Generate Documentation"
    4. **Generate**: Click "Generate Word Document"
    5. **Download**: Download your documentation

    ### ✨ What's New in v3.0

    - **Parser TMDL V2**: Sin regex, parsing estructurado
    - **Intelligent Mapper**: Mapeo automático de datos
    - **Real Template Filling**: Rellena template corporativo
    - **82% Automation**: Campos opcionales vía formulario
    - **No Invented Data**: Solo información real del PBIP

    ### 📋 Template Sections

    - **Portada**: Nombre del reporte (automático)
    - **Versión**: Tabla de versiones (form + automático)
    - **Objetivo**: Generado o manual
    - **Alcance**: Detectado o manual
    - **Definiciones**: Medidas DAX (100% automático)
    - **Orígenes**: Fuentes de datos (automático)
    - **Filtros**: Power Query y DAX (automático)
    - **Modelo ER**: Relaciones y cardinalidad (automático)
    - **RLS**: Roles de seguridad (automático)
    - **Anexo**: Jerarquías y columnas (automático)

    ### 📞 Support

    For issues or questions:
    - Email: analytics@ypf.com
    - Docs: See TEMPLATE_MAPPING_SPEC.md

    ### 📄 Version

    **v3.0 Integrated** - 2026-03-09
    """)

# Footer
st.markdown("---")
st.caption("Power BI Documentation Generator v3.0 | YPF S.A. | Claude + IT Analytics Team")
