"""
UI Components Module

Modern, reusable UI components for the Power BI Documentation Generator.
"""

# Import from metric_cards
from .metric_cards import (
    create_metric_card,
    create_stat_card,
    create_progress_card,
    create_info_box,
    create_feature_card
)

# Import from data_tables
from .data_tables import (
    create_interactive_table,
    create_table_with_details,
    create_colored_table,
    create_simple_table,
    create_metrics_table
)

# Import from file_uploader
from .file_uploader import (
    create_file_uploader,
    create_path_input,
    create_dual_input,
    create_simple_uploader
)

# Import from animations
from .animations import (
    show_loading_animation,
    show_success_animation,
    show_processing_animation,
    show_error_animation,
    show_celebration_animation,
    preload_animations
)

# Import from theme_manager
from .theme_manager import ThemeManager

__all__ = [
    # Metric cards
    'create_metric_card',
    'create_stat_card',
    'create_progress_card',
    'create_info_box',
    'create_feature_card',

    # Data tables
    'create_interactive_table',
    'create_table_with_details',
    'create_colored_table',
    'create_simple_table',
    'create_metrics_table',

    # File uploader
    'create_file_uploader',
    'create_path_input',
    'create_dual_input',
    'create_simple_uploader',

    # Animations
    'show_loading_animation',
    'show_success_animation',
    'show_processing_animation',
    'show_error_animation',
    'show_celebration_animation',
    'preload_animations',

    # Theme manager
    'ThemeManager'
]
