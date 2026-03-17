"""
Generador de Documentación Power BI v3.0
Interfaz Profesional en Español - UX Optimizada con Patrones Modernos
"""

import streamlit as st
import sys
from pathlib import Path
import traceback
from typing import Optional

# Configurar ruta del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.parsers import create_parser
from utils.file_helper import save_uploaded_file
from core.validators import ModelValidator, RelationshipValidator
from core.analyzers import ComplexityAnalyzer
from visualization import ERDiagramGenerator
from document_generation import DocxBuilder

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Generador de Documentación Power BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== INICIALIZAR ESTADO ====================
def init_session_state():
    """Inicializa el estado de la sesión con valores por defecto"""
    defaults = {
        'metadata': None,
        'validation_report': None,
        'er_diagram': None,
        'file_path': None,
        'paso_actual': 1,
        'error_message': None,
        'processing': False,
        'documento_generado': None,
        'show_success': False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== ESTILOS CSS PROFESIONALES ====================
st.markdown("""
<style>
    /* Base */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* Contenedor principal */
    .main .block-container {
        max-width: 1000px;
        padding: 2rem 1rem;
    }

    /* Card principal con glassmorphism */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 24px 48px rgba(0,0,0,0.2);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* Header mejorado */
    .header-section {
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }

    .header-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }

    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 1.2rem;
        color: #6c757d;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Indicador de pasos mejorado */
    .steps-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 3rem 0;
        position: relative;
        padding: 2rem 0;
    }

    .step {
        flex: 0 0 auto;
        text-align: center;
        position: relative;
        padding: 0 2rem;
    }

    .step-number {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: #e9ecef;
        color: #adb5bd;
        font-weight: 700;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
        border: 4px solid #fff;
    }

    .step.active .step-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transform: scale(1.1);
    }

    .step.completed .step-number {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }

    .step-label {
        font-size: 1rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .step.active .step-label {
        color: #667eea;
        font-weight: 700;
    }

    .step.completed .step-label {
        color: #10b981;
        font-weight: 600;
    }

    /* Conectores entre pasos */
    .step-connector {
        width: 80px;
        height: 4px;
        background: #e9ecef;
        position: relative;
        top: -2rem;
        border-radius: 2px;
    }

    .step-connector.active {
        background: linear-gradient(90deg, #10b981 0%, #667eea 100%);
    }

    /* Secciones de contenido */
    .content-section {
        margin: 2.5rem 0;
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .section-icon {
        font-size: 1.8rem;
    }

    /* Botones mejorados */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1.2rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    .stButton>button:disabled {
        background: #e9ecef;
        color: #adb5bd;
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
    }

    /* File uploader mejorado */
    [data-testid="stFileUploader"] {
        border: 3px dashed #667eea;
        border-radius: 16px;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        transform: scale(1.01);
    }

    /* Inputs mejorados */
    .stTextInput input, .stSelectbox select {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Radio buttons mejorados */
    .stRadio > div {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        gap: 1rem;
    }

    .stRadio > div > label {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .stRadio > div > label:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    }

    /* Mensajes de estado mejorados */
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        animation: slideInUp 0.5s ease;
    }

    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .success-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .success-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #065f46;
        margin-bottom: 0.5rem;
    }

    .success-text {
        color: #047857;
        margin: 0.3rem 0;
    }

    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        display: flex;
        align-items: start;
        gap: 1rem;
    }

    .info-icon {
        font-size: 1.5rem;
        color: #1e40af;
    }

    .info-text {
        color: #1e3a8a;
        line-height: 1.6;
    }

    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .warning-text {
        color: #92400e;
        font-weight: 500;
    }

    .error-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .error-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #991b1b;
        margin-bottom: 0.5rem;
    }

    .error-text {
        color: #b91c1c;
    }

    /* Progress bar personalizada */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 12px;
    }

    .stProgress > div {
        background: #e9ecef;
        border-radius: 10px;
        height: 12px;
    }

    /* Labels mejorados */
    label {
        font-weight: 600;
        color: #374151;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    /* Download button especial */
    .download-section {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
    }

    .download-section .stButton>button {
        background: white;
        color: #059669;
        font-size: 1.3rem;
        padding: 1.5rem 3rem;
    }

    .download-section .stButton>button:hover {
        background: #f0fdf4;
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(255, 255, 255, 0.3);
    }

    /* Divider elegante */
    hr {
        margin: 3rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e9ecef, transparent);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 2px solid #e9ecef;
    }

    .footer-logo {
        font-weight: 700;
        color: #667eea;
    }

    /* Loading overlay */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #6c757d;
    }

    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    .empty-text {
        font-size: 1.1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES AUXILIARES ====================
def limpiar_ruta(ruta: str) -> str:
    """Limpia comillas y espacios de una ruta"""
    if not ruta:
        return ""
    return ruta.strip().strip('"').strip("'").strip()

def mostrar_error(titulo: str, mensaje: str, detalles: Optional[str] = None):
    """Muestra un mensaje de error con diseño profesional"""
    st.markdown(f"""
    <div class="error-box">
        <div class="error-title">❌ {titulo}</div>
        <div class="error-text">{mensaje}</div>
    </div>
    """, unsafe_allow_html=True)

    if detalles:
        with st.expander("🔍 Ver detalles técnicos"):
            st.code(detalles)

def mostrar_exito(titulo: str, detalles: dict):
    """Muestra un mensaje de éxito con diseño profesional"""
    detalles_html = "<br>".join([f"<div class='success-text'><strong>{k}:</strong> {v}</div>"
                                  for k, v in detalles.items()])

    st.markdown(f"""
    <div class="success-box">
        <div class="success-icon">✅</div>
        <div class="success-title">{titulo}</div>
        {detalles_html}
    </div>
    """, unsafe_allow_html=True)

def mostrar_info(texto: str):
    """Muestra un mensaje informativo"""
    st.markdown(f"""
    <div class="info-box">
        <div class="info-icon">💡</div>
        <div class="info-text">{texto}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-card">
    <div class="header-section">
        <span class="header-icon">📊</span>
        <h1 class="header-title">Generador de Documentación</h1>
        <p class="header-subtitle">Power BI • Documentación Técnica Automática • Versión 3.0</p>
    </div>
""", unsafe_allow_html=True)

# ==================== INDICADOR DE PASOS ====================
paso = st.session_state.paso_actual

st.markdown(f"""
<div class="steps-indicator">
    <div class="step {'active' if paso == 1 else 'completed' if paso > 1 else ''}">
        <div class="step-number">1</div>
        <div class="step-label">Seleccionar</div>
    </div>
    <div class="step-connector {'active' if paso > 1 else ''}"></div>
    <div class="step {'active' if paso == 2 else 'completed' if paso > 2 else ''}">
        <div class="step-number">2</div>
        <div class="step-label">Configurar</div>
    </div>
    <div class="step-connector {'active' if paso > 2 else ''}"></div>
    <div class="step {'active' if paso == 3 else ''}">
        <div class="step-number">3</div>
        <div class="step-label">Descargar</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== PASO 1: SELECCIÓN DE ARCHIVO ====================
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title"><span class="section-icon">📁</span> Paso 1: Selecciona tu archivo</h2>', unsafe_allow_html=True)

# ERROR STATE: Mostrar si hubo error previo
if st.session_state.error_message and not st.session_state.processing:
    mostrar_error("Error en el proceso", st.session_state.error_message)
    # Botón para reintentar
    if st.button("🔄 Reintentar", key="retry_button"):
        st.session_state.error_message = None
        st.session_state.paso_actual = 1
        st.rerun()

tipo_archivo = st.radio(
    "Tipo de archivo",
    ["📦 Archivo PBIX", "📂 Proyecto PBIP"],
    horizontal=True,
    label_visibility="collapsed"
)

archivo_seleccionado = None

if tipo_archivo == "📦 Archivo PBIX":
    st.markdown("**Sube tu archivo Power BI Desktop (.pbix)**")
    archivo_subido = st.file_uploader(
        "Arrastra tu archivo aquí o haz clic para buscar",
        type=['pbix'],
        label_visibility="collapsed",
        disabled=st.session_state.processing  # Disable durante procesamiento
    )

    # SUCCESS STATE: Archivo cargado
    if archivo_subido:
        mostrar_exito("Archivo cargado correctamente", {
            "Nombre": archivo_subido.name,
            "Tamaño": f"{archivo_subido.size / 1024:.2f} KB"
        })
        archivo_seleccionado = save_uploaded_file(archivo_subido)
        st.session_state.file_path = archivo_seleccionado

else:  # PBIP
    st.markdown("**Ingresa la ruta de tu proyecto PBIP**")
    mostrar_info("💡 <strong>Tip:</strong> Copia la ruta desde el explorador de Windows (Ctrl+L en la barra de direcciones)")

    ruta_pbip = st.text_input(
        "Ruta del proyecto",
        placeholder=r"C:\Users\TuNombre\Documentos\MiProyecto.pbip",
        label_visibility="collapsed",
        disabled=st.session_state.processing  # Disable durante procesamiento
    )

    # VALIDATION STATE: Verificar ruta
    if ruta_pbip:
        ruta_limpia = limpiar_ruta(ruta_pbip)
        ruta_obj = Path(ruta_limpia)

        if ruta_obj.exists():
            mostrar_exito("Ruta válida", {
                "Proyecto": ruta_obj.name,
                "Ubicación": str(ruta_obj.parent)
            })
            archivo_seleccionado = ruta_obj
            st.session_state.file_path = archivo_seleccionado
        else:
            st.markdown(f"""
            <div class="warning-box">
                <div class="warning-text">⚠️ <strong>Ruta no encontrada:</strong> {ruta_limpia}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== PASO 2: CONFIGURACIÓN Y GENERACIÓN ====================
if archivo_seleccionado and not st.session_state.processing:
    st.session_state.paso_actual = 2

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title"><span class="section-icon">⚙️</span> Paso 2: Configuración del documento</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        nombre_reporte = st.text_input(
            "Nombre del reporte *",
            value=st.session_state.file_path.stem if st.session_state.file_path else "",
            placeholder="Mi Reporte de Power BI"
        )

    with col2:
        autor = st.text_input(
            "Autor *",
            value="Equipo TI YPF",
            placeholder="Nombre del autor"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # BUTTON STATE: Generar documento
    # Disable si faltan campos o está procesando
    puede_generar = bool(nombre_reporte and autor)

    if st.button(
        "🚀 Generar Documento Completo",
        type="primary",
        disabled=not puede_generar or st.session_state.processing,
        key="generate_button"
    ):
        # Validación antes de procesar
        if not nombre_reporte or not autor:
            mostrar_error("Campos incompletos", "Por favor completa todos los campos requeridos (*)")
        else:
            # Iniciar procesamiento
            st.session_state.processing = True
            st.session_state.error_message = None
            st.rerun()

# ==================== PROCESAMIENTO (LOADING STATE) ====================
if st.session_state.processing:
    try:
        # Barra de progreso con mensajes
        barra_progreso = st.progress(0, text="Iniciando análisis...")

        # 1. Análisis
        barra_progreso.progress(10, text="📖 Leyendo archivo Power BI...")
        parser = create_parser(str(st.session_state.file_path))

        barra_progreso.progress(30, text="🔍 Extrayendo metadatos...")
        metadata = parser.parse()
        metadata.report_name = nombre_reporte
        metadata.author = autor
        st.session_state.metadata = metadata

        # 2. Validación
        barra_progreso.progress(45, text="✅ Validando modelo de datos...")
        model_validator = ModelValidator(metadata.data_model)
        model_report = model_validator.validate_all()

        relationship_validator = RelationshipValidator(metadata.data_model)
        rel_report = relationship_validator.validate_all()

        combined_report = model_report
        for issue in rel_report.issues:
            combined_report.add_issue(issue)
        combined_report.quality_score = (model_report.quality_score + rel_report.quality_score) / 2
        st.session_state.validation_report = combined_report

        # 3. Análisis DAX
        barra_progreso.progress(55, text="📐 Analizando medidas DAX...")
        if metadata.data_model.measures:
            complexity_analyzer = ComplexityAnalyzer(metadata.data_model.measures)
            complexity_report = complexity_analyzer.analyze_all()

        # 4. Diagrama ER
        barra_progreso.progress(65, text="🎨 Generando diagrama ER...")
        try:
            er_gen = ERDiagramGenerator(metadata.data_model)
            er_gen.generate_plotly_figure(layout_algorithm='spring', width=1200, height=800)
            st.session_state.er_diagram = er_gen
        except Exception as e:
            st.warning(f"⚠️ Diagrama ER omitido: {str(e)}")
            st.session_state.er_diagram = None

        # 5. Generar documento Word
        barra_progreso.progress(75, text="📝 Generando documento Word...")

        template_path = r"C:\Users\SE46958\1 - Claude - Proyecto viz\Plantilla Documentacion Técnica Funcional Power Bi.docx"

        if not Path(template_path).exists():
            st.warning(f"⚠️ Plantilla no encontrada, usando documento en blanco")
            template_path = "templates/plantilla_corporativa_ypf.docx"

        builder = DocxBuilder(template_path)

        def actualizar_progreso(step, message):
            barra_progreso.progress(step, text=message)

        ruta_salida = builder.build(
            metadata=metadata,
            validation_report=combined_report,
            er_diagram_generator=st.session_state.er_diagram,
            progress_callback=actualizar_progreso
        )

        barra_progreso.progress(100, text="✅ ¡Documento generado!")

        # Guardar resultado y cambiar estado
        st.session_state.documento_generado = ruta_salida
        st.session_state.paso_actual = 3
        st.session_state.processing = False
        st.session_state.show_success = True
        st.balloons()
        st.rerun()

    except Exception as e:
        # ERROR HANDLING: Mostrar error y permitir retry
        st.session_state.processing = False
        st.session_state.error_message = str(e)
        st.session_state.paso_actual = 1
        mostrar_error(
            "Error al generar el documento",
            str(e),
            traceback.format_exc()
        )
        st.rerun()

# ==================== PASO 3: DESCARGA (SUCCESS STATE) ====================
if st.session_state.paso_actual == 3 and st.session_state.documento_generado:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title"><span class="section-icon">🎉</span> Paso 3: ¡Documento listo!</h2>', unsafe_allow_html=True)

    mostrar_exito("¡Documento generado exitosamente!", {
        "Archivo": Path(st.session_state.documento_generado).name,
        "Ubicación": str(st.session_state.documento_generado),
        "Tamaño": f"{Path(st.session_state.documento_generado).stat().st_size / 1024:.2f} KB"
    })

    # Download button con estilo especial
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    with open(st.session_state.documento_generado, 'rb') as f:
        st.download_button(
            label="⬇️ Descargar Documento",
            data=f,
            file_name=Path(st.session_state.documento_generado).name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            key="download_main"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón para generar otro documento
    if st.button("📄 Generar Otro Documento", key="new_doc"):
        # Reset state
        st.session_state.metadata = None
        st.session_state.validation_report = None
        st.session_state.er_diagram = None
        st.session_state.file_path = None
        st.session_state.paso_actual = 1
        st.session_state.documento_generado = None
        st.session_state.show_success = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== EMPTY STATE ====================
elif not archivo_seleccionado and not st.session_state.processing:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📁</div>
        <div class="empty-text">Selecciona un archivo PBIX o PBIP para comenzar</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
    </div>
    <div class="footer">
        <p><span class="footer-logo">Generador de Documentación Power BI</span> v3.0</p>
        <p>YPF S.A. © 2026 | Equipo de TI y Analítica</p>
    </div>
""", unsafe_allow_html=True)
