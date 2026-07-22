# VizzBreeze

A lightweight, high-performance transactional web-dashboard designed for advanced data flow analytics, multi-stage routing visualization, and statistical risk audit. Built natively on top of Streamlit, Pandas, and Plotly.

<video src="demo.mp4" controls width="60%"></video>

## Key Features

- **Flat Transaction Processing Engine**: Optimized for fast processing of un-aggregated logs (e.g., Client ➔ Fund ➔ Asset).
- **Global Session Synchronization**: Seamlessly locks metric column selections, typography sizes, and alignments across all workspace views.
- **Auto-Scroll Suppression**: Enhanced layout architecture prevents viewport jumps during widget updates and data updates.
- **Advanced Graph Matrix Analytics**: Includes high-fidelity stacked charts, multi-dimensional Parcats layouts, Density Matrices, and automated IQR risk audit profiling tools.

## Quick Start

You can install and launch the interactive analytical control room globally using just two commands in your terminal:

```bash
pip install vizzbreeze
vizzbreeze-run
```

**Test Dataset**: To explore the dashboard features instantly, you can use the pre-configured spreadsheet **`sample_data_unaggregated.xlsx`** located in the root folder of this repository. Just drag and drop it into the sidebar upload zone!

## Jupyter Notebook Integration

VizzBreeze is fully compatible with Jupyter Notebooks. You can import individual chart engines independently to render interactive Plotly visualizations directly within your notebook cells:

## Jupyter Notebook Advanced Integration

VizzBreeze functions return native `plotly.graph_objects.Figure` instances, making them fully compatible with Jupyter Notebook visualization viewports.

### Accessing Built-in Color Palettes
You don't need to hardcode HEX styles. Access the corporate design system directly from the package configuration:
```python
import vizzbreeze as vb

# View all available palette names
print(vb.COLOR_PALETTES.keys())

# Extract a specific synchronized list of colors
chosen_colors = vb.COLOR_PALETTES["Warm Amber"]
```

### Core Functions API Reference & Parameter Mapping

All visualization engines are fully modular, accept un-aggregated raw `pandas.DataFrame` inputs, and return native `plotly.graph_objects.Figure` interactive objects.

---

### 1. Multi-Stage Category Flows
```python
fig = vb.generate_parcats(
    df=df,                          # pandas.DataFrame: Source transaction logs (un-aggregated)
    stage_nodes=['col1', 'col2'],   # list: Ordered column names defining the routing stages
    target_node='col3',             # str: The terminal endpoint column name
    value_col='amount',             # str: Volume metric column name (or "Number of rows (Sample size)")
    selected_palette=chosen_colors, # list/str: List of HEX codes or a built-in palette name string
    unit_divider=1.0,               # float: Optional division scaling factor (e.g., 1000 for Thousands)
    force_shuffle=False,            # bool/int: Seed integer to randomize color distribution maps
    chart_title="Flow Canvas",      # str: Custom graph header text
    title_size=20,                  # int: Font size of the chart title
    width_px=1050,                  # int: Holster canvas width (1050 fits Jupyter viewports perfectly)
    height_px=500                   # int: Holster canvas height
)
```

### 2. Conversion Pipeline
```python
fig = vb.generate_funnel_chart(
    df=df,
    stage_nodes=['col1', 'col2'],   # list: Sequence of progressive funnel workflow steps
    target_node='col3',             # str: Terminal checkpoint layer name
    value_col='amount',             # str: Volume metric target column
    selected_route_dict=route_dict, # dict: Active routing coordinate filters (e.g., {'col1': 'Client_1'})
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=False,
    chart_title="Pipeline Drops",
    width_px=1050,
    height_px=500
)
```

### 3. Composition Stacked Bars
```python
fig = vb.generate_stacked_bar_chart(
    df=df,
    stage_nodes=['col1', 'col2'],   # list: Categories to aggregate and display on the horizontal X-axis
    target_node='col3',             # str: Legend segment categorical target breakdown
    value_col='amount',             # str: Numeric target volume metric
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=False,
    chart_title="Composition",
    width_px=1050,
    height_px=500
)
```

### 4. Bento Treemap Tiles
```python
fig = vb.generate_bento_treemap(
    df=df,
    id_col='target_dimension',      # str: Unique column name to rank and partition into tiles
    value_col='amount',             # str: Target numeric metric column name
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=False,
    chart_title="Bento Allocation Top-15", # Automatically truncates grid layout to Top 15 nodes
    width_px=1050,
    height_px=500
)
```

### 5. Intersection Density Matrix
```python
fig = vb.generate_heatmap(
    df=df,
    x_col='category_x',             # str: Categorical split column for horizontal partitions (X-Axis)
    y_col='category_y',             # str: Categorical split column for vertical partitions (Y-Axis)
    value_col='amount',             # str: Numeric target volume or "Number of rows (Sample size)"
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=False,
    chart_title="Density Matrix",
    show_annot=True,                # bool: Inject clean, non-zero numeric labels inside active cells
    width_px=1050,
    height_px=500
)
```

### 6. Statistical Risk Audit Profiler
```python
fig = vb.generate_outliers_chart(
    df=df,
    stage_col='origin_node',         # str: Operational source checkpoint step
    target_col='destination_node',   # str: Operational destination checkpoint step
    value_col='amount',              # str: Numeric target weight column to compute strict IQR bounds
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=False,
    chart_title="Statistical Anomaly Profile", # Automatically plots a dashed line at Q3 + 1.5*IQR upper boundary
    width_px=1050,
    height_px=500
)
```


## Core Analytical Tabs

1. **Flows**: Explore multi-stage multi-dimensional category paths with thin, light axis labels and custom high-contrast hover tooltips.
2. **Funnel**: Track progressive conversion drops along specific workflow layers.
3. **Structural Breakdown**: Classic stacked column bar charts configured with responsive axis titles that update on the fly based on active filters.
4. **Bento**: An asymmetrical modular tile framework designed to compress complex multi-level dimensions into a clean, prioritized grid dashboard.
5. **Density Matrix**: High-density dashboard to scan cluster intersections instantly.
5. **Anomaly & Risk Audit**: Automated statistical anomaly profiling that detects process outliers without freezing the browser engine.

## Requirements

- Python >= 3.9
- Streamlit >= 1.35.0
- Pandas >= 2.1.0
- Plotly >= 5.18.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.
