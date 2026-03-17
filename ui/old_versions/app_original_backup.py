"""
Power BI Documentation Generator v3.0 - Main Application
Professional UI with Modern Components - FASE 4 + 5 Complete
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

# Import document generation
from document_generation import DocxBuilder

# Page config
st.set_page_config(
    page_title="Power BI Documentation Generator",
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
    <h1 class="app-title">📊 Power BI Documentation Generator</h1>
    <p class="app-subtitle">Generación automática de documentación técnica profesional | Version 3.0</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")

    page = st.radio(
        "Navegación",
        ["🏠 Dashboard", "📤 Generate Documentation", "📊 Analysis Results", "⚙️ Settings", "📚 Help"],
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
    st.markdown('<span class="status-badge status-completed">✓ Parsers Active</span>', unsafe_allow_html=True)
    st.markdown("")
    if st.session_state.analysis_done:
        st.markdown('<span class="status-badge status-completed">✓ Analysis Complete</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-progress">⚡ Ready to Analyze</span>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📈 Project Progress")
    st.progress(0.83)  # Updated: Phase 4+5 = 83% (5/6 phases)
    st.caption("Phase 5 of 6 completed")

    st.markdown("---")

    st.caption("© 2026 YPF S.A.")
    st.caption("IT Analytics Team")

# Main content
if page == "🏠 Dashboard":
    # Use metric cards component
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_metric_card("Formats", "2", "📦", "primary")

    with col2:
        create_metric_card("Extraction", "100%", "✓", "success")

    with col3:
        create_metric_card("Tests", "30+", "🧪", "info")

    with col4:
        create_metric_card("Status", "Live", "🚀", "success")

    st.markdown("##")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🚀 Ready to Generate Documentation</h3>
            <p>Upload your Power BI file and get professional documentation in minutes.</p>
            <ul style="list-style: none; padding-left: 0;">
                <li>✅ <strong>PBIX & PBIP</strong> - Both formats supported</li>
                <li>✅ <strong>Complete Metadata</strong> - Full extraction without truncation</li>
                <li>✅ <strong>Word Generation</strong> - Complete document with all sections</li>
                <li>✅ <strong>Interactive UI</strong> - Modern components with dark/light themes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Quick Stats</h3>
            <p><strong>Architecture:</strong> Modular</p>
            <p><strong>Components:</strong> 6 UI + 9 Generators</p>
            <p><strong>Phase:</strong> 5/6</p>
            <p><strong>Status:</strong> Operational</p>
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
            <div class="step-label {'active' if step == 3 else ''}">Analyze</div>
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
        help="PBIX: Single file upload | PBIP: Local project folder"
    )

    file_ready = False

    if format_type == "PBIX File (.pbix)":
        st.markdown("""
        <div class="info-card">
            <h4>📦 PBIX File Upload</h4>
            <p>Upload your Power BI Desktop file (.pbix)</p>
            <p><strong>✓</strong> Single file - easy to share</p>
            <p><strong>✓</strong> Direct upload from anywhere</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your .pbix file here or click to browse",
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
            <h4>📁 PBIP Project Path</h4>
            <p>Provide the path to your PBIP project or folder</p>
            <p><strong>✓</strong> No upload needed - works directly with your files</p>
            <p><strong>✓</strong> Faster for large projects</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warning-box">
            <p><strong>📍 How to get the path:</strong></p>
            <ol>
                <li>Open Windows Explorer</li>
                <li>Navigate to your PBIP project</li>
                <li>Click on the file/folder in the address bar</li>
                <li>Copy the path (Ctrl+C)</li>
                <li>Paste it below (quotes will be removed automatically)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💡 See example"):
            st.code(r"C:\Users\YourName\Documents\PowerBI\MyProject.pbip", language="text")
            st.markdown("**Or the project folder:**")
            st.code(r"C:\Users\YourName\Documents\PowerBI\MyProject", language="text")

        pbip_input = st.text_input(
            "Paste the path here:",
            placeholder=r"C:\Users\...\MyProject.pbip",
            help="Paste the full path - quotes will be cleaned automatically",
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
                st.markdown("""
                <div class="error-box">
                    <p><strong>Path doesn't exist. Please check:</strong></p>
                    <ul>
                        <li>The path is correct</li>
                        <li>The file/folder exists</li>
                        <li>You have permission to access it</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Step 2: Configuration
    if file_ready:
        st.markdown("### ✏️ Step 2: Configure Report Information")

        with st.form("report_config"):
            col1, col2 = st.columns(2)

            with col1:
                report_name = st.text_input(
                    "Report Name *",
                    value=st.session_state.file_path.stem if st.session_state.file_path else "",
                    help="Name of the Power BI report"
                )
                author = st.text_input("Author *", value="YPF IT Team")

            with col2:
                version = st.text_input("Version *", value="1.0")
                department = st.text_input("Department", value="Analytics")

            objective = st.text_area(
                "Objective",
                placeholder="Describe the business purpose of this report...",
                help="What problem does this report solve?"
            )

            scope = st.text_area(
                "Scope",
                placeholder="Define what is included in this report...",
                help="What data, time periods, and metrics are covered?"
            )

            st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                analyze_button = st.form_submit_button(
                    "🚀 Analyze File",
                    use_container_width=True,
                    help="Start analyzing the Power BI file"
                )

        if analyze_button:
            if not report_name or not author or not version:
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                try:
                    # Show loading animation
                    with st.spinner(""):
                        show_loading_animation("data-processing", height=150, key="analysis_anim")

                    with st.spinner("🔄 Analyzing Power BI file..."):
                        parser = create_parser(str(st.session_state.file_path))

                        progress = st.progress(0)
                        progress.progress(25)
                        st.write("📖 Reading file structure...")

                        progress.progress(50)
                        st.write("🔍 Extracting metadata...")

                        metadata = parser.parse()

                        progress.progress(75)
                        st.write("✨ Building data model...")

                        st.session_state.metadata = metadata

                        # Validation
                        st.write("🔍 Validating model...")
                        model_validator = ModelValidator(metadata.data_model)
                        model_report = model_validator.validate_all()

                        relationship_validator = RelationshipValidator(metadata.data_model)
                        rel_report = relationship_validator.validate_all()

                        combined_report = model_report
                        for issue in rel_report.issues:
                            combined_report.add_issue(issue)
                        combined_report.quality_score = (model_report.quality_score + rel_report.quality_score) / 2

                        st.session_state.validation_report = combined_report

                        # DAX complexity
                        if metadata.data_model.measures:
                            st.write("📐 Analyzing DAX complexity...")
                            complexity_analyzer = ComplexityAnalyzer(metadata.data_model.measures)
                            st.session_state.complexity_report = complexity_analyzer.analyze_all()

                        # ER diagram
                        st.write("🎨 Generating ER diagram...")
                        try:
                            er_gen = ERDiagramGenerator(metadata.data_model)
                            st.session_state.er_diagram = er_gen
                        except ImportError as ie:
                            st.warning(f"ER diagram generation skipped: {ie}")

                        st.session_state.analysis_done = True

                        progress.progress(100)

                    # Show success animation
                    show_success_animation(height=150, key="success_anim")

                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ Analysis Complete!</h3>
                        <p><strong>Successfully extracted:</strong></p>
                        <ul>
                            <li>📊 {} tables</li>
                            <li>🔗 {} relationships</li>
                            <li>📐 {} DAX measures</li>
                            <li>📄 {} report pages</li>
                        </ul>
                        <p><strong>→ Go to "Analysis Results" to explore the data</strong></p>
                    </div>
                    """.format(
                        metadata.data_model.table_count,
                        metadata.data_model.relationship_count,
                        metadata.data_model.measure_count,
                        metadata.layout.page_count
                    ), unsafe_allow_html=True)

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
                <li>Click "Analyze File"</li>
                <li>Return here to see results</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    else:
        metadata = st.session_state.metadata

        # Summary metrics with cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            create_metric_card("Tables", str(metadata.data_model.table_count), "📊", "primary")
        with col2:
            create_metric_card("Relationships", str(metadata.data_model.relationship_count), "🔗", "info")
        with col3:
            create_metric_card("Measures", str(metadata.data_model.measure_count), "📐", "success")
        with col4:
            create_metric_card("Pages", str(metadata.layout.page_count), "📄", "info")

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Data Model",
            "🔗 Relationships",
            "📐 DAX Measures",
            "📄 Report Layout",
            "🎨 ER Diagram",
            "✅ Validation"
        ])

        with tab1:
            st.subheader("Tables")

            # Prepare data for AG-Grid
            tables_data = []
            for table in metadata.data_model.tables:
                tables_data.append({
                    'Name': table.name,
                    'Type': table.table_type.value,
                    'Columns': len(table.columns),
                    'Calculated': table.calculated_column_count,
                    'Hidden': 'Yes' if hasattr(table, 'is_hidden') and table.is_hidden else 'No'
                })

            if tables_data:
                df = pd.DataFrame(tables_data)
                grid_response = create_interactive_table(
                    df,
                    enable_sorting=True,
                    enable_filtering=True,
                    enable_pagination=True,
                    page_size=10,
                    selection_mode='single',
                    height=400
                )

                # Show selected table details
                selected_rows = grid_response.get('selected_rows', [])
                if selected_rows is not None and len(selected_rows) > 0:
                    selected_name = selected_rows[0]['Name']
                    selected_table = next((t for t in metadata.data_model.tables if t.name == selected_name), None)

                    if selected_table:
                        st.markdown(f"### 📋 {selected_table.name} Details")

                        # Columns
                        columns_data = []
                        for col in selected_table.columns:
                            columns_data.append({
                                'Column': col.name,
                                'Type': col.data_type.value,
                                'Calculated': '✓' if col.is_calculated else '',
                                'Key': '✓' if hasattr(col, 'is_key') and col.is_key else ''
                            })

                        if columns_data:
                            df_cols = pd.DataFrame(columns_data)
                            create_interactive_table(
                                df_cols,
                                enable_pagination=True,
                                page_size=20,
                                selection_mode='disabled',
                                height=300
                            )

        with tab2:
            st.subheader(f"Relationships ({len(metadata.data_model.relationships)})")

            if metadata.data_model.relationships:
                # Prepare data for AG-Grid
                rel_data = []
                for rel in metadata.data_model.relationships:
                    rel_data.append({
                        'From Table': rel.from_table,
                        'From Column': rel.from_column,
                        '→': '⟷' if rel.is_bidirectional else '→',
                        'To Table': rel.to_table,
                        'To Column': rel.to_column,
                        'Cardinality': rel.cardinality.value,
                        'M:M': '🔶' if rel.is_many_to_many else ''
                    })

                df = pd.DataFrame(rel_data)
                create_interactive_table(
                    df,
                    enable_sorting=True,
                    enable_filtering=True,
                    selection_mode='disabled',
                    height=500
                )
            else:
                st.info("No relationships found")

        with tab3:
            st.subheader(f"DAX Measures ({len(metadata.data_model.measures)})")

            if metadata.data_model.measures:
                # Prepare data for AG-Grid
                measures_data = []
                for measure in metadata.data_model.measures:
                    measures_data.append({
                        'Measure': measure.name,
                        'Table': measure.table,
                        'Complexity': measure.complexity.value if measure.complexity else 'Unknown',
                        'Length': measure.expression_length,
                        'Time Intel': '✓' if measure.has_time_intelligence else '',
                        'Iterators': '✓' if measure.uses_iterators else ''
                    })

                df = pd.DataFrame(measures_data)
                grid_response = create_interactive_table(
                    df,
                    enable_sorting=True,
                    enable_filtering=True,
                    enable_pagination=True,
                    page_size=15,
                    selection_mode='single',
                    height=500
                )

                # Show selected measure expression
                selected_rows = grid_response.get('selected_rows', [])
                if selected_rows is not None and len(selected_rows) > 0:
                    selected_name = selected_rows[0]['Measure']
                    selected_measure = next((m for m in metadata.data_model.measures if m.name == selected_name), None)

                    if selected_measure:
                        st.markdown(f"### 📐 {selected_measure.name}")
                        st.code(selected_measure.expression, language="dax")
            else:
                st.info("No measures found")

        with tab4:
            st.subheader(f"Report Pages ({len(metadata.layout.pages)})")

            if metadata.layout.pages:
                pages_data = []
                for page in metadata.layout.pages:
                    pages_data.append({
                        'Page': page.display_name,
                        'Visuals': page.visual_count,
                        'Hidden': 'Yes' if page.is_hidden else 'No'
                    })

                df = pd.DataFrame(pages_data)
                create_interactive_table(
                    df,
                    enable_sorting=True,
                    selection_mode='disabled',
                    height=400
                )
            else:
                st.info("No pages found")

        with tab5:
            st.subheader("🎨 Entity-Relationship Diagram")

            if st.session_state.er_diagram:
                er_gen = st.session_state.er_diagram

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    layout = st.selectbox(
                        "Layout Algorithm",
                        options=['spring', 'circular', 'kamada_kawai', 'shell'],
                        index=0,
                        help="Spring layout works best for most models"
                    )

                try:
                    with st.spinner("Generating ER diagram..."):
                        fig = er_gen.generate_plotly_figure(
                            layout_algorithm=layout,
                            width=1400,
                            height=900,
                            show_column_count=True
                        )

                        if fig:
                            st.plotly_chart(fig, use_container_width=True)

                            st.markdown("### 📊 Diagram Metrics")
                            metrics = er_gen.get_graph_metrics()

                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                create_metric_card("Nodes", str(metrics['node_count']), "", "info")
                            with col2:
                                create_metric_card("Edges", str(metrics['edge_count']), "", "info")
                            with col3:
                                create_metric_card("Density", f"{metrics['density']:.2%}", "", "warning")
                            with col4:
                                connected = "Yes" if metrics['is_connected'] else "No"
                                create_metric_card("Connected", connected, "", "success" if metrics['is_connected'] else "error")

                            if metrics['most_connected_tables']:
                                st.markdown("### 🔗 Most Connected Tables")
                                for table, degree in metrics['most_connected_tables']:
                                    st.write(f"- **{table}**: {degree} relationships")

                        else:
                            st.warning("Could not generate diagram (Plotly not available)")

                except Exception as e:
                    st.error(f"Error generating diagram: {e}")
                    with st.expander("Technical details"):
                        st.code(traceback.format_exc())

            else:
                st.info("ER diagram generation was skipped. NetworkX may not be installed.")

        with tab6:
            st.subheader("✅ Model Validation Report")

            if st.session_state.validation_report:
                report = st.session_state.validation_report

                # Quality score
                st.markdown("### 📊 Quality Score")
                score_color = "green" if report.quality_score >= 80 else "orange" if report.quality_score >= 60 else "red"
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem;">
                    <h1 style="color: {score_color}; font-size: 4rem; margin: 0;">{report.quality_score:.1f}</h1>
                    <p style="font-size: 1.2rem; color: #aaa;">out of 100</p>
                </div>
                """, unsafe_allow_html=True)

                # Issue summary
                st.markdown("### 📋 Issue Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    create_metric_card("Critical", str(report.critical_count), "🔴", "error")
                with col2:
                    create_metric_card("Errors", str(report.error_count), "🟠", "warning")
                with col3:
                    create_metric_card("Warnings", str(report.warning_count), "🟡", "warning")
                with col4:
                    create_metric_card("Info", str(report.info_count), "ℹ️", "info")

                st.markdown("---")

                # Issues
                if report.total_issues > 0:
                    st.markdown("### 🔍 Issues Detected")

                    severity_filter = st.multiselect(
                        "Filter by severity",
                        options=['CRITICAL', 'ERROR', 'WARNING', 'INFO'],
                        default=['CRITICAL', 'ERROR', 'WARNING']
                    )

                    filtered_issues = [
                        issue for issue in report.issues
                        if issue.severity.name in severity_filter
                    ]

                    for issue in filtered_issues:
                        if issue.severity == ValidationSeverity.CRITICAL:
                            icon = "🔴"
                        elif issue.severity == ValidationSeverity.ERROR:
                            icon = "🟠"
                        elif issue.severity == ValidationSeverity.WARNING:
                            icon = "🟡"
                        else:
                            icon = "ℹ️"

                        with st.expander(f"{icon} {issue.category}: {issue.message}"):
                            st.markdown(f"**Severity:** {issue.severity.name}")
                            st.markdown(f"**Details:** {issue.details}")

                            if issue.affected_objects:
                                st.markdown(f"**Affected Objects:**")
                                for obj in issue.affected_objects:
                                    st.write(f"- {obj}")

                            if issue.recommendation:
                                st.markdown(f"**💡 Recommendation:** {issue.recommendation}")

                else:
                    st.success("🎉 No issues found! Your model looks great.")

            else:
                st.info("No validation report available")

        st.markdown("---")

        # DOCUMENT GENERATION BUTTON - INTEGRATED!
        st.markdown("## 📥 Generate Documentation")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Generate Word Document", use_container_width=True):
                try:
                    # Show processing animation
                    with st.spinner(""):
                        show_loading_animation("data-processing", height=150, key="doc_gen_anim")

                    with st.spinner("Generating Word document..."):
                        progress = st.progress(0)

                        def update_progress(step, message):
                            progress.progress(step)
                            st.write(message)

                        # Initialize builder
                        from document_generation.docx_builder import DocxBuilder
                        template_path = "templates/plantilla_corporativa_ypf.docx"

                        # Check if template exists
                        if not Path(template_path).exists():
                            st.warning(f"Template not found at {template_path}, using blank document")

                        builder = DocxBuilder(template_path)

                        # Build document
                        output_path = builder.build(
                            metadata=st.session_state.metadata,
                            validation_report=st.session_state.validation_report,
                            er_diagram_generator=st.session_state.er_diagram,
                            progress_callback=update_progress
                        )

                        progress.progress(100)

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

elif page == "⚙️ Settings":
    st.markdown("## ⚙️ Settings")

    tab1, tab2 = st.tabs(["📄 Template", "⚡ Advanced"])

    with tab1:
        st.markdown("""
        <div class="info-card">
            <h3>📄 Word Template</h3>
            <p>Current: <strong>YPF Corporate Template</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.text_input(
            "Template Path",
            value="templates/plantilla_corporativa_ypf.docx",
            disabled=True
        )

    with tab2:
        st.markdown("""
        <div class="info-card">
            <h3>⚡ Advanced Settings</h3>
        </div>
        """, unsafe_allow_html=True)

        st.checkbox("Include ER Diagram", value=True)
        st.checkbox("Validate model", value=True)
        st.checkbox("Include security analysis", value=True)

elif page == "📚 Help":
    st.markdown("## 📚 Help & Documentation")

    st.markdown("""
    <div class="info-card">
        <h3>🎯 Quick Start</h3>
        <ol>
            <li>Go to <strong>Generate Documentation</strong></li>
            <li>Select your file type (PBIX or PBIP)</li>
            <li>Upload/provide path to your file</li>
            <li>Fill in report information</li>
            <li>Click <strong>Analyze File</strong></li>
            <li>View results in <strong>Analysis Results</strong></li>
            <li>Click <strong>Generate Word Document</strong></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("❓ FAQ"):
        st.markdown("""
        **Q: My PBIP path has quotes, what do I do?**
        A: Just paste it normally - quotes are removed automatically.

        **Q: Which format should I use?**
        A: PBIX for single files, PBIP for projects you're working on locally.

        **Q: Does document generation work?**
        A: Yes! Phase 5 complete - full Word generation with all sections.

        **Q: Are DAX expressions truncated?**
        A: No! All expressions are included in full, no matter the length.

        **Q: Can I switch between themes?**
        A: Yes! Use the theme toggle in the sidebar to switch between dark and light modes.
        """)

    with st.expander("🆕 What's New in v3.0"):
        st.markdown("""
        **Phase 4: Modern UI**
        - ✅ Dark/Light theme toggle
        - ✅ AG-Grid interactive tables
        - ✅ Lottie animations
        - ✅ Metric cards
        - ✅ Enhanced components

        **Phase 5: Document Generation**
        - ✅ Complete Word document generation
        - ✅ 9 section generators (cover, summary, data model, relationships, DAX, security, visualizations, validation, appendix)
        - ✅ ER diagram embedding
        - ✅ YPF corporate template
        - ✅ NO truncation - all data included!
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.4); padding: 1rem 0;">
    <p style="margin: 0;">Power BI Documentation Generator v3.0 | YPF S.A. © 2026</p>
    <p style="margin: 0; font-size: 0.8rem;">Phase 5 Complete - Document Generation Active</p>
</div>
""", unsafe_allow_html=True)
