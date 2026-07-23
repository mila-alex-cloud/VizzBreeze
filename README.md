# VizzBreeze

A lightweight, high-performance transactional web-dashboard designed for advanced data flow analytics, multi-stage routing visualization, and statistical risk audit. Built natively on top of Streamlit, Pandas, and Plotly.

## Key Features

- **Flat Transaction Processing Engine**: Optimized for fast processing of un-aggregated logs (e.g., Client ➔ Fund ➔ Asset).
- **Global Session Synchronization**: Seamlessly locks metric column selections, typography sizes, and alignments across all workspace views.
- **Auto-Scroll Suppression**: Enhanced layout architecture prevents viewport jumps during widget updates and data updates.
- **Advanced Graph Matrix Analytics**: Includes high-fidelity stacked charts, multi-dimensional Parcats layouts, Density Matrices, and automated IQR risk audit profiling tools.

## Build With
1  - [Plotly](https://plotly.com) - Core interactive charting engine.
2  - [Streamlit](https://streamlit.io) - Cloud infrastructure and web UI framework.
3  - [Pandas](https://pydata.org) - High-performance data structures and data analysis engine.

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

## Core Analytical Tabs

1. **Flows**: Explore multi-stage multi-dimensional category paths with thin, light axis labels and custom high-contrast hover tooltips.
2. **Funnel**: Track progressive conversion drops along specific workflow layers.
3. **Structural Breakdown**: Classic stacked column bar charts configured with responsive axis titles that update on the fly based on active filters.
4. **Bento**: An asymmetrical modular tile framework designed to compress complex multi-level dimensions into a clean, prioritized grid dashboard.
5. **Density Matrix**: High-density dashboard to scan cluster intersections instantly.
5. **Anomaly & Risk Audit**: Automated statistical anomaly profiling that detects process outliers without freezing the browser engine.

### Core Functions API Reference & Parameter Mapping

All visualization engines are fully modular, accept un-aggregated raw `pandas.DataFrame` inputs, and return native `plotly.graph_objects.Figure` interactive objects.

---

### 1. Flows
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
    height_px=500,                  # int: Holster canvas height
    title_x=0.5                     # float: Header Alighnment
)
fig.update_layout(
    margin=dict(l=100, r=100, t=100, b=50)
    )
fig.show()
```

<img width="837" height="416" alt="image" src="https://github.com/user-attachments/assets/fa4bc19d-4629-4d7e-a733-afc4dfd30ac8" />

### 2. Funnel
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
    height_px=500,
    title_x=0.5                     
)
fig.update_layout(
    margin=dict(l=250, r=20, t=100, b=50)
    )
fig.show()
```

<img width="934" height="437" alt="image" src="https://github.com/user-attachments/assets/517a4d97-6eeb-44cd-8d95-b583cc22bdd6" />

### 3. Structural Breakdown
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
    height_px=500,
    title_x=0.5 
)
fig.update_layout(
    margin=dict(l=100, r=20, t=50, b=50) 
)
fig.update_layout(
    yaxis=dict(
        title="", 
    )
fig.show()
```

<img width="923" height="427" alt="image" src="https://github.com/user-attachments/assets/a9ea4ef1-ba04-453f-b105-2693a228f240" />

### 4. Bento
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
    height_px=500,
    title_x=0.5 
)
fig.update_layout(
    margin=dict(l=50, r=20, t=50, b=50)
    )
fig.show()
```

<img width="909" height="405" alt="image" src="https://github.com/user-attachments/assets/1fc64f9e-ef9b-473d-914a-6d295254cf4e" />

### 5. Density Matrix
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
    height_px=500,
    title_x=0.5 
)
fig.update_layout(
    margin=dict(l=100, r=20, t=50, b=50)
    )
fig.show()
```

<img width="939" height="436" alt="image" src="https://github.com/user-attachments/assets/395a247b-788b-4d81-a9dd-5d9b93546b1c" />

### 6. Anomaly & Risk Audit
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
    height_px=500,
    title_x=0.5 
)
fig.update_layout(
    margin=dict(l=170, r=20, t=50, b=70)
    )
fig.update_layout(
    yaxis=dict(
        title="", 
    )
)
fig.show()
```

<img width="934" height="442" alt="image" src="https://github.com/user-attachments/assets/50398b02-b697-44d8-a55a-5c0c2215f0b3" />


## Requirements

- Python >= 3.9
- Streamlit >= 1.35.0
- Pandas >= 2.1.0
- Plotly >= 5.18.0

## Roadmap

- Advanced Data Preprocessing Pipeline: Implementing automated anomaly tracking and missing value imputation optimized for multi-source financial and operational data arrays.
- Interactive Risk Metrics: Adding features for deep data analysis, including volatility tracking, anomaly detection, and custom structural breakdown widgets.
- Large-Scale Data Engineering: Adding chunks-based data loading and optimization widgets to seamlessly process unaggregated corporate and industrial datasets exceeding 500MB.
- Enterprise Stability & Testing: Expanding code verification with an extensive pytest suite to achieve 85%+ test coverage for secure local CLI execution.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
