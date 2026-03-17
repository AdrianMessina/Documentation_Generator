"""
Animations Component

Lottie animations for loading and success states.
"""

import streamlit as st
from streamlit_lottie import st_lottie
import json
from pathlib import Path
from typing import Optional
import requests


# Built-in fallback animations (simple JSON)
LOADING_ANIMATION = {
    "v": "5.5.7",
    "fr": 60,
    "ip": 0,
    "op": 180,
    "w": 200,
    "h": 200,
    "nm": "Loading",
    "ddd": 0,
    "assets": [],
    "layers": []
}

SUCCESS_ANIMATION = {
    "v": "5.5.7",
    "fr": 60,
    "ip": 0,
    "op": 60,
    "w": 200,
    "h": 200,
    "nm": "Success",
    "ddd": 0,
    "assets": [],
    "layers": []
}


def load_lottie_file(filepath: str) -> Optional[dict]:
    """
    Load Lottie animation from file

    Args:
        filepath: Path to JSON file

    Returns:
        Animation dict or None
    """
    try:
        path = Path(filepath)
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load animation from {filepath}: {e}")

    return None


def load_lottie_url(url: str) -> Optional[dict]:
    """
    Load Lottie animation from URL

    Args:
        url: URL to JSON file

    Returns:
        Animation dict or None
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.warning(f"Could not load animation from {url}: {e}")

    return None


def show_loading_animation(animation_name: str = "data-processing",
                          height: int = 200,
                          key: Optional[str] = None) -> None:
    """
    Display loading animation

    Args:
        animation_name: Name of animation to load
        height: Animation height in pixels
        key: Optional unique key for widget
    """
    # Skip animations - just show spinner (no external connections)
    pass


def show_success_animation(height: int = 150,
                          key: Optional[str] = None) -> None:
    """
    Display success animation

    Args:
        height: Animation height in pixels
        key: Optional unique key for widget
    """
    # Skip animations - just show success message
    pass


def show_processing_animation(message: str = "Processing...",
                             height: int = 150) -> None:
    """
    Display processing animation with message

    Args:
        message: Message to display
        height: Animation height in pixels
    """
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        show_loading_animation(animation_name="processing", height=height)
        st.markdown(
            f"<div style='text-align: center; color: white; font-size: 1.1rem;'>{message}</div>",
            unsafe_allow_html=True
        )


def show_error_animation(message: str = "An error occurred",
                        height: int = 150) -> None:
    """
    Display error animation with message

    Args:
        message: Error message
        height: Animation height in pixels
    """
    # Try to load error animation
    animation_path = Path("assets/animations/error.json")
    animation = load_lottie_file(str(animation_path))

    if animation is None:
        # Fallback URL
        url = "https://assets2.lottiefiles.com/packages/lf20_ddxv3rxw.json"
        animation = load_lottie_url(url)

    if animation:
        st_lottie(animation, height=height, loop=False)

    st.error(message)


def show_celebration_animation(height: int = 200) -> None:
    """
    Display celebration animation

    Args:
        height: Animation height in pixels
    """
    # Celebration animation URL
    url = "https://assets2.lottiefiles.com/packages/lf20_aEFaHc.json"
    animation = load_lottie_url(url)

    if animation:
        st_lottie(animation, height=height, loop=False)
    else:
        st.balloons()


# Preload common animations for performance
def preload_animations():
    """Preload common animations into session state"""
    if 'animations_loaded' not in st.session_state:
        st.session_state.animations_loaded = {}

        # Try to preload common animations
        for name in ['loading', 'success', 'processing']:
            animation_path = Path(f"assets/animations/{name}.json")
            animation = load_lottie_file(str(animation_path))
            if animation:
                st.session_state.animations_loaded[name] = animation

        st.session_state.animations_preloaded = True
