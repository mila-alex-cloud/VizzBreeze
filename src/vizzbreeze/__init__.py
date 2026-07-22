# EXPOSE CHANNELS FOR JUPYTER NOTEBOOK EMBEDDING
from vizzbreeze.app import generate_parcats
from vizzbreeze.app import generate_heatmap
from vizzbreeze.app import generate_funnel_chart
from vizzbreeze.app import generate_stacked_bar_chart
from vizzbreeze.app import generate_bento_treemap
from vizzbreeze.app import generate_outliers_chart

# DIRECT DESIGN SYSTEM EXPORT FOR JUPYTER RUNTIME
from vizzbreeze.app import COLOR_PALETTES

__all__ = [
    "generate_parcats",
    "generate_heatmap",
    "generate_funnel_chart",
    "generate_stacked_bar_chart",
    "generate_bento_treemap",
    "generate_outliers_chart",
    "COLOR_PALETTES"
]
