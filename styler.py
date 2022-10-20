import dataclasses
import streamlit as st

import pandas as pd
import locale
from typing import List
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode

locale.setlocale(locale.LC_ALL, "")

MIN_TABLE_HEIGHT = 500


def value_with_locale(value, precision: int = 0) -> str:
    return locale.format_string(f"%10.{precision}f", value, grouping=True).replace(",", " ")


@dataclasses.dataclass
class Formatter:
    short_name: str
    rus_name: str
    format: str = None


def style_df(df: pd.DataFrame, style_dict: dict):
    styles = __to_formatter(style_dict)
    cols = [f.short_name for f in styles if f.short_name in df.columns]
    rename_cols = {f.short_name: f.rus_name for f in styles}
    format_cols = {f.rus_name: f.format for f in styles if f.format}
    return df[cols].rename(rename_cols, axis=1).style.format(format_cols)


def __to_formatter(style_dict: dict) -> List[Formatter]:
    return [Formatter(k, v[0], v[1]) for k, v in style_dict.items()]


def get_highlighter_by_condition(condition, color):
    return JsCode(
        f"""
        function(params) {{
            color = "{color}";
            if (params.value {condition}) {{
                return {{
                    'backgroundColor': color
                }}
            }}
        }};
        """
    )


def get_numeric_style_with_precision(precision: int) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"], "precision": precision}


PRECISION_ZERO = get_numeric_style_with_precision(0)
PRECISION_ONE = get_numeric_style_with_precision(1)
PRECISION_TWO = get_numeric_style_with_precision(2)


def get_current_streamlit_theme() -> str:
    return "light" if not st.get_option("theme.base") else st.get_option("theme.base")


def draw_grid(
    df,
    formatter: dict = None,
    selection="multiple",
    use_checkbox=False,
    fit_columns=False,
    theme="light",
    min_height: int = MIN_TABLE_HEIGHT,
    wrap_text: bool = False,
    auto_height: bool = False,
    key=None
):
    if formatter is None:
        formatter = {}
    cols = (
        [col for col in list(formatter.keys()) if col in df.columns]
        if formatter
        else df.columns
    )
    gb = GridOptionsBuilder.from_dataframe(df[cols])
    gb.configure_selection(selection_mode=selection, use_checkbox=use_checkbox)
    gb.configure_default_column(
        filterable=True, 
        groupable=False, 
        editable=False,
        wrapText=wrap_text,
        autoHeight=auto_height
    )
    for latin_name, (rus_name, style_dict) in formatter.items():
        gb.configure_column(latin_name, header_name=rus_name, **style_dict)
    return AgGrid(
        df[cols],
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=fit_columns,
        height=min(min_height, (1 + len(df.index)) * 35),
        theme=theme if theme is not None else get_current_streamlit_theme(),
        key=key
    )


def print_docs(path, header):
    with st.expander(header):
        with open(f".{path}", "r", encoding="utf-8") as f:
            lines = f.readlines()
            st.markdown("".join(lines))
