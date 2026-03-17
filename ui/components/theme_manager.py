"""
Theme Manager Component

Manages theme switching between dark and light modes.
"""

import streamlit as st
from ..styles.theme import DARK_THEME, LIGHT_THEME


class ThemeManager:
    """Manages application theme (dark/light mode)"""

    THEME_KEY = 'app_theme'
    DARK = 'dark'
    LIGHT = 'light'

    def __init__(self):
        """Initialize theme manager"""
        if self.THEME_KEY not in st.session_state:
            st.session_state[self.THEME_KEY] = self.DARK

    def get_current_theme(self) -> str:
        """
        Get current theme name

        Returns:
            Theme name ('dark' or 'light')
        """
        return st.session_state.get(self.THEME_KEY, self.DARK)

    def get_current_theme_css(self) -> str:
        """
        Get CSS for current theme

        Returns:
            CSS string for current theme
        """
        current = self.get_current_theme()
        return DARK_THEME if current == self.DARK else LIGHT_THEME

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        current = self.get_current_theme()
        new_theme = self.LIGHT if current == self.DARK else self.DARK
        st.session_state[self.THEME_KEY] = new_theme
        st.rerun()

    def apply_theme(self):
        """Apply current theme CSS to the page"""
        css = self.get_current_theme_css()
        st.markdown(css, unsafe_allow_html=True)

    def render_theme_toggle(self):
        """
        Render theme toggle button

        Returns:
            True if theme was toggled
        """
        current = self.get_current_theme()

        if current == self.DARK:
            icon = "☀️"
            label = "Light Mode"
        else:
            icon = "🌙"
            label = "Dark Mode"

        if st.button(f"{icon} {label}", use_container_width=True):
            self.toggle_theme()
            return True

        return False

    def is_dark_mode(self) -> bool:
        """
        Check if current theme is dark mode

        Returns:
            True if dark mode is active
        """
        return self.get_current_theme() == self.DARK

    def is_light_mode(self) -> bool:
        """
        Check if current theme is light mode

        Returns:
            True if light mode is active
        """
        return self.get_current_theme() == self.LIGHT
