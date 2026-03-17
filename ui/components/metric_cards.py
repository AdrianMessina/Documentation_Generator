"""
Metric Cards Component

Professional metric display components with animations and gradients.
"""

import streamlit as st
from typing import Optional


def create_metric_card(label: str, value: str, icon: str = "",
                       color: str = "primary") -> None:
    """
    Create animated metric card with gradient background

    Args:
        label: Metric label text
        value: Metric value to display
        icon: Optional emoji icon
        color: Color scheme ('primary', 'success', 'warning', 'error')
    """
    # Color gradients
    gradients = {
        'primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'success': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        'warning': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
        'error': 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
        'info': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
    }

    gradient = gradients.get(color, gradients['primary'])

    st.markdown(f"""
    <div class="metric-card" style="background: {gradient};">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def create_stat_card(title: str, value: str, subtitle: Optional[str] = None,
                     icon: str = "", trend: Optional[str] = None) -> None:
    """
    Create detailed statistics card

    Args:
        title: Card title
        value: Main value to display
        subtitle: Optional subtitle
        icon: Optional emoji icon
        trend: Optional trend indicator ('+10%', '-5%', etc.)
    """
    trend_html = ""
    if trend:
        trend_color = "#10b981" if trend.startswith('+') else "#ef4444"
        trend_html = f'<div style="color: {trend_color}; font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem;">{trend}</div>'

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 0.25rem;">{subtitle}</div>'

    st.markdown(f"""
    <div class="info-card">
        <h3>{icon} {title}</h3>
        <div style="font-size: 2rem; font-weight: 700; color: white; margin: 1rem 0;">
            {value}
        </div>
        {subtitle_html}
        {trend_html}
    </div>
    """, unsafe_allow_html=True)


def create_progress_card(label: str, current: int, total: int,
                         description: Optional[str] = None) -> None:
    """
    Create progress card with percentage bar

    Args:
        label: Progress label
        current: Current progress value
        total: Total value
        description: Optional description text
    """
    percentage = int((current / total) * 100) if total > 0 else 0

    # Determine color based on percentage
    if percentage >= 80:
        bar_color = "#10b981"
    elif percentage >= 50:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"

    desc_html = ""
    if description:
        desc_html = f'<div style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 0.5rem;">{description}</div>'

    st.markdown(f"""
    <div class="info-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-weight: 600; color: white;">{label}</span>
            <span style="font-weight: 700; color: {bar_color};">{percentage}%</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; overflow: hidden;">
            <div style="background: {bar_color}; width: {percentage}%; height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
        </div>
        <div style="color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;">
            {current} of {total} completed
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


def create_info_box(title: str, content: str, box_type: str = "info") -> None:
    """
    Create informational box with icon

    Args:
        title: Box title
        content: Box content (supports markdown)
        box_type: Type of box ('info', 'success', 'warning', 'error')
    """
    icons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }

    classes = {
        'info': 'info-card',
        'success': 'success-box',
        'warning': 'warning-box',
        'error': 'error-box'
    }

    icon = icons.get(box_type, icons['info'])
    css_class = classes.get(box_type, classes['info'])

    st.markdown(f"""
    <div class="{css_class}">
        <h4 style="margin-top: 0;">{icon} {title}</h4>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def create_feature_card(icon: str, title: str, description: str,
                        status: str = "active") -> None:
    """
    Create feature card with status indicator

    Args:
        icon: Emoji icon
        title: Feature title
        description: Feature description
        status: Status ('active', 'coming_soon', 'disabled')
    """
    status_badges = {
        'active': '<span class="status-badge status-completed">✓ Active</span>',
        'coming_soon': '<span class="status-badge status-progress">⏳ Coming Soon</span>',
        'disabled': '<span class="status-badge" style="background: #6b7280; color: white;">⊘ Disabled</span>'
    }

    status_html = status_badges.get(status, status_badges['active'])

    st.markdown(f"""
    <div class="format-option">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">{icon}</div>
            {status_html}
        </div>
        <h3 style="margin: 0.5rem 0; color: white;">{title}</h3>
        <p style="margin: 0; color: rgba(255,255,255,0.7); line-height: 1.5;">{description}</p>
    </div>
    """, unsafe_allow_html=True)
