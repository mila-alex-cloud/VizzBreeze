import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import sys

# =============================================================================
# HARD SYS.STDERR FILTER: MUTING STREAMLIT BEFORE ANY IMPORTS EXECUTE
# =============================================================================
class StreamlitNoiseFilter:
    def __init__(self, original_stream):
        self.original_stream = original_stream

    def write(self, message):
        # Жестко отсекаем строки, содержащие внутренний лог-мусор Streamlit
        if "missing ScriptRunContext" in message or "streamlit run" in message or "Session state does not function" in message:
            return
        if self.original_stream:
            self.original_stream.write(message)

    def flush(self):
        if self.original_stream:
            self.original_stream.flush()


# Intercept the standard error stream before Streamlit is imported
if sys.stderr:
    sys.stderr = StreamlitNoiseFilter(sys.stderr)

# Now the Streamlit import will execute completely silently in Jupyter / Colab environments
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


def render_with_scroll(fig, width, height):
    import streamlit as st
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    # Calculate physical pixels from your centimeter scale
    final_width = width if width is not None else 1800
    fig.update_layout(width=final_width, height=height, autosize=False)

    if get_script_run_ctx() is not None:
        # ULTRA-DYNAMIC SCROLL WITH SIDEBAR COLLAPSE SUPPORT
        st.markdown(f"""
        <div style="overflow-x: auto; overflow-y: hidden; width: 100%; display: block; padding-bottom: 15px;">
        <style>
        .stPlotlyChart > div {{
            /* Set the base fixed width calculated from your cm scale */
            width: {final_width}px !important;      
            min-width: {final_width}px !important;  
            
            /* CRITICAL FIX: If the calculated chart width is smaller than the 
               actual screen content area (e.g., when the sidebar is collapsed), 
               the chart will automatically and smoothly stretch to 100% of the browser window! */
            max-width: 100% !important; 
        }}
        </style>
        """, unsafe_allow_html=True)

def render_with_scroll(fig, width, height):
    import streamlit as st
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    # 1. Calculate precise physical pixels based on your centimeters formula
    final_width = width if width is not None else 1800
    fig.update_layout(width=final_width, height=height, autosize=False) # Disables autosizing

    # 2. Check the execution environment: Cloud (Streamlit) or Notebook (Jupyter / Colab)
    if get_script_run_ctx() is not None:
        # --- MINIMALIST SOLUTION FOR STREAMLIT (WITHOUT BUTTONS) ---

        # Get the unique memory address of the figure object to clear the cache
        obj_id = id(fig)

        # Open the scrollable container and hard-lock the width of the chart
        st.markdown(f"""
        <div style="overflow-x: auto; overflow-y: hidden; width: 100%; display: block; padding-bottom: 15px;">
        <style>
        .stPlotlyChart > div {{
            width: {final_width}px !important;      /* Hard-locks the container width */
            min-width: {final_width}px !important;  /* Prevents it from shrinking or stretching */
            max-width: 100% !important;             /* Allows the chart to expand when the sidebar is collapsed */
        }}
        </style>
        """, unsafe_allow_html=True)

        # Render the native chart with fluid container width disabled.
        # The key parameter ensures that Plotly updates the canvas tracking the slider.
        st.plotly_chart(
            fig,
            use_container_width=False,
            key=f"chart_scroll_node_direct_{obj_id}_{final_width}"
        )
        st.markdown("</div>", unsafe_allow_html=True) # Closes the scroll container

    else:
        # --- UNIVERSAL BLOCK FOR JUPYTER / GOOGLE COLAB ---
        from IPython.display import display, HTML
        import plotly.io as pio

        chart_html = pio.to_html(fig, include_plotlyjs='cdn', full_html=False)
        scrollable_wrapper = f"""
        <div style="width: 100%; overflow-x: auto; overflow-y: hidden; white-space: nowrap; border: 1px solid #e6e6e6; padding: 5px;">
            {chart_html}
        </div>
        """
        display(HTML(scrollable_wrapper))


# Initialize the page configuration ONLY within an active Streamlit server session
if get_script_run_ctx() is not None:
    st.set_page_config(
        layout="wide",
        page_title="VizzBreeze | Data Visualization App",
        page_icon="",
        initial_sidebar_state="expanded"
    )
    # --- BRANDING IN SIDEBAR ---
    st.sidebar.title("VizzBreeze")
    st.sidebar.markdown("*From Chaos to Clarity*")
    st.sidebar.markdown("Developed by: [Mila Alex, CFA](https://linkedin.com)")
    st.sidebar.markdown("---")


# GLOBAL AUTOSIZING & STYLING CONFIGURATION FOR ALL PACKAGES
DEFAULT_PALETTE = "Warm Amber"  # Set your fallback brand color scheme here

# Securely inject custom CSS styles to override standard tab sizing limits
st.markdown(r"""
    <style>
        /* Scale up font styling inside tab headers */
        button[data-baseweb="tab"] {
            font-size: 22px !important;
            font-weight: bold !important;
        }
        button[data-baseweb="tab"] * {
            font-size: 22px !important;
            font-weight: bold !important;
            font-family: 'Arial', sans-serif !important;
        }
        [data-baseweb="tab-list"] button div {
            font-size: 22px !important;
            font-weight: bold !important;
        }
        
        /* Set minimum tab panel height to suppress viewport page jumps during chart re-rendering */
        .stTabs [data-baseweb="tab-panel"] {
            min-height: 800px !important;
        }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# GLOBAL SESSION STATE MATRIX & TYPOGRAPHY ANCHORS (PEP 8 COMPLIANT)
# =============================================================================
# Initialize global volumetric metrics, dashboard titles, and alignment layers
if "global_measure_col" not in st.session_state:
    st.session_state["global_measure_col"] = "Number of rows (Sample size)"

if "global_color_col" not in st.session_state:
    st.session_state["global_color_col"] = "Select Feature"

if "global_chart_title" not in st.session_state:
    st.session_state["global_chart_title"] = "Add Header"

if "global_title_size" not in st.session_state:
    st.session_state["global_title_size"] = 20

if "global_title_align" not in st.session_state:
    st.session_state["global_title_align"] = "Left"


def sync_global_session_variable(tab_key, state_target_key):
    """
    Unified high-performance callback engine to synchronize any local tab widget
    state modifications seamlessly into the global session state vector.
    """
    st.session_state[state_target_key] = st.session_state[tab_key]

# =========================================================================
# GLOBAL VISUAL CONFIGURATION (DEFAULT CHART SIZES)
# =========================================================================


# Global Dictionary of Palettes
COLOR_PALETTES = {
    "Vibrant": [
        "rgba(17, 138, 178, 0.7)", "rgba(42, 157, 143, 0.7)", "rgba(230, 57, 70, 0.7)",
        "rgba(244, 162, 97, 0.7)", "rgba(233, 196, 106, 0.7)", "rgba(69, 123, 157, 0.7)",
        "rgba(29, 53, 87, 0.7)", "rgba(241, 250, 238, 0.7)", "rgba(168, 218, 220, 0.7)", "rgba(141, 153, 174, 0.7)"
    ],
    "Consulting Premium": [
        "rgba(5, 28, 44, 0.7)", "rgba(34, 81, 255, 0.7)", "rgba(34, 34, 34, 0.7)",
        "rgba(162, 170, 173, 0.7)", "rgba(243, 193, 58, 0.7)", "rgba(0, 94, 184, 0.7)",
        "rgba(198, 207, 214, 0.7)", "rgba(77, 107, 123, 0.7)", "rgba(28, 45, 66, 0.7)", "rgba(119, 150, 162, 0.7)"
    ],
    "Classic Corporate": [
        "rgba(32, 28, 32, 0.7)", "rgba(156, 164, 20, 0.7)", "rgba(252, 236, 0, 0.7)",
        "rgba(112, 114, 112, 0.7)", "rgba(52, 112, 160, 0.7)", "rgba(172, 144, 196, 0.7)",
        "rgba(140, 24, 56, 0.7)", "rgba(252, 230, 148, 0.7)", "rgba(84, 110, 122, 0.7)", "rgba(207, 216, 220, 0.7)"
    ],
    "Warm Amber": [
        "rgba(255, 182, 0, 0.7)", "rgba(235, 140, 0, 0.7)", "rgba(208, 74, 2, 0.7)",
        "rgba(224, 48, 30, 0.7)", "rgba(219, 83, 106, 0.7)", "rgba(0, 0, 0, 0.7)",
        "rgba(45, 45, 45, 0.7)", "rgba(70, 70, 70, 0.7)", "rgba(125, 125, 125, 0.7)", "rgba(222, 222, 222, 0.7)"
    ],
    "E-Commerce Bright": [
        "rgba(0, 91, 255, 0.7)", "rgba(245, 0, 155, 0.7)", "rgba(255, 102, 0, 0.7)",
        "rgba(0, 204, 126, 0.7)", "rgba(123, 97, 255, 0.7)", "rgba(31, 32, 36, 0.7)",
        "rgba(141, 149, 161, 0.7)", "rgba(215, 222, 230, 0.7)", "rgba(255, 214, 0, 0.7)", "rgba(0, 180, 216, 0.7)"
    ],
    "Tech Titan Blue": [
        "rgba(0, 120, 215, 0.7)", "rgba(16, 124, 65, 0.7)", "rgba(242, 80, 34, 0.7)",
        "rgba(255, 185, 0, 0.7)", "rgba(70, 23, 143, 0.7)", "rgba(0, 102, 204, 0.7)",
        "rgba(240, 242, 245, 0.7)", "rgba(138, 141, 145, 0.7)", "rgba(44, 62, 80, 0.7)", "rgba(52, 73, 94, 0.7)"
    ],
    "Imperial Vermilion": [
        "rgba(186, 12, 47, 0.7)", "rgba(218, 165, 32, 0.7)", "rgba(224, 88, 43, 0.7)",
        "rgba(58, 93, 114, 0.7)", "rgba(47, 79, 79, 0.7)", "rgba(247, 241, 227, 0.7)",
        "rgba(44, 44, 44, 0.7)", "rgba(115, 115, 115, 0.7)", "rgba(197, 160, 89, 0.7)", "rgba(142, 40, 0, 0.7)"
    ],
    "Monochrome + Accent": [
        "rgba(252, 236, 0, 0.7)", "rgba(100, 116, 139, 0.7)", "rgba(148, 163, 184, 0.7)",
        "rgba(71, 85, 105, 0.7)", "rgba(203, 213, 225, 0.7)", "rgba(51, 65, 85, 0.7)",
        "rgba(226, 232, 240, 0.7)", "rgba(241, 245, 249, 0.7)", "rgba(30, 41, 59, 0.7)", "rgba(15, 23, 42, 0.7)"
    ]
}

palette_options = list(COLOR_PALETTES.keys())
default_index = palette_options.index(DEFAULT_PALETTE)

# 1. Defining all the necessary functions
def get_smart_brand_color(index, palette_list):
    # Returns a color from the palette. If index exceeds palette length,
    # it dynamically generates a cohesive intermediate blend of the brand colors.

    n = len(palette_list)
    if index < n:
        return palette_list[index]

    try:
        # Select two adjacent colors from the palette to blend together
        c1_str = palette_list[index % n]
        c2_str = palette_list[(index + 1) % n]

        # Helper to extract integers from rgba string
        def parse_rgba(s):
            # Extracts numbers between '(' and ')'
            nums = s.split('(')[1].split(')')[0].split(',')
            return [int(nums[0]), int(nums[1]), int(nums[2]), float(nums[3])]

        r1, g1, b1, a1 = parse_rgba(c1_str)
        r2, g2, b2, a2 = parse_rgba(c2_str)

        # Calculate a deterministic intermediate blend (50/50 mix)
        # We use a bit of index jitter so different overflow items don't get identical colors
        mix_factor = 0.5 + 0.1 * (index % 3 - 1)
        r_new = int(r1 * mix_factor + r2 * (1 - mix_factor))
        g_new = int(g1 * mix_factor + g2 * (1 - mix_factor))
        b_new = int(b1 * mix_factor + b2 * (1 - mix_factor))

        # Keep alpha locked to a readable visual structure
        return f"rgba({r_new}, {g_new}, {b_new}, 0.6)"

    # Robust fallback to neutral slate gray if parsing ever fails
    except (ValueError, TypeError, KeyError, IndexError):
        return "rgba(162, 170, 173, 0.6)"

# Global Color Blender


def get_blended_brand_color(index, base_palette):
    """
    Dynamically interpolates smooth intermediate shades
    between core brand colors when categorical features overflow the palette capacity.
    """

    n = len(base_palette)
    if index < n:
        return base_palette[index]
    try:
        c1 = base_palette[index % n]
        c2 = base_palette[(index + 1) % n]

        p1 = [float(x) for x in c1.replace("rgba(", "").replace(")", "").split(",")]
        p2 = [float(x) for x in c2.replace("rgba(", "").replace(")", "").split(",")]

        mix = 0.5 + 0.1 * ((index % 3) - 1)
        r_mix = int(p1[0] * mix + p2[0] * (1 - mix))
        g_mix = int(p1[1] * mix + p2[1] * (1 - mix))
        b_mix = int(p1[2] * mix + p2[2] * (1 - mix))

        return f"rgba({r_mix}, {g_mix}, {b_mix}, 0.6)"

    except (ValueError, TypeError, KeyError, IndexError):
        return "rgba(162, 170, 173, 0.6)"


def check_is_aggregated_data(df, stage_nodes, target_node):
    """
    Global structural topology detector. Ignores date and year columns
    to prevent false positive alerts on timestamps (e.g., 2023, 2024).
    """

    if not stage_nodes:
        return False

    all_active_nodes = list(dict.fromkeys(list(stage_nodes) + [target_node]))

    if len(all_active_nodes) >= 2:
        source_col = all_active_nodes[0]
        target_col = all_active_nodes[1]

        # --- NUMERIC & TEMPORAL COLUMN FILTER ---
        # Validate column data types: numeric or datetime series cannot act as graph process nodes
        if pd.api.types.is_numeric_dtype(df[source_col]) or pd.api.types.is_numeric_dtype(df[target_col]):
            return False
        if pd.api.types.is_datetime64_any_dtype(df[source_col]) or pd.api.types.is_datetime64_any_dtype(df[target_col]):
            return False

        # Safeguard against string-formatted years or dates (e.g., text literals '2023', '2024')
        # Skip validation if the column label matches any standard chronological keywords
        invalid_markers = ['year', 'date', 'time', 'год', 'дата', 'период']
        if any(m in str(source_col).lower() or m in str(target_col).lower() for m in invalid_markers):
            return False

        # Extract unique entries while filtering out raw 4-digit numeric string representations
        sources_series = df[source_col].dropna().astype(str).str.strip()
        targets_series = df[target_col].dropna().astype(str).str.strip()

        # Strip out standalone 4-digit combinations typical for fiscal or calendar years
        clean_sources = {x for x in sources_series.unique() if not (x.isdigit() and len(x) == 4)}
        clean_targets = {x for x in targets_series.unique() if not (x.isdigit() and len(x) == 4)}

        # Isolate genuine intersecting operational entity identifiers (network graph hubs)
        network_hubs = clean_sources & clean_targets

        if len(network_hubs) > 0:
            st.error(
                f"### Aggregated Network Detected\n"
                f"This dashboard view is optimized exclusively for **flat, un-aggregated transaction logs** "
                f"(e.g., *Client ➔ Fund ➔ Asset*).\n\n"
                f"The system detected that elements like `{', '.join(list(network_hubs)[:3])}` act simultaneously as both senders and receivers. "
                f"Please ensure your selected columns represent independent process stages or upload a flat dataset."
            )
            return True  # Data structure is aggregated (invalid context)

    return False  # Data structure is flat (valid transaction log context)


def generate_parcats(df, stage_nodes, target_node, value_col, width_px, height_px, selected_palette=None, unit_divider=1.0, force_shuffle=False,
                     chart_title="Parallel Categories Flow", title_size=20, title_x=0.0):

    # 1. Fallback to the global default scheme name if no custom palette is explicitly passed
    chosen_scheme = selected_palette if selected_palette is not None else DEFAULT_PALETTE

    # 2. Extract the actual list of HEX colors from the dictionary if a string label is provided
    if isinstance(chosen_scheme, str):
        final_palette = COLOR_PALETTES.get(chosen_scheme, ["#FFBF00", "#FF7E00"]) # Fallback lists
    else:
        final_palette = chosen_scheme

    # 3. Securely clone the localized list and execute the pseudo-random positioning layout
    working_colors = final_palette.copy()
    if isinstance(force_shuffle, int):
        random.seed(force_shuffle)
    random.shuffle(working_colors)

    if not stage_nodes:
        return go.Figure()

    df_clean = df.copy()

    # Consolidate all user-selected nodes into a unified sequential stage list
    all_active_nodes = list(dict.fromkeys(list(stage_nodes) + [target_node]))

    # Enforce data type consistency: cast all categorical keys to standardized trimmed strings
    for col in all_active_nodes:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    # Initialize volume metrics and handle data un-aggregation modes
    if value_col == "Number of rows (Sample size)":
        df_clean['__volume__'] = 1
        value_col_internal = '__volume__'
    else:
        df_clean[value_col] = pd.to_numeric(df_clean[value_col], errors='coerce').fillna(0)
        value_col_internal = value_col

    # Directly group the flat transactional dataset by the user-defined active stages sequence
    df_grouped = df_clean.groupby(all_active_nodes)[value_col_internal].sum().reset_index(name='volume_val')
    display_nodes = all_active_nodes

    df_grouped['volume_val'] = df_grouped['volume_val'] / unit_divider
    df_grouped = df_grouped[df_grouped['volume_val'] > 0].reset_index(drop=True)

    if df_grouped.empty:
        return go.Figure()

    # Apply flow gradient sorting mapped to the primary origin node dimensions
    color_col_name = display_nodes[0]
    unique_color_vals = sorted(df_grouped[color_col_name].dropna().unique())

    # Fallback interpolation helper for color assignments
    def get_blended_brand_color(index, palette):
        return palette[index % len(palette)]

    local_color_map = {}
    for i, val in enumerate(unique_color_vals):
        local_color_map[val] = get_blended_brand_color(i, working_colors)

    df_grouped["sort_c"] = df_grouped[color_col_name].map({v: i for i, v in enumerate(unique_color_vals)})
    df_grouped = df_grouped.sort_values("sort_c").reset_index(drop=True)
    df_grouped["color_val"] = df_grouped[color_col_name].map(local_color_map)

    # Compute node totals to display volume metrics along category axes
    node_totals = {}
    for col in display_nodes:
        totals = df_grouped.groupby(col)['volume_val'].sum()
        for val, s in totals.items():
            node_totals[f"{col}::{val}"] = s

    # Generate layout dimensions for the Plotly Parcats construct
    parcats_dimensions = []
    for idx, col in enumerate(display_nodes):
        unique_vals_in_axis = sorted(df_grouped[col].unique())

        # Enforce scoping via compound delimiters to separate identical keys across stages
        category_array = [f"{col}::{v}" for v in unique_vals_in_axis]
        column_values_as_keys = df_grouped[col].apply(lambda x: f"{col}::{x}").tolist()

        # Generate formatted axis labels using clean spacing standard without HTML span hacks
        tick_text = []
        for v in unique_vals_in_axis:
            # Construct the unique dictionary compound key safely
            lookup_key = f"{col}::{v}"
            scaled_volume = node_totals.get(lookup_key, 0)

            # Assign numerical precision based on active data scale context
            formatted_vol = f"{scaled_volume:,.1f}" if unit_divider > 1 or (scaled_volume % 1 != 0) else f"{scaled_volume:,.0f}"

            # Replace standard commas with sleek, clean thin spacing layout
            formatted_vol = formatted_vol.replace(",", " ")

            # UNIFIED: Pure text token array. Plotly vectors handle the fonts natively via tickfont
            tick_text.append(f"{str(v)} - {formatted_vol}")

        if col == target_node:
            axis_label = f"FINAL DESTINATION ({col.upper()})"
        else:
            axis_label = f"{idx+1}. STAGE ({col.upper()})"

        parcats_dimensions.append({
            # "label": axis_label,
            "values": column_values_as_keys,
            "categoryorder": "array",
            "categoryarray": category_array,
            "ticktext": tick_text
        })

    # Render smooth continuous flow streams using high-fidelity hspline shapes
    fig = go.Figure(data=[go.Parcats(
        dimensions=parcats_dimensions,
        line={"color": df_grouped["color_val"].tolist(), "shape": "hspline"},
        counts=df_grouped["volume_val"].tolist(),

        # UNIFIED TYPOGRAPHY STYLE: Identical font parameters matched with the Funnel trace settings
        labelfont=dict(color="#000000", size=11, family="Arial"),
        tickfont=dict(color="#000000", size=11, family="Arial"),

        arrangement='perpendicular',
        hoveron='category',
        hoverinfo='count+probability'
    )])


    # DYNAMIC ANNOTATION ENGINE: Automatically builds centered titles for each column layer
    # Stage 1 is at X=0 (left), Stage 2 (if exists) or Destination is distributed evenly up to X=1 (right)
    num_stages = len(stage_nodes)
    chart_annotations = []

    # 1. Generate annotations for sequential stages
    for idx, node in enumerate(stage_nodes):
        # Calculate strict horizontal positioning between 0.0 and 1.0
        x_pos = idx / num_stages if num_stages > 0 else 0.0
        chart_annotations.append(dict(
            x=x_pos, y=1.07, # y=1.07 elevates text safely above the column nodes
            xref="paper", yref="paper",
            text=f"{idx + 1}. STAGE ({str(node).upper()})",
            showarrow=False,
            font=dict(size=12, family="Arial", color="#000000"),
            xanchor="center" if x_pos > 0 and x_pos < 1 else ("left" if x_pos == 0 else "right")
        ))

    # 2. Append the terminal destination layer annotation at the exact right boundary (X=1.0)
    chart_annotations.append(dict(
        x=1.0, y=1.07,
        xref="paper", yref="paper",
        text=f"FINAL DESTINATION ({str(target_node).upper()})",
        showarrow=False,
        font=dict(size=12, family="Arial", color="#000000"),
        xanchor="right"
    ))

    # UNIFIED LAYOUT ARCHITECTURE: Matched with the corporate reporting layout standard
    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=title_size), x=title_x, xanchor='auto'),
        plot_bgcolor="white", paper_bgcolor="white",
        height=height_px,
        width=width_px if width_px else None,
        autosize=True if not width_px else False,
        annotations=chart_annotations,

        # FIXED VERTICAL GAP: Increased t (top margin) to 100 to push the chart down and restore the header spacing
        margin=dict(l=150, r=150, t=100, b=40),
        # Sync hover format masks with thin spacing delimiters standard
        separators=" .",

        # Lock high-contrast text strings inside tooltips safely on the layout canvas layer
        hoverlabel=dict(
            font_size=12,
            font_color="#000000"
        )
    )

    return fig


def generate_funnel_chart(df, stage_nodes, target_node, value_col, selected_route_dict, width_px, height_px, selected_palette=None, unit_divider=1.0, force_shuffle=False,
                          chart_title="Pipeline Stage Conversion", title_size=20, title_x=0.0):

    # 1. Fallback to the global default scheme name if no custom palette is explicitly passed
    chosen_scheme = selected_palette if selected_palette is not None else DEFAULT_PALETTE

    # 2. Extract the actual list of HEX colors from the dictionary if a string label is provided
    if isinstance(chosen_scheme, str):
        final_palette = COLOR_PALETTES.get(chosen_scheme, ["#FFBF00", "#FF7E00"]) # Fallback lists
    else:
        final_palette = chosen_scheme

    # 3. Securely clone the localized list and execute the pseudo-random positioning layout
    working_colors = final_palette.copy()
    if isinstance(force_shuffle, int):
        random.seed(force_shuffle)
    random.shuffle(working_colors)

    if not stage_nodes:
        return go.Figure()

    df_base = df.copy()

    # Consolidate categorical active tracking keys based on user selections
    all_active_nodes = list(dict.fromkeys(list(stage_nodes) + [target_node]))
    for col in all_active_nodes:
        df_base[col] = df_base[col].astype(str).str.strip()

    if value_col == "Number of rows (Sample size)":
        df_base['metric_val'] = 1
        value_col_internal = 'metric_val'
    else:
        df_base[value_col] = pd.to_numeric(df_base[value_col], errors='coerce').fillna(0)
        value_col_internal = value_col

    funnel_labels = []
    funnel_values = []

    display_nodes = list(stage_nodes)

    for idx, col in enumerate(display_nodes):
        current_chosen_val = str(selected_route_dict.get(col, '')).strip()

        # Build a progressive cascading filter based on user-selected selector pathways
        df_step_filter = df_base.copy()
        for j in range(idx + 1):
            past_col = display_nodes[j]
            past_val = str(selected_route_dict.get(past_col, '')).strip()
            df_step_filter = df_step_filter[df_step_filter[past_col].astype(str) == past_val]

        step_volume = float(df_step_filter[value_col_internal].sum())
        funnel_labels.append(f"Stage {idx+1}: {col.upper()} ({current_chosen_val})")
        funnel_values.append(step_volume)

    # Render the final target node explicitly based on strict end-to-end path mapping
    if target_node not in display_nodes:
        final_chosen_val = str(selected_route_dict.get(target_node, '')).strip()
        df_final_filter = df_base.copy()
        for col in display_nodes + [target_node]:
            val = str(selected_route_dict.get(col, '')).strip()
            df_final_filter = df_final_filter[df_final_filter[col].astype(str) == val]

        v_end = float(df_final_filter[value_col_internal].sum())
        funnel_labels.append(f"Destination: {target_node.upper()} ({final_chosen_val})")
        funnel_values.append(v_end)

    funnel_values = [v / unit_divider for v in funnel_values]
    if not funnel_values:
        return go.Figure()

    funnel_text_preformatted = []
    initial_volume = funnel_values[0] if funnel_values else 1.0

    for idx, val in enumerate(funnel_values):
        val_str = f"{val:,.1f}" if unit_divider > 1 or (val % 1 != 0) else f"{val:,.0f}"
        val_str = val_str.replace(",", " ")
        pct_initial = (val / initial_volume) if initial_volume > 0 else 0.0
        pct_str = f"{pct_initial:.1%}"
        funnel_text_preformatted.append(f"{val_str} ({pct_str})")

    def get_blended_brand_color(index, palette):
        return palette[index % len(palette)]

    color_sequence = [get_blended_brand_color(i, working_colors) for i in range(len(funnel_labels))]

    fig = go.Figure(go.Funnel(
        y=funnel_labels,
        x=funnel_values,
        text=funnel_text_preformatted,
        textinfo="text",
        insidetextfont=dict(color="#000000", size=11, family="Arial"),
        textfont=dict(color="#000000", size=11, family="Arial"),
        marker=dict(color=color_sequence, line=dict(color="#FFFFFF", width=2))
    ))

    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=title_size), x=title_x, xanchor='auto'),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=height_px,
        width=width_px if width_px else None, # Если None, то график будет растягиваться
        autosize=True if not width_px else False,
        margin=dict(l=250, r=40, t=60, b=60),
        separators=" ."
    )
    return fig


def generate_stacked_bar_chart(df, stage_nodes, target_node, value_col, width_px, height_px, selected_palette=None, unit_divider=1.0, force_shuffle=False,
                               chart_title="Structural Composition Breakdown", title_size=20, title_x=0.0):

    # 1. Fallback to the global default scheme name if no custom palette is explicitly passed
    chosen_scheme = selected_palette if selected_palette is not None else DEFAULT_PALETTE

    # 2. Extract the actual list of HEX colors from the dictionary if a string label is provided
    if isinstance(chosen_scheme, str):
        final_palette = COLOR_PALETTES.get(chosen_scheme, ["#FFBF00", "#FF7E00"]) # Fallback lists
    else:
        final_palette = chosen_scheme

    # 3. Securely clone the localized list and execute the pseudo-random positioning layout
    working_colors = final_palette.copy()
    if isinstance(force_shuffle, int):
        random.seed(force_shuffle)
    random.shuffle(working_colors)

    if not stage_nodes:
        return go.Figure()

    df_clean = df.copy()

    # Consolidate all active nodes into a unique chronological list
    all_active_nodes = list(dict.fromkeys(list(stage_nodes) + [target_node]))

    # Enforce data type consistency: cast categorical attributes to strings
    for col in all_active_nodes:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    # Initialize volume metrics and handle data un-aggregation modes
    if value_col == "Number of rows (Sample size)":
        df_clean['__volume__'] = 1
        value_col_internal = '__volume__'
    else:
        df_clean[value_col] = pd.to_numeric(df_clean[value_col], errors='coerce').fillna(0)
        value_col_internal = value_col

    # Multi-stage routing layout for detailed un-aggregated transaction records
    x_cols = list(stage_nodes)

    # Create the horizontal multistep process label on the X-axis (e.g., Client_1 ➔ Fund_A)
    # df_clean['COMPOSITE_X'] = df_clean[x_cols].agg(' ➔ '.join, axis=1)

    # 1. Check if the column list is not empty
    if not x_cols:
        # If no columns are selected, create a placeholder to prevent the chart from crashing
        df_clean['COMPOSITE_X'] = "No stages selected"
    else:
        # 2. Safely cast all elements in the selected columns to strings
        # and then join them using the arrow separator
        df_clean['COMPOSITE_X'] = df_clean[x_cols].astype(str).agg(' ➔ '.join, axis=1)

    # Directly aggregate flat transaction items using a high-performance single groupby pass
    df_final = df_clean.groupby(['COMPOSITE_X', target_node])[value_col_internal].sum().reset_index()
    df_final.columns = ['X_AXIS', 'COLOR_CATEGORIES', 'VOLUME']

    df_final = df_final[df_final['VOLUME'] > 0].reset_index(drop=True)

    if df_final.empty:
        return go.Figure()

    # FIXED: Extracted single data scaling pass to prevent exponential division bugs
    df_final['VOLUME'] = df_final['VOLUME'] / unit_divider
    val_format = ":,.1f" if unit_divider > 1 else ":,.0f"
    tick_format = ",.1f" if unit_divider > 1 else ",.0f"

    # Extract distinct dimensions for rendering
    unique_x = sorted(df_final['X_AXIS'].unique())
    unique_cats = sorted(df_final['COLOR_CATEGORIES'].unique())

    # Internal helper fallback for color generation
    def get_blended_brand_color(index, palette):
        return palette[index % len(palette)]

    color_map = {cat: get_blended_brand_color(i, working_colors) for i, cat in enumerate(unique_cats)}

    fig = go.Figure()

    # Distribute volumetric metrics sequentially into categorical bar stacks
    for cat in unique_cats:
        df_cat = df_final[df_final['COLOR_CATEGORIES'] == cat]
        volumes_y = []

        # Build a safe string template mask to decouple nested brace structures
        bar_hovertemplate = (
            "<b>Category:</b> " + str(cat) + "<br>"
            "<b>Path:</b> %{x}<br>"
            "<b>Volume:</b> %{y" + val_format + "}<br>"
            "<extra></extra>"
        )

        for x_val in unique_x:
            val_row = df_cat[df_cat['X_AXIS'] == x_val]
            volumes_y.append(float(val_row['VOLUME'].iloc[0]) if not val_row.empty else 0.0)

        # GENERATE STATIC LABELS:
        # If the metric volume is positive, format the output text string, otherwise leave blank
        text_labels = []
        for val in volumes_y:
            if val > 0:
                # Format to decimal string if divider is active or floating value context exists
                val_str = f"{val:,.1f}" if unit_divider > 1 or (val % 1 != 0) else f"{val:,.0f}"
                text_labels.append(val_str.replace(",", " "))  # Inject clean space separations
            else:
                text_labels.append("")

        fig.add_trace(go.Bar(
            x=unique_x,
            y=volumes_y,
            name=str(cat),
            text=text_labels,
            textposition='inside',
            textfont=dict(color='black', size=11, family='Arial'),
            insidetextanchor='middle',
            hovertemplate=bar_hovertemplate,
            marker=dict(color=color_map[cat], line=dict(color='#FFFFFF', width=0.5))
        ))


    # Apply corporate reporting layout architecture using the British dot standard
    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=title_size), x=title_x, xanchor='auto'),
        barmode='stack', plot_bgcolor="white", paper_bgcolor="white",
        height=height_px,
        width=width_px if width_px else None,
        autosize=True if not width_px else False,
        margin=dict(l=60, r=40, t=60, b=120),
        xaxis=dict(title=dict(
                text=' ➔ '.join([str(c).upper() for c in x_cols]),
                font=dict(size=12, family="Arial", color="#1f1f1f"),
                standoff=20
            ), showgrid=False, linecolor='#000000', tickangle=270),
        yaxis=dict(title=dict(
                text=value_col,
                font=dict(size=12, family="Arial", color="#1f1f1f")
            ), showgrid=True, gridcolor='#E5E5E5', linecolor='#000000', tickformat=tick_format),
        legend=dict(
            title=dict(text=f"<b>{target_node.upper()}</b>", font=dict(size=12)),
            itemsizing='constant', orientation="v", yanchor="top", y=1, xanchor="left", x=1.02
        ),
        # FIXED: Synced hover format masks with thin spacing delimiters standard
        separators=" ."
    )
    return fig

def generate_bento_treemap(df, id_col, value_col, width_px, height_px, selected_palette=None, unit_divider=1.0, force_shuffle=False,
                           chart_title="Bento Treemap Dashboard", title_size=20, title_x=0.0):

    # 1. Fallback to the global default scheme name if no custom palette is explicitly passed
    chosen_scheme = selected_palette if selected_palette is not None else DEFAULT_PALETTE

    # 2. Extract the actual list of HEX colors from the dictionary if a string label is provided
    if isinstance(chosen_scheme, str):
        final_palette = COLOR_PALETTES.get(chosen_scheme, ["#FFBF00", "#FF7E00"]) # Fallback lists
    else:
        final_palette = chosen_scheme

    # 3. Securely clone the localized list and execute the pseudo-random positioning layout
    working_colors = final_palette.copy()
    if isinstance(force_shuffle, int):
        random.seed(force_shuffle)
    random.shuffle(working_colors)

    df_bento_clean = df.copy()

    # Enforce type consistency across identifier columns
    if isinstance(id_col, list):
        active_cols = list(dict.fromkeys(id_col))
    else:
        active_cols = [id_col]

    for col in active_cols:
        df_bento_clean[col] = df_bento_clean[col].astype(str).str.strip()

    # Initialize volumetric metrics and handle data un-aggregation modes
    if value_col == "Number of rows (Sample size)":
        df_bento_clean['__volume__'] = 1
        value_col_internal = '__volume__'
    else:
        df_bento_clean[value_col] = pd.to_numeric(df_bento_clean[value_col], errors='coerce').fillna(0)
        value_col_internal = value_col

    # If a list of columns is active, combine them into an end-to-end transactional track
    if len(active_cols) > 1:
        df_bento_clean['TARGET_ID'] = df_bento_clean[active_cols].agg(' ➔ '.join, axis=1)
    else:
        df_bento_clean['TARGET_ID'] = df_bento_clean[active_cols[0]]

    # Directly aggregate flat transaction items using a single high-performance groupby pass
    df_bento_grouped = df_bento_clean.groupby('TARGET_ID')[value_col_internal].sum().reset_index(name='bento_val')
    df_bento_grouped.columns = ['TARGET_ID', 'bento_val']

    # Filter non-zero items and capture top-tier volumetric records
    df_bento_grouped = df_bento_grouped[df_bento_grouped['bento_val'] > 0]
    df_bento_grouped['bento_val'] = df_bento_grouped['bento_val'] / unit_divider
    df_bento_grouped = df_bento_grouped.sort_values(by='bento_val', ascending=False).head(15).reset_index(drop=True)

    if df_bento_grouped.empty:
        return go.Figure()

    # Calculate global metrics context for accurate percentage shares pre-formatting
    total_bento_sum = df_bento_grouped['bento_val'].sum()

    labels = df_bento_grouped['TARGET_ID'].astype(str).tolist()
    values = df_bento_grouped['bento_val'].astype(float).tolist()
    parents = [""] * len(labels)

    # Pre-format layout text strings via Python core execution to prevent string parsing errors
    text_labels_preformatted = []
    for idx, row in df_bento_grouped.iterrows():
        node_name = str(row['TARGET_ID'])
        node_val = float(row['bento_val'])
        node_share = (node_val / total_bento_sum) if total_bento_sum > 0 else 0.0

        # Enforce British numerical format: space for thousands, dot for decimals
        val_str = f"{node_val:,.1f}" if unit_divider > 1 or (node_val % 1 != 0) else f"{node_val:,.0f}"
        val_str = val_str.replace(",", " ")

        share_str = f"{node_share:.1%}"

        text_labels_preformatted.append(
            f"<b>{node_name}</b><br><br>"
            f"Volume: {val_str}<br>"
            f"Share: {share_str}"
        )

    def get_blended_brand_color(index, palette):
        return palette[index % len(palette)]

    color_sequence = [get_blended_brand_color(i, working_colors) for i in range(len(labels))]

    # Render high-fidelity tiled architecture with clean pre-formatted text maps
    fig_bento = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        text=text_labels_preformatted,
        textinfo="text",
        hoverinfo="text",
        marker=dict(colors=color_sequence, line=dict(color="#FFFFFF", width=2)),
        textfont=dict(size=14, color="black")
    ))


    # Apply corporate reporting layout architecture using the British dot standard
    fig_bento.update_layout(
        title=dict(text=chart_title, font=dict(size=title_size), x=title_x, xanchor='auto'),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=height_px,
        width=width_px if width_px else None,
        autosize=True if not width_px else False,
        margin=dict(l=20, r=20, t=60, b=20),
        separators="."
    )
    return fig_bento


def generate_heatmap(df, x_col, y_col, value_col, width_px, height_px, selected_palette=None, unit_divider=1.0, force_shuffle=False,
                     chart_title="Category Intersection & Heatmap", title_size=20, title_x=0.0,
                     show_annot=False):

    # 1. Fallback to the global default scheme name if no custom palette is explicitly passed
    chosen_scheme = selected_palette if selected_palette is not None else DEFAULT_PALETTE

    # 2. Extract the actual list of HEX colors from the dictionary if a string label is provided
    if isinstance(chosen_scheme, str):
        final_palette = COLOR_PALETTES.get(chosen_scheme, ["#FFBF00", "#FF7E00"]) # Fallback lists
    else:
        final_palette = chosen_scheme

    # 3. Securely clone the localized list and execute the pseudo-random positioning layout
    working_colors = final_palette.copy()
    if isinstance(force_shuffle, int):
        random.seed(force_shuffle)
    random.shuffle(working_colors)

    if len(working_colors) > 0:
        base_color = working_colors[0]
    else:
        base_color = "rgba(34, 81, 255, 0.6)"

    # Construct a continuous gradient map targeting a selected structural color
    colorscale = [[0.0, "rgba(245,247,250,1)"], [1.0, base_color]]

    df_clean = df.copy()

    # Enforce type consistency across categorical coordinate variables
    active_cols = list(dict.fromkeys([x_col, y_col]))
    for col in active_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    # Initialize volumetric metrics and handle data un-aggregation modes
    if value_col == "Number of rows (Sample size)":
        df_clean['__volume__'] = 1
        value_col_internal = '__volume__'
    else:
        df_clean[value_col] = pd.to_numeric(df_clean[value_col], errors='coerce').fillna(0)
        value_col_internal = value_col

    # Directly assemble the intersection grid layout using native high-performance pivot operations
    if value_col == "Number of rows (Sample size)":
        df_pivot = df_clean.pivot_table(index=y_col, columns=x_col, aggfunc='size', fill_value=0)
    else:
        df_pivot = df_clean.pivot_table(index=y_col, columns=x_col, values=value_col_internal, aggfunc='sum', fill_value=0)

    if df_pivot.empty:
        return go.Figure()

    # Apply continuous scalar scaling factor transformation to the pivot table cells
    df_pivot = df_pivot / unit_divider

    z_data = df_pivot.values
    x_labels = df_pivot.columns.tolist()
    y_labels = df_pivot.index.tolist()

    # Assign layout formatting precision mapped to the active unit context
    tick_format = ",.1f" if unit_divider > 1 else ",.0f"
    val_format = ":,.1f" if unit_divider > 1 else ":,.0f"

    # Create an identical matrix containing formatted string weights with blank spaces for thousands
    text_data = []
    for row in z_data:
        text_row = []
        for val in row:
            if val > 0:
                val_str = f"{val:,.1f}" if unit_divider > 1 or (val % 1 != 0) else f"{val:,.0f}"
                text_row.append(val_str.replace(",", " ")) # Clean thin spacing layout standard
            else:
                text_row.append("") # Keep zero cells completely clean and textless
        text_data.append(text_row)

    # Base configuration for the native Plotly Heatmap trace object
    heatmap_trace = go.Heatmap(
        z=z_data,
        x=x_labels,
        y=y_labels,
        colorscale=colorscale,
        showscale=True,
        xgap=2, ygap=2,
        hovertemplate="<b>X:</b> %{x}<br><b>Y:</b> %{y}<br><b>Value:</b> %{z" + val_format + "}<extra></extra>",
        colorbar=dict(tickformat=tick_format)
    )

    # FIXED: Inject annotations dynamically ONLY if the checkbox flag evaluates to True
    if show_annot:
        heatmap_trace.text = text_data
        heatmap_trace.texttemplate = "%{text}"
        # Set text font style context to ensure pure black high-contrast values inside cells
        heatmap_trace.textfont = dict(color="#000000", size=11, family="Arial")

    fig = go.Figure(data=heatmap_trace)


    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=title_size), x=title_x, xanchor='auto'),
        height=height_px,
    # width=width_px if width_px else None,
    # autosize=True if not width_px else False,
        margin=dict(l=120, r=40, t=60, b=120),
        xaxis=dict(tickangle=0, type='category', scaleanchor="y", scaleratio=1),
        yaxis=dict(type='category'),
        plot_bgcolor="white",
        paper_bgcolor="white",
        separators=" ."
    )
    return fig


def generate_outliers_chart(df, stage_col, target_col, value_col,
                            width_px, height_px, agg_func="sum", selected_palette=None, unit_divider=1.0, force_shuffle=False,
                            chart_title="Transaction Outlier & Anomaly Analysis", title_size=20, title_x=0.0):

    # 1. Fallback to the global default scheme name if no custom palette is explicitly passed
    chosen_scheme = selected_palette if selected_palette is not None else DEFAULT_PALETTE

    # 2. Extract the actual list of HEX colors from the dictionary if a string label is provided
    if isinstance(chosen_scheme, str):
        final_palette = COLOR_PALETTES.get(chosen_scheme, ["#FFBF00", "#FF7E00"]) # Fallback lists
    else:
        final_palette = chosen_scheme

    # 3. Securely clone the localized list and execute the pseudo-random positioning layout
    working_colors = final_palette.copy()
    if isinstance(force_shuffle, int):
        random.seed(force_shuffle)
    random.shuffle(working_colors)

    df_clean = df.copy()

    # Consolidate categorical active tracking keys from the new standalone parameters
    all_active_nodes = list(dict.fromkeys([stage_col, target_col]))

    for col in all_active_nodes:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # Initialize quantitative transaction fields
    if value_col == "Number of rows (Sample size)":
        df_clean['__volume__'] = 1
        value_col_internal = '__volume__'
    else:
        df_clean[value_col] = pd.to_numeric(df_clean[value_col], errors='coerce').fillna(0)
        value_col_internal = value_col

    # Validate that the passed aggregation function is supported by pandas
    if agg_func not in ["sum", "max", "mean", "min", "count"]:
        agg_func = "sum"

    # Directly assemble composite path sequences using a clean high-performance groupby pass
    df_clean['COMPOSITE_PATH'] = df_clean[stage_col] + " ➔ " + df_clean[target_col]

    df_analysis = df_clean.groupby('COMPOSITE_PATH')[value_col_internal].agg(agg_func).reset_index()
    df_analysis.columns = ['ENTITY_ID', 'VALUE_METRIC']

    df_analysis = df_analysis[df_analysis['VALUE_METRIC'] > 0].reset_index(drop=True)

    # Scale data values down by the user-selected scale factor modifier
    df_analysis['VALUE_METRIC'] = df_analysis['VALUE_METRIC'] / unit_divider

    if df_analysis.empty:
        return go.Figure()

    # --- ADVANCED STATISTICAL OUTLIER DETECTION (IQR METHOD) ---
    q1 = np.percentile(df_analysis['VALUE_METRIC'], 25) if len(df_analysis) >= 4 else df_analysis['VALUE_METRIC'].min()
    q3 = np.percentile(df_analysis['VALUE_METRIC'], 75) if len(df_analysis) >= 4 else df_analysis['VALUE_METRIC'].max()
    iqr = q3 - q1

    # Establish upper bound boundaries for anomaly validation
    upper_bound = q3 + 1.5 * iqr if iqr > 0 else df_analysis['VALUE_METRIC'].mean() * 1.5

    # Classify nodes based on the calculated metric constraints
    df_analysis['IS_OUTLIER'] = df_analysis['VALUE_METRIC'] > upper_bound
    df_analysis = df_analysis.sort_values(by='VALUE_METRIC', ascending=True).reset_index(drop=True)

    # Distribute tracking colors from corporate identity matrices
    base_color = working_colors[0] if len(working_colors) > 0 else "rgb(0, 94, 184)"
    outlier_color = "rgb(217, 83, 79)"

    colors = [outlier_color if row['IS_OUTLIER'] else base_color for _, row in df_analysis.iterrows()]

    # Resolve layout formatting masks based on the active scale metrics context
    val_format = ":,.1f" if unit_divider > 1 else ":,.0f"
    tick_format = ",.1f" if unit_divider > 1 else ",.0f"

    # Construct safe string template mask to decouple nested brace structures
    outliers_hovertemplate = (
        "<b>Sub-Route/Batch:</b> %{y}<br>"
        "<b>Value:</b> %{x" + val_format + "}<br>"
        "<b>Status:</b> %{customdata}<extra></extra>"
    )

    # Render a high-fidelity visual audit report layout
    fig = go.Figure(go.Bar(
        y=df_analysis['ENTITY_ID'],
        x=df_analysis['VALUE_METRIC'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='#FFFFFF', width=0.5)),
        hovertemplate=outliers_hovertemplate,
        # UPDATED: More universal status labels fit for both logs and finance
        customdata=["Anomaly (Outlier)" if out else "Normal Route" for out in df_analysis['IS_OUTLIER']]
    ))

    # NEW: Automatically switch the X-axis label context based on the active agg_func parameter
    if agg_func == "max":
        xaxis_label = f"MAX SINGLE-RUN VOLUME ({value_col.upper()})"
    elif agg_func == "mean":
        xaxis_label = f"AVERAGE VOLUME ({value_col.upper()})"
    elif agg_func == "min":
        xaxis_label = f"MIN SINGLE-RUN VOLUME ({value_col.upper()})"
    elif agg_func == "count":
        xaxis_label = f"NUMBER OF ({value_col.upper()})"
    else:
        xaxis_label = f"TOTAL ACCUMULATED VOLUME ({value_col.upper()})"

    # Apply corporate dashboard presentation configuration using the British dot standard
    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=title_size), x=title_x, xanchor='auto'),
        plot_bgcolor="white", paper_bgcolor="white",
        height=height_px,     width=width_px if width_px else None,
        autosize=True if not width_px else False,
        # UPDATED: Injected dynamic left margin calculation to prevent text truncation
        margin=dict(l=120, r=40, t=60, b=60),
        xaxis=dict(title=xaxis_label, # UPDATED: Using dynamic context label here
                   showgrid=True,
                   gridcolor='#E5E5E5',
                   linecolor='#000000',
                   tickformat=tick_format,
                   dtick=1 if (unit_divider == 1.0 and df_analysis['VALUE_METRIC'].max() < 10) else None),
        yaxis=dict(title="PROCESS PATHS / ENTITIES",
                   showgrid=False,
                   linecolor='#000000',
                   type='category'),
        separators=" ."
    )

    fig.add_vline(x=upper_bound,
                  line_width=1.5,
                  line_dash="dash",
                  line_color="orange",
                  annotation_text=f"Anomaly Threshold",
                  annotation_position="bottom right",
                  )

    return fig

# =============================================================================
# INGESTION & PIPELINE RUNTIME LOGIC (DASHBOARD CONTROL WORKSPACE)
# =============================================================================

uploaded_file = st.file_uploader("Upload Excel File",
                                 type=["xlsx"],
                                 label_visibility="collapsed")

if uploaded_file is not None:
    opt_table = pd.read_excel(uploaded_file)

    # Initialize a reactive checkbox layout element to preview transactional logs
    show_raw_data = st.checkbox("View Uploaded Data Table", key="checkbox_raw_data")
    all_columns = list(opt_table.columns)

    # Compile numerical fields securely and assign standardized fallback metrics
    found_numeric = list(opt_table.select_dtypes(include=[np.number]).columns)
    numeric_cols = ["Number of rows (Sample size)"] + found_numeric

    # Expand interactive data workspace if the layout preview checkbox is checked
    if show_raw_data:
        st.subheader("Uploaded Data View")
        st.dataframe(opt_table,
                     use_container_width=False,
                     column_config={
                         col: st.column_config.NumberColumn(format="%d")
                         for col in found_numeric
                     }
                     )
        st.markdown("---")

    # --- SIDEBAR PRESENTATION & CONFIGURATION LAYER ---
    st.sidebar.markdown("Chart Print Dimensions (A4 Optimization)")

    # Capture target printable dimensions directly via metric scale sliders
    chart_width_cm = st.sidebar.slider(
        "Width (cm):",
        min_value=15, max_value=100, value=30, step=1,
        key="width_cm_slider"
    )
    chart_height_cm = st.sidebar.slider(
        "Height (cm):",
        min_value=10, max_value=40, value=15, step=1,
        key="height_cm_slider"
    )

    # Convert standard physical dimensions (cm) to target logical canvas parameters (px @ 96 DPI)
    chart_width_px = int(chart_width_cm * (96 / 2.54))
    chart_height_px = int(chart_height_cm * (96 / 2.54))

    # Display operational logging parameters to track live canvas scaling properties
    st.sidebar.caption(f"*Rendered Web Size:* **{chart_width_px}px** × **{chart_height_px}px**")
    st.sidebar.markdown("---")

    st.sidebar.subheader("Color Palettes")

    # Dropdown interface mapping targeting system theme color layouts
    selected_palette = st.sidebar.selectbox(
        "",
        options=list(COLOR_PALETTES.keys()),
        index=default_index
    )

    chosen_colors = COLOR_PALETTES[selected_palette]

    # Stateful session memory layer management for asset maps cache flushing
    if "previous_palette_name" not in st.session_state:
        st.session_state["previous_palette_name"] = selected_palette

    if st.session_state["previous_palette_name"] != selected_palette:
        st.session_state["previous_palette_name"] = selected_palette
        if "color_map" in st.session_state:
            del st.session_state.color_map
        if "color_map_agg" in st.session_state:
            del st.session_state.color_map_agg
        st.session_state["shuffle_seed_modifier"] = 0

    st.session_state["selected_palette"] = selected_palette

    # Maintain stateful cryptographic tracking variables for stable permutations
    if "current_seed" not in st.session_state:
        st.session_state["current_seed"] = 42

    # Allocate a random seeding modifier upon execution to invalidate outdated tracking map configurations
    if st.sidebar.button("Shuffle Colors"):
        st.session_state["current_seed"] = random.randint(0, 100000)
        if "color_map" in st.session_state:
            del st.session_state.color_map
        if "color_map_agg" in st.session_state:
            del st.session_state.color_map_agg

    st.sidebar.markdown("---")

    st.sidebar.subheader("Data Scale & Formatting")

    # User selects how much to divide the raw values (1 = no division, 1000 = thousands, etc.)
    unit_options = {"Original Values (1)": 1.0, "Thousands (1 000)": 1000.0, "Millions (1 000 000)": 1000000.0}
    selected_unit_label = st.sidebar.selectbox("Divide Values By:", options=list(unit_options.keys()), index=0)
    unit_divider = unit_options[selected_unit_label]

    st.sidebar.markdown("---")

    # =============================================================================
    # EXECUTIVE WORKSPACE: UNIFIED PROCESS & SUPPLY CHAIN INTELLIGENCE DASHBOARD
    # =============================================================================

    # Initialize unified chronological tab architecture for sequential business audit
    tab_parcats, tab_funnel_route, tab_vol_static, tab_bento, tab_matrix, tab_outliers = st.tabs([
        "1. Flows",
        "2. Funnel",
        "3. Structural Breakdown",
        "4. Bento",
        "5. Heatmap",
        "6. Anomaly & Risk Audit"
    ])

    # =============================================================================
    # TAB 1: MULTIDIMENSIONAL PATHS (PARALLEL CATEGORIES ARCHITECTURE)
    # =============================================================================
    with tab_parcats:
        st.subheader("Multi-Layer Pipeline Analysis")
        st.write(
            "**Best for:** Hybrid routing. Define your sequential starting stages in the multiselect, "
            "and choose your final destination column to append it automatically."
        )

        # Control Panel Section 2: Visual Layout Typography & Header Options
        title_col1, title_col2, title_col3 = st.columns(3)
        with title_col1:
            chart_title = st.text_input(
                "Header:",
                value=st.session_state["global_chart_title"],
                key="local_title_text_parcats",
                on_change=sync_global_session_variable,
                args=("local_title_text_parcats", "global_chart_title")
            )
        with title_col2:
            align_options = ["Left", "Center", "Right"]
            current_align = st.session_state["global_title_align"]
            default_align_idx = align_options.index(current_align) if current_align in align_options else 0

            parcats_title_align = st.selectbox(
                "Header Alignment:",
                options=align_options,
                index=default_align_idx,
                key="local_title_align_parcats",
                on_change=sync_global_session_variable,
                args=("local_title_align_parcats", "global_title_align")
            )
        with title_col3:
            title_size = st.slider(
                "Title Font Size:",
                min_value=12,
                max_value=32,
                value=int(st.session_state["global_title_size"]),
                step=1,
                key="local_title_size_parcats",
                on_change=sync_global_session_variable,
                args=("local_title_size_parcats", "global_title_size")
            )

        # Control Panel Section 1: Axis Mapping and Pipeline Traversal Configuration
        p_ctrl1, p_ctrl2, p_ctrl3 = st.columns(3)
        with p_ctrl1:
            selected_stages_parcats = st.multiselect(
                "Source/Intermediate Points:",
                options=all_columns,
                default=[all_columns[0]] if len(all_columns) > 0 else all_columns,
                key="p_stages_multi"
            )
        with p_ctrl2:
            remaining_for_target = [c for c in all_columns if c not in selected_stages_parcats]
            if not remaining_for_target:
                remaining_for_target = all_columns
            final_target_parcats = st.selectbox(
                "Target:",
                options=remaining_for_target,
                index=0,
                key="p_target_final"
            )
        with p_ctrl3:
            parcats_metric_options = ["Number of rows (Sample size)"] + list(opt_table.select_dtypes(include=[np.number]).columns)
            current_global_val = st.session_state["global_measure_col"]
            default_idx_par = parcats_metric_options.index(current_global_val) if current_global_val in parcats_metric_options else 0

            value_col_parcats = st.selectbox(
                "Weight/Volume:",
                options=parcats_metric_options,
                index=default_idx_par,
                key="local_val_parcats",
                on_change=sync_global_session_variable,
                args=("local_val_parcats", "global_measure_col")
            )

        # Geometry transformations for header placement and random seeds allocation
        align_mapping_s = {"Left": 0.0, "Center": 0.5, "Right": 1.0}
        title_x_pos_s = align_mapping_s.get(parcats_title_align, 0.0)

        base_seed = st.session_state.get("current_seed", 42)
        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        use_shuffle = base_seed + (palette_indices.get(selected_palette, 0) * 100)

        # GLOBAL INTERCEPTOR: Validate the column combination selected by the user
        # If the check_is_aggregated_data function returns True, it will handle displaying st.error natively,
        # meaning the block inside 'else' (rendering the chart) simply will not execute!
        if check_is_aggregated_data(opt_table, selected_stages_parcats, final_target_parcats):
            pass
        else:
            fig_parcats = generate_parcats(
                df=opt_table,
                stage_nodes=selected_stages_parcats,
                target_node=final_target_parcats,
                value_col=value_col_parcats,
                selected_palette=chosen_colors,
                unit_divider=unit_divider,
                force_shuffle=use_shuffle,
                chart_title=chart_title,
                title_size=title_size,
                title_x=title_x_pos_s,
                width_px=chart_width_px,
                height_px=chart_height_px
            )

            render_with_scroll(
                fig=fig_parcats,
                width=chart_width_px,
                height=chart_height_px
            )

    # =============================================================================
    # TAB 2: PIPELINE ROUTE CONVERSION (ROUTE-SPECIFIC FUNNEL ANALYSIS)
    # =============================================================================
    with tab_funnel_route:
        st.subheader("Single Route Analysis")
        st.write(
            "**Best for:** Specific route diagnostics. Select multiple sequential starting points and "
            "a final destination to isolate and trace volume contraction step-by-step."
        )

        # Control Panel Section 1: Visual Layout Typography & Header Options
        fun_title_col1, fun_title_col2, fun_title_col3 = st.columns(3)
        with fun_title_col1:
            fun_chart_title = st.text_input(
                "Header:",
                value=st.session_state["global_chart_title"],
                key="local_title_text_funnel",
                on_change=sync_global_session_variable,
                args=("local_title_text_funnel", "global_chart_title")
                # value="Specific Pipeline Route Conversion",
                # key="fun_title_input"
            )
        with fun_title_col2:
            align_options=["Left", "Center", "Right"]
            current_align = st.session_state["global_title_align"]
            default_align_idx = align_options.index(current_align) if current_align in align_options else 0
            fun_title_align = st.selectbox(
                "Header Alignment:",
                options=align_options,
                index=default_align_idx,
                key="local_title_align_funnel",
                on_change=sync_global_session_variable,
                args=("local_title_align_funnel", "global_title_align")
            )
        with fun_title_col3:
            fun_title_size = st.slider(
                "Title Font Size:",
                min_value=12,
                max_value=36,
                value=20,
                step=1,
                key="local_title_size_funnel",
                on_change=sync_global_session_variable,
                args=("local_title_size_funnel", "global_title_size")
            )

        # Control Panel Section 2: Component Axis Mapping Configuration (MULTISELECT ENHANCED)
        fun_ctrl_col1, fun_ctrl_col2, fun_ctrl_col3 = st.columns(3)
        with fun_ctrl_col1:
            selected_stages_fun = st.multiselect(
                "Source/Intermediate Points:",
                options=all_columns,
                default=[all_columns[0]] if len(all_columns) > 0 else all_columns,
                key="fun_stages_multi"
            )
        with fun_ctrl_col2:
            remaining_for_fun_target = [c for c in all_columns if c not in selected_stages_fun]
            if not remaining_for_fun_target:
                remaining_for_fun_target = all_columns
            final_target_fun = st.selectbox(
                "Target:",
                options=remaining_for_fun_target,
                index=0,
                key="fun_target_final"
            )
        with fun_ctrl_col3:
            funnel_metric_options = ["Number of rows (Sample size)"] + list(opt_table.select_dtypes(include=[np.number]).columns)
            current_global_val = st.session_state["global_measure_col"]
            default_idx_fun = funnel_metric_options.index(current_global_val) if current_global_val in funnel_metric_options else 0
            value_col_fun = st.selectbox(
                "Weight/Volume:",
                options=funnel_metric_options,
                index=default_idx_fun,
                key="local_val_funnel",
                on_change=sync_global_session_variable,
                args=("local_val_parcats", "global_measure_col")
            )

        st.markdown("Select Specific Route Path for Funnel Profiling:")

        # =============================================================================
        # MODERNIZATION: DYNAMIC CASCADE ROUTE ENGINE FOR ANY DEPTH
        # =============================================================================
        # Combine all user-selected stage columns and the final target into a unified steps list
        pipeline_steps = list(selected_stages_fun)
        if final_target_fun not in pipeline_steps:
            pipeline_steps.append(final_target_fun)

        # Build an adaptive horizontal columns grid based on the total number of steps
        cols_layout = st.columns(len(pipeline_steps))
        selected_route_dict = {}

        # Initialize the data context tracker, which narrows down progressively per step
        df_routing_context = opt_table.copy()

        for idx, stage_col in enumerate(pipeline_steps):
            with cols_layout[idx]:
                # Options are derived strictly from surviving transactions of preceding levels
                available_options = sorted(list(df_routing_context[stage_col].dropna().astype(str).unique()))

                # Safeguard against empty lists if a previous selection hits a dead end
                if not available_options:
                    available_options = ["N/A"]

                chosen_val = st.selectbox(
                    f"Step {idx+1}: {stage_col.upper()}",
                    options=available_options,
                    key=f"funnel_cascade_step_selector_{stage_col}_{idx}"
                )

                # Save the current selection into the routing directory passed to the chart renderer
                selected_route_dict[stage_col] = chosen_val

                # Cascade-filter the tracking dataset context for the next downstream node level
                df_routing_context = df_routing_context[df_routing_context[stage_col].astype(str) == chosen_val]

        st.markdown("---")

        # Geometry transformations for header placement and coordinate mapping
        align_mapping_f = {"Left": 0.0, "Center": 0.5, "Right": 1.0}
        title_x_pos_f = align_mapping_f.get(fun_title_align, 0.0)

        # Fetch stable randomization seed explicitly to safeguard pipeline operations
        base_seed = st.session_state.get("current_seed", 42)
        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        use_shuffle = base_seed + (palette_indices.get(selected_palette, 0) * 100)

        # Generate a stable randomization seed for the visualization palette
        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        base_seed = st.session_state.get("current_seed", 42)
        use_shuffle_fun = base_seed + (palette_indices.get(selected_palette, 0) * 100) + 100

        if check_is_aggregated_data(opt_table, selected_stages_fun, final_target_fun):
            pass
        else:
            # Initialize the automated route-specific pipeline conversion engine
            fig_fun = generate_funnel_chart(
                df=opt_table,
                stage_nodes=selected_stages_fun,
                target_node=final_target_fun,
                value_col=value_col_fun,
                selected_route_dict=selected_route_dict,
                selected_palette=chosen_colors,
                unit_divider=unit_divider,
                force_shuffle=use_shuffle_fun,
                chart_title=fun_chart_title,
                title_size=fun_title_size,
                title_x=title_x_pos_f,
                width_px=chart_width_px,
                height_px=chart_height_px
            )

            render_with_scroll(
                fig=fig_fun,
                width=chart_width_px,
                height=chart_height_px
            )

    # =============================================================================
    # TAB 3: VOLUMETRIC ANALYSIS: STRUCTURAL BREAKDOWN (STACKED BAR ARCHITECTURE)
    # =============================================================================
    with tab_vol_static:
        st.subheader("Structural Breakdown Chart")
        st.write("**Best for:** Comparing structural compositions and breakdown shares between selected dimensions.")

        # Control Panel Section 1: Visual Layout Typography & Header Options
        bar_title_col1, bar_title_col2, bar_title_col3 = st.columns(3)

        with bar_title_col1:
            bar_chart_title = st.text_input(
                "Header:",
                value=st.session_state["global_chart_title"],
                key="local_title_text_bar",
                on_change=sync_global_session_variable,
                args=("local_title_text_bar", "global_chart_title")
            )

        with bar_title_col2:
            align_options = ["Left", "Center", "Right"]
            current_align = st.session_state["global_title_align"]
            default_align_idx = align_options.index(current_align) if current_align in align_options else 0

            bar_title_align = st.selectbox(
                "Header Alignment:",
                options=align_options,
                index=default_align_idx,
                key="local_title_align_bar",
                on_change=sync_global_session_variable,
                args=("local_title_align_bar", "global_title_align")
            )

        with bar_title_col3:
            bar_title_size = st.slider(
                "Title Font Size:",
                min_value=12,
                max_value=32,
                value=int(st.session_state["global_title_size"]),
                step=1,
                key="local_title_size_bar",
                on_change=sync_global_session_variable,
                args=("local_title_size_bar", "global_title_size")
            )

        # Control Panel Section 2: Axis Mapping and Pipeline Traversal Configuration
        bar_ctrl_col1, bar_ctrl_col2, bar_ctrl_col3 = st.columns(3)
        with bar_ctrl_col1:
            selected_stages_bar = st.multiselect(
                "Source/Intermediate Points:",
                options=all_columns,
                default=[all_columns[0]] if len(all_columns) > 0 else all_columns,
                key="bar_stages_multi"
            )
        with bar_ctrl_col2:
            current_global_col = st.session_state.get("global_color_col")
            # 2. Generate the list of available columns
            remaining_for_bar_target = [c for c in all_columns if c not in selected_stages_bar]
            if not remaining_for_bar_target:
                remaining_for_bar_target = all_columns

            # 3. Calculate the current index for the selectbox
            # If the saved value exists in the new list, use its index; otherwise, default to 0
            if current_global_col in remaining_for_bar_target:
                default_index = remaining_for_bar_target.index(current_global_col)
            else:
                default_index = 0

            # 4. Render the widget with the dynamic index
            final_target_bar = st.selectbox(
                "Color by:",
                options=remaining_for_bar_target,
                index=default_index,
                key="local_color_col",
                on_change=sync_global_session_variable,
                args=("local_color_col", "global_color_col")
            )

        with bar_ctrl_col3:
            bar_metric_options = ["Number of rows (Sample size)"] + list(opt_table.select_dtypes(include=[np.number]).columns)
            current_global_val = st.session_state["global_measure_col"]
            default_idx_bar = funnel_metric_options.index(current_global_val) if current_global_val in bar_metric_options else 0

            value_col_bar = st.selectbox(
                "Weight/Volume:",
                options=bar_metric_options,
                index=default_idx_bar,
                key="local_val_bar",
                on_change=sync_global_session_variable,
                args=("local_val_bar", "global_measure_col")
            )

        st.markdown("---")

        # Geometry transformations for header placement and coordinate mapping
        align_mapping_bar = {"Left": 0.0, "Center": 0.5, "Right": 1.0}
        title_x_pos_bar = align_mapping_bar.get(bar_title_align, 0.0)

        # Generate a stable randomization seed for the visualization palette
        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        base_seed = st.session_state.get("current_seed", 42)
        use_shuffle_bar = base_seed + (palette_indices.get(selected_palette, 0) * 100) + 200

        if check_is_aggregated_data(opt_table, selected_stages_bar, final_target_bar):
            pass
        else:

            # Initialize the automated volumetric aggregation engine
            fig_bar = generate_stacked_bar_chart(
                df=opt_table,
                stage_nodes=selected_stages_bar,
                target_node=final_target_bar,
                value_col=value_col_bar,
                selected_palette=chosen_colors,
                unit_divider=unit_divider,
                force_shuffle=use_shuffle_bar,
                chart_title=bar_chart_title,
                title_size=bar_title_size,
                title_x=title_x_pos_bar,
                width_px=chart_width_px,
                height_px=chart_height_px
            )

            render_with_scroll(
                fig=fig_bar,
                width=chart_width_px,
                height=chart_height_px
            )

    # =============================================================================
    # TAB 4: COMPONENT SHARE MAP (BENTO TREEMAP ARCHITECTURE)
    # =============================================================================
    with tab_bento:
        st.subheader("Bento Chart")
        st.write(
            "**Best for:** At-a-glance dashboard summaries to spot top-performing "
            "categories and volume distribution instantly within a tiled bento layout."
        )

        # Control Panel Section 1: Visual Layout Typography & Header Options
        bento_title_col1, bento_title_col2, bento_title_col3 = st.columns(3)
        with bento_title_col1:
            bento_chart_title = st.text_input(
                "Header:",
                value=st.session_state["global_chart_title"],
                key="local_title_text_bento",
                on_change=sync_global_session_variable,
                args=("local_title_text_bento", "global_chart_title")
            )
        with bento_title_col2:
            align_options = ["Left", "Center", "Right"]
            current_align = st.session_state["global_title_align"]
            default_align_idx = align_options.index(current_align) if current_align in align_options else 0

            bento_title_align = st.selectbox(
                "Header Alignment:",
                options=align_options,
                index=default_align_idx,
                key="local_title_align_bento",
                on_change=sync_global_session_variable,
                args=("local_title_align_bento", "global_title_align")
            )
        with bento_title_col3:
            bento_title_size = st.slider(
                "Title Font Size:",
                min_value=12,
                max_value=36,
                value=int(st.session_state["global_title_size"]),
                step=1,
                key="local_title_size_bento",
                on_change=sync_global_session_variable,
                args=("local_title_size_bento", "global_title_size")
            )

        # Control Panel Section 2: Axis Mapping and Dimension Grouping Configuration
        bento_ctrl_col1, bento_ctrl_col2 = st.columns(2)
        with bento_ctrl_col2:
            bento_metric_options = ["Number of rows (Sample size)"] + list(opt_table.select_dtypes(include=[np.number]).columns)
            current_global_val = st.session_state["global_measure_col"]
            default_idx_bento = bento_metric_options.index(current_global_val) if current_global_val in bento_metric_options else 0
            value_col_bento = st.selectbox(
                "Weight/Volume",
                options=bento_metric_options,
                index=default_idx_bento,
                key="local_val_bento",
                on_change=sync_global_session_variable,
                args=("local_val_bento", "global_measure_col")
            )

        with bento_ctrl_col1:
            id_options = [c for c in all_columns if c != value_col_bento]
            bento_id_col = st.selectbox(
                "Categorical Feature:",
                options=id_options,
                key="bento_id_raw"
            )

        st.markdown("---")

        # Geometry transformations for header placement and text mapping
        align_mapping = {"Left": 0.0, "Center": 0.5, "Right": 1.0}
        title_x_pos = align_mapping.get(bento_title_align, 0.0)

        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        base_seed = st.session_state.get("current_seed", 42)
        use_shuffle_bento = base_seed + (palette_indices.get(selected_palette, 0) * 100) + 300


        # Initialize the automated volumetric tile allocation engine
        fig_bento = generate_bento_treemap(
            df=opt_table,
            id_col=bento_id_col,
            value_col=value_col_bento,
            selected_palette=chosen_colors,
            unit_divider=unit_divider,
            force_shuffle=use_shuffle_bento,
            chart_title=bento_chart_title,
            title_size=bento_title_size,
            title_x=title_x_pos,
            width_px=chart_width_px,
            height_px=chart_height_px
        )

        render_with_scroll(
            fig=fig_bento,
            width=chart_width_px,
            height=chart_height_px
        )

    # =============================================================================
    # TAB 5: HEATMAP DENSITY ARCHITECTURE
    # =============================================================================
    with tab_matrix:
        st.subheader("Heatmap")
        st.write(
            "**Best for:** Density analysis to instantly spot where two dimensions cross "
            "with the highest volume or transaction activity over temporal cycles."
        )

        # Control Panel Section 1: Visual Layout Typography & Header Options
        h_title_col1, h_title_col2, h_title_col3 = st.columns(3)
        with h_title_col1:
            heatmap_chart_title = st.text_input(
                "Header:",
                value=st.session_state["global_chart_title"],
                key="local_title_text_heatmap",
                on_change=sync_global_session_variable,
                args=("local_title_text_heatmap", "global_chart_title")
            )
        with h_title_col2:
            align_options = ["Left", "Center", "Right"]
            current_align = st.session_state["global_title_align"]
            default_align_idx = align_options.index(current_align) if current_align in align_options else 0

            heatmap_title_align = st.selectbox(
                "Header Alignment:",
                options=align_options,
                index=default_align_idx,
                key="local_title_align_heatmap",
                on_change=sync_global_session_variable,
                args=("local_title_align_heatmap", "global_title_align")
            )
        with h_title_col3:
            heatmap_title_size = st.slider(
                "Title Font Size:",
                min_value=12,
                max_value=36,
                value=int(st.session_state["global_title_size"]),
                step=1,
                key="local_title_size_heatmap",
                on_change=sync_global_session_variable,
                args=("local_title_size_heatmap", "global_title_size")
            )

        # Control Panel Section 2: Axis Mapping and Heatmap Configuration
        h_ctrl1, h_ctrl2, h_ctrl3, mat_ctrl_col4 = st.columns(4)
        with h_ctrl1:
            x_axis_heatmap = st.selectbox(
                "X-Axis Columns (Categories):",
                options=all_columns,
                index=2 if len(all_columns) > 2 else 0,
                key="h_x"
            )
        with h_ctrl2:
            remaining_cols_h = [c for c in all_columns if c != x_axis_heatmap]
            y_axis_heatmap = st.selectbox(
                "Y-Axis Rows (Categories):",
                options=remaining_cols_h,
                index=0,
                key="h_y"
            )
        with h_ctrl3:
            heat_metric_options = ["Number of rows (Sample size)"] + list(opt_table.select_dtypes(include=[np.number]).columns)
            current_global_val = st.session_state["global_measure_col"]
            default_idx_heat = heat_metric_options.index(current_global_val) if current_global_val in heat_metric_options else 0
            value_col_heatmap = st.selectbox(
                "Volume Measure (Z-Axis Value):",
                options=bento_metric_options,
                index=default_idx_heat,
                key="local_val_heat",
                on_change=sync_global_session_variable,
                args=("local_val_heat", "global_measure_col")
            )

        with mat_ctrl_col4:
            st.markdown("""
                <style>
                    div[data-testid="stCheckbox"] {
                        margin-top: 10px !important; 
                    }
                </style>
            """, unsafe_allow_html=True)

            # FIXED: Provide a non-empty label but hide it natively using label_visibility
            show_annotations = st.checkbox(
                label="Show Cell Values",
                value=False,
                key="matrix_show_annot_switch",
                label_visibility="visible"
            )

        st.markdown("---")

        # Geometry transformations for header placement and text mapping
        align_mapping = {"Left": 0.0, "Center": 0.5, "Right": 1.0}
        title_x_pos_h = align_mapping.get(heatmap_title_align, 0.0)

        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        base_seed = st.session_state.get("current_seed", 42)
        use_shuffle_heat = base_seed + (palette_indices.get(selected_palette, 0) * 100) + 400

        # Initialize the automated heatmap aggregation engine
        fig_heatmap = generate_heatmap(
            df=opt_table,
            x_col=x_axis_heatmap,
            y_col=y_axis_heatmap,
            value_col=value_col_heatmap,
            selected_palette=chosen_colors,
            unit_divider=unit_divider,
            force_shuffle=use_shuffle_heat,
            chart_title=heatmap_chart_title,
            title_size=heatmap_title_size,
            title_x=title_x_pos_h,
            width_px=chart_width_px,
            height_px=chart_height_px,
            show_annot=show_annotations
        )

        render_with_scroll(
            fig=fig_heatmap,
            width=chart_width_px,
            height=chart_height_px
        )

    # =============================================================================
    # TAB 6: ANOMALY & RISK AUDIT (ROUTE TRANSACTIONS & LOG OUTLIER ANALYSIS)
    # =============================================================================
    with tab_outliers:
        st.subheader("Process Route Outlier & Anomaly Analysis")
        st.write(
            "**Best for:** Specific route auditing. Define an end-to-end corridor to automatically compute "
            "statistical thresholds (IQR method) and isolate abnormal execution spikes, infinite loops, or transaction bursts."
        )

        # Control Panel Section 1: Visual Layout Typography & Header Options
        out_title_col1, out_title_col2, out_title_col3 = st.columns(3)
        with out_title_col1:
            outliers_chart_title = st.text_input(
                "Header:",
                value=st.session_state["global_chart_title"],
                key="local_title_text_outlier",
                on_change=sync_global_session_variable,
                args=("local_title_text_outlier", "global_chart_title")
            )

        with out_title_col2:
            align_options = ["Left", "Center", "Right"]
            current_align = st.session_state["global_title_align"]
            default_align_idx = align_options.index(current_align) if current_align in align_options else 0

            outliers_title_align = st.selectbox(
                "Header Alignment:",
                options=align_options,
                index=default_align_idx,
                key="outliers_title_align",
                on_change=sync_global_session_variable,
                args=("outliers_title_align", "global_title_align")
            )
        with out_title_col3:
            outliers_title_size = st.slider(
                "Title Font Size:",
                min_value=12,
                max_value=36,
                value=int(st.session_state["global_title_size"]),
                step=1,
                key="local_title_size_outlier",
                on_change=sync_global_session_variable,
                args=("local_title_size_outlier", "global_title_size")
            )


        # Control Panel Section 2: Core Axis Mapping & Aggregation Configuration
        out_ctrl_col1, out_ctrl_col2, out_ctrl_col3, out_ctrl_col4 = st.columns(4) # Split into 4 columns to fit aggregation selector
        with out_ctrl_col1:
            stage_col_out = st.selectbox(
                "Source (From):",
                options=all_columns,
                key="out_stage_axis"
            )

        with out_ctrl_col2:
            # Consolidate text columns for the destination axis layout dynamically
            remaining_for_out_target = [c for c in all_columns if c != stage_col_out]
            if not remaining_for_out_target:
                remaining_for_out_target = all_columns

            target_col_out = st.selectbox(
                "Target (To):",
                options=remaining_for_out_target,
                key="out_target_axis"
            )

        with out_ctrl_col3:
            # TIGHT SYNCHRONIZATION FILTER: Bind the weight selector to global session state memory
            current_global_val = st.session_state["global_measure_col"]
            default_idx_out = numeric_cols.index(current_global_val) if current_global_val in numeric_cols else 0

            value_col_out = st.selectbox(
                "Weight/Volume/Metric:",
                options=numeric_cols,
                index=default_idx_out,          # Preserves the user choice globally across tabs
                key="local_val_outliers",       # Unique state tracking key for this selector element
                on_change=sync_global_session_variable,
                args=("local_val_outliers", "global_measure_col")    # FIXED: Bound to global_measure_col instead of alignment
            )

        with out_ctrl_col4:
            # NEW: Aggregation method dropdown for flexible analytical view scoping
            agg_options_out = {"Total Accumulated (Sum)": "sum", "Max Single-Run (Max)": "max", "Average (Mean)": "mean", "Min Single-Rin (Min)" : "min", "Total Number (Count)" : "count"}
            selected_agg_label_out = st.selectbox(
                "Aggregation Method:",
                options=list(agg_options_out.keys()),
                index=0,
                key="out_aggregation_func"
            )
            agg_func_out = agg_options_out[selected_agg_label_out]

        st.markdown("Select Specific Route Path for Statistical Audit:")
        filter_col1, filter_col2 = st.columns(2)

        # Geometry transformations for header placement and coordinate mapping
        align_mapping_out = {"Left": 0.0, "Center": 0.5, "Right": 1.0}
        title_x_pos_out = align_mapping_out.get(outliers_title_align, 0.0)

        palette_indices = {name: i for i, name in enumerate(COLOR_PALETTES.keys())}
        base_seed = st.session_state.get("current_seed", 42)
        # Seed offset unified standard for the 7th tab view (+ 700)
        use_shuffle_out = base_seed + (palette_indices.get(selected_palette, 0) * 100) + 700


        # Initialize the automated statistical risk profiling engine targeting a specific route
        fig_outliers = generate_outliers_chart(
            df=opt_table,
            stage_col=stage_col_out,
            target_col=target_col_out,
            value_col=value_col_out,
            agg_func=agg_func_out, # UPDATED: Dynamic aggregation method parameter pass
            selected_palette=chosen_colors,
            unit_divider=unit_divider,
            force_shuffle=use_shuffle_out,
            chart_title=outliers_chart_title,
            title_size=outliers_title_size,
            title_x=title_x_pos_out,
            width_px=chart_width_px,
            height_px=chart_height_px
        )

        render_with_scroll(
            fig=fig_outliers,
            width=chart_width_px,
            height=chart_height_px
        )
