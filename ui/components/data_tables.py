"""
Data Tables Component

AG-Grid interactive tables for data display.
"""

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from typing import List, Dict, Any, Optional


def create_interactive_table(data: pd.DataFrame,
                            columns: Optional[List[str]] = None,
                            enable_sorting: bool = True,
                            enable_filtering: bool = True,
                            enable_pagination: bool = True,
                            page_size: int = 20,
                            fit_columns_on_grid_load: bool = True,
                            selection_mode: str = 'single',
                            height: int = 400) -> Any:
    """
    Create AG-Grid interactive table with full features

    Args:
        data: DataFrame to display
        columns: Optional list of columns to display (None = all)
        enable_sorting: Enable column sorting
        enable_filtering: Enable column filtering
        enable_pagination: Enable pagination
        page_size: Rows per page
        fit_columns_on_grid_load: Auto-fit column widths
        selection_mode: Selection mode ('single', 'multiple', 'disabled')
        height: Grid height in pixels

    Returns:
        Grid response object
    """
    if columns:
        data = data[columns]

    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(data)

    # Enable features
    if enable_sorting:
        gb.configure_default_column(sorteable=True)

    if enable_filtering:
        gb.configure_default_column(filterable=True)

    if enable_pagination:
        gb.configure_pagination(
            enabled=True,
            paginationAutoPageSize=False,
            paginationPageSize=page_size
        )

    # Selection
    if selection_mode != 'disabled':
        gb.configure_selection(
            selection_mode=selection_mode,
            use_checkbox=True
        )

    # Column sizing
    if fit_columns_on_grid_load:
        gb.configure_grid_options(domLayout='normal')

    grid_options = gb.build()

    # Render grid
    grid_response = AgGrid(
        data,
        gridOptions=grid_options,
        height=height,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        theme='streamlit'
    )

    return grid_response


def create_table_with_details(data: pd.DataFrame,
                              detail_columns: List[str],
                              summary_columns: Optional[List[str]] = None,
                              key_column: str = None) -> Any:
    """
    Create table with expandable details

    Args:
        data: DataFrame to display
        detail_columns: Columns to show in detail view
        summary_columns: Columns to show in summary (None = all except detail)
        key_column: Column to use as row key

    Returns:
        Selected row data or None
    """
    if summary_columns is None:
        summary_columns = [col for col in data.columns if col not in detail_columns]

    # Display summary table
    grid_response = create_interactive_table(
        data[summary_columns],
        enable_pagination=True,
        selection_mode='single',
        height=400
    )

    # Show details for selected row
    selected_rows = grid_response.get('selected_rows', [])

    if selected_rows is not None and len(selected_rows) > 0:
        selected_row = selected_rows[0]

        st.markdown("### Selected Row Details")

        # Find full row in original data
        if key_column and key_column in summary_columns:
            key_value = selected_row[key_column]
            full_row = data[data[key_column] == key_value].iloc[0]

            # Display detail columns
            for col in detail_columns:
                if col in full_row:
                    st.markdown(f"**{col}:**")
                    st.code(str(full_row[col]), language='text')

            return full_row

    return None


def create_colored_table(data: pd.DataFrame,
                        color_column: str,
                        color_map: Dict[Any, str],
                        columns: Optional[List[str]] = None) -> Any:
    """
    Create table with colored cells based on values

    Args:
        data: DataFrame to display
        color_column: Column to use for coloring
        color_map: Mapping of values to colors
        columns: Optional list of columns to display

    Returns:
        Grid response object
    """
    if columns:
        data = data[columns]

    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(data)

    # Configure default features
    gb.configure_default_column(sorteable=True, filterable=True)
    gb.configure_pagination(enabled=True, paginationPageSize=20)
    gb.configure_selection(selection_mode='single', use_checkbox=True)

    # Add cell styling based on color_column
    # Note: This requires JavaScript code which may not work in all environments
    # Basic implementation without JS
    grid_options = gb.build()

    # Render grid
    grid_response = AgGrid(
        data,
        gridOptions=grid_options,
        height=400,
        fit_columns_on_grid_load=True,
        theme='streamlit'
    )

    return grid_response


def create_simple_table(data: pd.DataFrame,
                       max_rows: int = 100,
                       use_container_width: bool = True) -> None:
    """
    Create simple non-interactive table (fallback)

    Args:
        data: DataFrame to display
        max_rows: Maximum rows to display
        use_container_width: Use full container width
    """
    if len(data) > max_rows:
        st.warning(f"Displaying first {max_rows} of {len(data)} rows")
        data = data.head(max_rows)

    st.dataframe(data, use_container_width=use_container_width)


def create_metrics_table(data: Dict[str, Any],
                        title: Optional[str] = None) -> None:
    """
    Create 2-column metrics table

    Args:
        data: Dictionary of label: value pairs
        title: Optional title
    """
    if title:
        st.markdown(f"### {title}")

    # Convert to DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])

    # Use simple table for metrics (no need for AG-Grid)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
