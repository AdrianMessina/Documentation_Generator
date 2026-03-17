"""
Power BI Documentation Generator - VERSIÓN ULTRA SIMPLIFICADA
Interfaz minimalista con PBIP automático + Upload de imágenes
"""

import streamlit as st
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.parsers import create_parser, FormatDetector, PowerBIFormat
from core.parsers.tmdl_parser_v2 import TMDLParserV2
from utils.image_helper import save_uploaded_images, cleanup_temp_images
from visualization import ERDiagramGenerator
from document_generation.docx_builder_v3 import DocxBuilderV3

# Initialize logger
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Power BI Doc Generator",
    page_icon="📊",
    layout="centered"
)

# Simple CSS
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title"><h1>📊 Generador de Documentación</h1><p>Power BI - Versión Simplificada</p></div>', unsafe_allow_html=True)

# Auto-detect PBIP file
pbip_folder = project_root / "PBI test"
pbip_files = list(pbip_folder.glob("*.pbip"))

if not pbip_files:
    st.error("❌ No se encontró archivo PBIP en la carpeta 'PBI test'")
    st.info("📁 Coloca tu archivo .pbip en: " + str(pbip_folder))
    st.stop()

pbip_path = pbip_files[0]
st.success(f"✅ Archivo detectado: **{pbip_path.stem}**")

st.markdown("---")

# Simple form
with st.form("ultra_simple_form"):

    st.markdown("### 👤 Información Básica")

    col1, col2 = st.columns(2)
    with col1:
        version = st.text_input("Versión", value="1.0")
    with col2:
        autor = st.text_input("Autor", value="YPF IT Analytics Team")

    st.markdown("---")

    # Image uploads - PRINCIPALES
    st.markdown("### 📸 Agregar Imágenes al Documento")

    st.info("💡 **Recomendación**: Sube capturas de pantalla de tu reporte para un documento más completo")

    # ER Model image
    st.markdown("#### 📊 Modelo de Relaciones (ER Diagram)")
    er_image = st.file_uploader(
        "Sube una captura del diagrama de relaciones",
        type=['png', 'jpg', 'jpeg'],
        key="er_upload",
        help="Captura del Model View en Power BI Desktop"
    )

    if er_image:
        st.success(f"✅ Imagen cargada: {er_image.name}")

    st.markdown("#### 📈 Visualizaciones del Reporte")
    viz_images = st.file_uploader(
        "Sube capturas de tus dashboards (máximo 10 imágenes)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="viz_upload",
        help="Capturas del Report View - páginas principales"
    )

    if viz_images:
        count = min(len(viz_images), 10)
        st.success(f"✅ {count} imagen(es) cargada(s)")
        if len(viz_images) > 10:
            st.warning("⚠️ Solo se usarán las primeras 10 imágenes")

    st.markdown("---")

    # Generate button
    generate = st.form_submit_button(
        "🚀 GENERAR DOCUMENTO WORD",
        use_container_width=True,
        type="primary"
    )

# Generation logic
if generate:
    try:
        # Progress indicators
        progress = st.progress(0)
        status = st.empty()

        # Step 1: Process images
        status.write("📸 Procesando imágenes...")
        progress.progress(10)

        er_image_path = None
        viz_image_paths = []

        if er_image:
            saved_er = save_uploaded_images(er_image, prefix="er_model")
            if saved_er:
                er_image_path = saved_er[0]

        if viz_images:
            viz_images_limited = viz_images[:10]
            viz_image_paths = save_uploaded_images(viz_images_limited, prefix="viz")

        # Step 2: Parse PBIP
        status.write("📖 Leyendo archivo Power BI...")
        progress.progress(25)

        format_detector = FormatDetector()
        detected_format = format_detector.detect(str(pbip_path))

        if detected_format == PowerBIFormat.PBIP:
            parser = TMDLParserV2()
            metadata = parser.parse_from_path(str(pbip_path))
        else:
            parser = create_parser(str(pbip_path))
            metadata = parser.parse()

        # Step 3: Generate ER diagram (auto)
        status.write("🎨 Generando diagrama de relaciones...")
        progress.progress(50)

        er_diagram_path = None
        try:
            er_generator = ERDiagramGenerator()
            er_diagram_path = er_generator.generate_from_metadata(
                metadata,
                output_dir=str(project_root / "output")
            )
        except Exception as e:
            logger.warning(f"Could not generate ER diagram: {e}")

        # Step 4: Build Word document
        status.write("📄 Construyendo documento Word...")
        progress.progress(70)

        # Minimal user inputs
        user_inputs = {
            'version': version,
            'autor': autor,
            'observaciones': 'Documentación técnica generada automáticamente',
            'objetivo': None,  # Se genera automáticamente
            'alcance': None,
            'administrador': None,
            'solicitante': None,
            'frecuencia': 'No especificada'
        }

        # Find template
        template_path = project_root.parent / "Plantilla Documentacion Técnica Funcional Power Bi.docx"
        if not template_path.exists():
            template_path = project_root / "templates" / "plantilla_corporativa_ypf.docx"

        if not template_path.exists():
            st.error("❌ Template no encontrado. Colócalo en la carpeta raíz o en templates/")
            st.stop()

        # Build
        def progress_callback(step, message):
            progress.progress(step)
            status.write(f"[{step}%] {message}")

        builder = DocxBuilderV3(str(template_path))
        output_path = builder.build(
            metadata=metadata,
            user_inputs=user_inputs,
            er_diagram_path=er_diagram_path,
            er_image_path=er_image_path,
            visualization_images=viz_image_paths,
            progress_callback=progress_callback
        )

        progress.progress(100)
        status.empty()

        # Success!
        st.success("✅ ¡Documento generado exitosamente!")

        # Show summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Documento", "Completo")
        with col2:
            img_count = (1 if er_image_path else 0) + len(viz_image_paths)
            st.metric("📸 Imágenes", f"{img_count}")
        with col3:
            st.metric("🎯 Objetivo", "Auto-generado")

        # Download button
        st.markdown("---")
        with open(output_path, 'rb') as f:
            st.download_button(
                label="⬇️ DESCARGAR DOCUMENTO WORD",
                data=f,
                file_name=Path(output_path).name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        st.balloons()

        # Cleanup
        if er_image_path or viz_image_paths:
            try:
                all_temp_images = []
                if er_image_path:
                    all_temp_images.append(er_image_path)
                if viz_image_paths:
                    all_temp_images.extend(viz_image_paths)
                cleanup_temp_images(all_temp_images)
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")

    except Exception as e:
        st.error(f"❌ Error al generar el documento: {str(e)}")
        with st.expander("🔍 Ver detalles del error"):
            import traceback
            st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.caption("📊 Power BI Documentation Generator v3.1 | YPF IT Analytics Team")
