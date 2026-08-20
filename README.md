[![PyPI Downloads](https://static.pepy.tech/personalized-badge/vizzbreeze?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/vizzbreeze)

# VizzBreeze

A lightweight, high-performance transactional web-dashboard designed for advanced data flow analytics, multi-stage routing visualization, and statistical risk audit，and AI Agent trace visualization. Built natively on top of Streamlit, Pandas, and Plotly.

## Key Features

- **Flat Transaction Processing Engine**: Optimized for fast processing of un-aggregated logs (e.g., Client ➔ Fund ➔ Asset).
- **Global Session Synchronization**: Seamlessly locks metric column selections, typography sizes, and alignments across all workspace views.
- **Auto-Scroll Suppression**: Enhanced layout architecture prevents viewport jumps during widget updates and data updates.
- **Advanced Graph Matrix Analytics**: Includes high-fidelity stacked charts, multi-dimensional Parcats layouts, Density Matrices, and automated IQR risk audit profiling tools.
- **AI Agent Trace & Observability**: Native templates designed to map LLM chain-of-thought routing, monitor token consumption footprints, and catch execution latency anomalies.


## Build With
1  - [Plotly](https://plotly.com) - Core interactive charting engine.
2  - [Streamlit](https://streamlit.io) - Cloud infrastructure and web UI framework.
3  - [Pandas](https://pydata.org) - High-performance data structures and data analysis engine.

## Quick Start

#### 1. Standard Python / Jupyter Notebook Usage
VizzBreeze functions process un-aggregated raw DataFrames and return native Plotly figures, making them fully compatible with Jupyter views and pipeline automation:

```python
import vizzbreeze as vb
import pandas as pd

# Load raw transaction logs
df = pd.read_csv("transactions.csv")

# Generate advanced Parcats flow directly in your notebook
fig = vb.generate_parcats(
    df=df, 
    stage_nodes=['client', 'fund'], 
    target_node='asset', 
    value_col='amount'
)
fig.show()
```

#### 2. Standalone Web Control Room Execution
If you prefer a full-scale interactive UI with global layout sync, just open your local terminal and run:

```bash
vizzbreeze-run
```

#### Cloud Execution
If you explicitly need to run VizzBreeze in cloud environments like Google Colab, please use a secure SSH/Port-forwarding tunnel to bypass iframe infrastructure limits.

## Test Dataset
To explore the dashboard features instantly, you can use the pre-configured spreadsheet **`sample_data_unaggregated.xlsx`** located in the root folder of this repository. Just drag and drop it into the sidebar upload zone!

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

1. **Flows**: Explore multi-stage category paths (e.g., LLM chain-of-thought: Intent ➔ Agent ➔ Tool) with thin, light axis labels and custom high-contrast hover tooltips.
2. **Funnel**: Track progressive conversion drops along specific workflow layers.
3. **Structural Breakdown**: Classic stacked column bar charts configured with responsive axis titles that update on the fly based on active filters.
4. **Bento**: An asymmetrical modular tile framework designed to compress complex multi-level dimensions (like Token Consumption Footprints) into a clean, prioritized grid dashboard.
5. **Density Matrix**: High-density dashboard to scan cluster intersections instantly.
5. **Anomaly & Risk Audit**: Automated statistical anomaly profiling that detects execution latency spikes and infinite loop outliers without freezing the browser engine.

### Core Functions API Reference & Parameter Mapping

All visualization engines are fully modular, accept un-aggregated raw `pandas.DataFrame` inputs, and return native `plotly.graph_objects.Figure` interactive objects.

---

### 1. Flows
```python
flow_fig = vb.generate_parcats(
    df=df,
    stage_nodes=['user_intent', 'active_agent', 'tool_called'],
    target_node='execution_status',
    value_col='tokens_used',  # Flows will scale by token consumption!
    chart_title="AI Agent Chain of Thought & Token Distribution",
    selected_palette=chosen_colors,
    title_size=20,
    width_px=1600,
    height_px=500,
    title_x = 0.5
)

flow_fig.show()
```
<img width="867" height="266" alt="image" src="https://github.com/user-attachments/assets/71925812-abc1-4d78-a68f-9e497a6dcf3f" />

### 2. Funnel
```python
fig = vb.generate_funnel_chart(
    df=df,
    stage_nodes=['user_intent', 'active_agent', 'tool_called'],   
    target_node='execution_status',                               
    value_col='tokens_used',                                      
    
    # ИСПРАВЛЕНИЕ: Передаем параметры фильтрации из таблицы логов
    selected_route_dict={
        'user_intent':'Tech Support', 'active_agent':'Router_Agent', 'tool_called':'Knowledge_Base_Lookup'  # Показываем путь только для конкретного ID лога

    },                                       
    selected_palette=chosen_colors,            
    unit_divider=1.0,
    force_shuffle=True,
    chart_title="AI Agent Chain of Thought & Token Distribution", 
    width_px=1050,
    height_px=500,
    title_x=0.5
)

fig.update_layout(
    margin=dict(l=350, r=20, t=100, b=50)
)
```
<img width="575" height="249" alt="image" src="https://github.com/user-attachments/assets/78f14331-6bdd-4ea4-96b7-8953fd52edd7" />

### 3. Structural Breakdown
```python
stage_nodes=['user_intent']
target_node='execution_status'
value_col='tokens_used'

fig = vb.generate_stacked_bar_chart(
    df=df,
    stage_nodes=stage_nodes,
    target_node=target_node,           
    value_col=value_col,            
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=True,
    chart_title="Systemic Error Distribution Across Active Agents",
    width_px=1600,
    height_px=500,
    title_x = 0.5
)
fig.update_layout(
    margin=dict(l=100, r=20, t=50, b=120)
)

fig.update_layout(
    yaxis=dict(
        title=""
    )
)

fig.show()
```
<img width="869" height="278" alt="image" src="https://github.com/user-attachments/assets/3e6dd8d4-8a50-464f-99f5-151eeb7c51dd" />

### 4. Bento
```python
fig = vb.generate_bento_treemap(
    df=df,
    id_col='user_intent',      
    value_col=value_col,           
    selected_palette=chosen_colors,
    unit_divider=1.0,
    force_shuffle=True,
    chart_title="Token Consumption Footprint by Intent Layer",
    width_px=1050,
    height_px=500,
    title_x = 0.5
)
fig.update_layout(
    margin=dict(l=50, r=20, t=50, b=50)
    )
fig.show()
```
<img width="562" height="257" alt="image" src="https://github.com/user-attachments/assets/4a147f48-3e30-47ea-97ab-8956f4f2c13d" />

### 5. Density Matrix
```python
fig = vb.generate_heatmap(
    df=df,
    x_col='user_intent',
    y_col='execution_status',
    value_col='tokens_used',
    selected_palette=chosen_colors,
    chart_title="AI Agent Token Consumption Heatmap by Execution Status", 
    show_annot=True,
    width_px=1050,
    height_px=500,
    title_x=0.5
)

fig.update_xaxes(title_text="USER INTENT LAYER")
fig.update_yaxes(title_text="EXECUTION STATUS")

fig.update_layout(
    margin=dict(l=150, r=20, t=50, b=50)
)
fig.show()
```

<img width="582" height="280" alt="image" src="https://github.com/user-attachments/assets/d46b91f3-b557-4fd1-84f6-13d5528568fe" />

### 6. Anomaly & Risk Audit
```python
anomaly_fig = vb.generate_outliers_chart(
    df=df,
    stage_col='active_agent',
    target_col='tool_called',
    value_col='execution_time_sec',
    chart_title="AI Execution Latency Anomaly Profile (IQR Bounds)",
    selected_palette=chosen_colors,
    width_px=1050,
    height_px=500,
    title_x=0.5
)

anomaly_fig.update_xaxes(title_text="TOTAL ACCUMULATED LATENCY (SEC)")

anomaly_fig.update_layout(
    margin=dict(l=310, r=20, t=50, b=50)
)
anomaly_fig.show()
```

<img width="580" height="280" alt="image" src="https://github.com/user-attachments/assets/f6568901-5fee-4c2b-aa25-d5350b5dab8c" />

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
