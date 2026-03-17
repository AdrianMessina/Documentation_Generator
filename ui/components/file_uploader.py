"""
File Uploader Component

Enhanced file upload component with drag-drop, preview, and validation.
"""

import streamlit as st
from pathlib import Path
from typing import List, Optional, Tuple
import os


def create_file_uploader(file_types: List[str],
                        max_size_mb: int = 100,
                        help_text: Optional[str] = None,
                        key: Optional[str] = None) -> Optional[any]:
    """
    Create enhanced file uploader with validation

    Args:
        file_types: List of allowed file extensions (e.g., ['.pbix', '.pbip'])
        max_size_mb: Maximum file size in MB
        help_text: Optional help text to display
        key: Optional unique key for widget

    Returns:
        Uploaded file object or None
    """
    # Display custom help text
    if help_text:
        st.markdown(
            f"<div class='info-card'>{help_text}</div>",
            unsafe_allow_html=True
        )

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=file_types,
        help=f"Maximum file size: {max_size_mb}MB",
        key=key
    )

    if uploaded_file is not None:
        # Validate file size
        file_size_mb = uploaded_file.size / (1024 * 1024)

        if file_size_mb > max_size_mb:
            st.error(f"❌ File too large: {file_size_mb:.1f}MB (max: {max_size_mb}MB)")
            return None

        # Show file info
        _show_file_info(uploaded_file, file_size_mb)

        return uploaded_file

    return None


def create_path_input(label: str = "File Path",
                     file_types: List[str] = None,
                     help_text: Optional[str] = None,
                     key: Optional[str] = None) -> Optional[str]:
    """
    Create file path input with validation

    Args:
        label: Input label
        file_types: Optional list of allowed extensions
        help_text: Optional help text
        key: Optional unique key for widget

    Returns:
        Validated file path or None
    """
    # Text input
    file_path = st.text_input(
        label,
        help=help_text or "Enter the full path to the file",
        key=key
    )

    if file_path:
        # Clean path (remove quotes)
        file_path = file_path.strip().strip('"').strip("'").strip()

        # Validate path
        valid, message = _validate_file_path(file_path, file_types)

        if not valid:
            st.error(f"❌ {message}")
            return None

        # Show file info
        _show_path_info(file_path)

        return file_path

    return None


def create_dual_input(file_types: List[str],
                     max_size_mb: int = 100,
                     help_text: Optional[str] = None) -> Tuple[Optional[any], Optional[str]]:
    """
    Create both file uploader and path input

    Args:
        file_types: List of allowed file extensions
        max_size_mb: Maximum file size in MB
        help_text: Optional help text

    Returns:
        Tuple of (uploaded_file, file_path)
    """
    st.markdown("### Select File")

    # Choice tabs
    tab1, tab2 = st.tabs(["📤 Upload File", "📂 Enter Path"])

    uploaded_file = None
    file_path = None

    with tab1:
        uploaded_file = create_file_uploader(
            file_types=file_types,
            max_size_mb=max_size_mb,
            help_text=help_text
        )

    with tab2:
        file_path = create_path_input(
            label="File Path",
            file_types=file_types,
            help_text=help_text
        )

    return uploaded_file, file_path


def _validate_file_path(file_path: str,
                       file_types: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Validate file path

    Args:
        file_path: Path to validate
        file_types: Optional list of allowed extensions

    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(file_path)

    # Check if exists
    if not path.exists():
        return False, f"File not found: {file_path}"

    # Check if is file
    if not path.is_file():
        return False, f"Path is not a file: {file_path}"

    # Check extension
    if file_types:
        extension = path.suffix.lower()
        if extension not in [ft.lower() for ft in file_types]:
            return False, f"Invalid file type: {extension}. Allowed: {', '.join(file_types)}"

    return True, "Valid"


def _show_file_info(uploaded_file, file_size_mb: float) -> None:
    """Show uploaded file information"""
    st.markdown(
        f"""
        <div class='info-card' style='margin-top: 1rem;'>
            <h4 style='margin-top: 0;'>📄 File Information</h4>
            <p><strong>Name:</strong> {uploaded_file.name}</p>
            <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>
            <p><strong>Type:</strong> {uploaded_file.type or 'Unknown'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def _show_path_info(file_path: str) -> None:
    """Show file path information"""
    path = Path(file_path)
    file_size_mb = path.stat().st_size / (1024 * 1024)

    st.markdown(
        f"""
        <div class='info-card' style='margin-top: 1rem;'>
            <h4 style='margin-top: 0;'>📂 File Information</h4>
            <p><strong>Name:</strong> {path.name}</p>
            <p><strong>Path:</strong> {path.parent}</p>
            <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>
            <p><strong>Extension:</strong> {path.suffix}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def create_simple_uploader(label: str = "Upload File",
                          file_types: Optional[List[str]] = None,
                          key: Optional[str] = None) -> Optional[any]:
    """
    Create simple file uploader (fallback without enhancements)

    Args:
        label: Uploader label
        file_types: Optional list of allowed extensions
        key: Optional unique key

    Returns:
        Uploaded file or None
    """
    return st.file_uploader(
        label,
        type=file_types,
        key=key
    )
