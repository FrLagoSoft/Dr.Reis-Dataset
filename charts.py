"""
charts.py
---------
Plotly figure builders. Each function takes a DataFrame plus the user's
choices and returns a figure with a title, labeled axes, and a legend
(or color bar), so the UI code never has to repeat styling.
"""

import plotly.express as px
import plotly.graph_objects as go

from data_utils import PARAMETERS, label

ZONE_COLORS = {"Shallow": "#7FD1E8", "Medium": "#2A9DF4", "Deep": "#1B3A6B"}
ZONE_ORDER = {"Depth Zone": ["Shallow", "Medium", "Deep"]}


def time_series(df, param, smooth_window=0):
    """Line chart of one parameter over time, with an optional rolling average."""
    col = PARAMETERS[param][0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Timestamp"], y=df[col], mode="lines", name="Raw reading",
        line=dict(color="#2A9DF4", width=1.5), opacity=0.55 if smooth_window else 1,
    ))
    if smooth_window:
        fig.add_trace(go.Scatter(
            x=df["Timestamp"], y=df[col].rolling(smooth_window, center=True).mean(),
            mode="lines", name=f"{smooth_window}-reading rolling avg",
            line=dict(color="#E8743B", width=3),
        ))
    fig.update_layout(
        title=f"{param} Over Time",
        xaxis_title="Time of Day (Feb 4, 2022)",
        yaxis_title=label(param),
        legend_title_text="Series",
        hovermode="x unified",
    )
    return fig


def relationship(df, x_param, y_param):
    """Scatter of two parameters, colored by depth zone (categorical legend)."""
    fig = px.scatter(
        df, x=PARAMETERS[x_param][0], y=PARAMETERS[y_param][0],
        color="Depth Zone", color_discrete_map=ZONE_COLORS, category_orders=ZONE_ORDER,
        hover_data={"Timestamp": "|%H:%M:%S"}, opacity=0.75,
        title=f"{y_param} vs. {x_param}",
        labels={PARAMETERS[x_param][0]: label(x_param), PARAMETERS[y_param][0]: label(y_param)},
    )
    fig.update_traces(marker=dict(size=7))
    return fig


def distribution(df, param):
    """Histogram of one parameter, stacked by depth zone."""
    col = PARAMETERS[param][0]
    fig = px.histogram(
        df, x=col, color="Depth Zone", nbins=30,
        color_discrete_map=ZONE_COLORS, category_orders=ZONE_ORDER,
        title=f"Distribution of {param}",
        labels={col: label(param)},
    )
    fig.update_layout(yaxis_title="Number of readings", bargap=0.05)
    return fig


def correlation_heatmap(df):
    """Correlation matrix across all tracked parameters."""
    cols = {name: col for name, (col, _, _) in PARAMETERS.items()}
    corr = df[list(cols.values())].corr().round(2)
    corr.index = corr.columns = list(cols.keys())
    fig = px.imshow(
        corr, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="How Parameters Move Together (Pearson correlation)",
    )
    fig.update_layout(coloraxis_colorbar_title="r", height=560)
    return fig


def track_map(df, param):
    """Map of the boat's path, each point colored by the chosen parameter."""
    col = PARAMETERS[param][0]
    fig = px.scatter_map(
        df, lat="Latitude", lon="Longitude", color=col,
        color_continuous_scale="Viridis", zoom=16.5, height=560,
        center={"lat": df["Latitude"].mean(), "lon": df["Longitude"].mean()},
        hover_data={"Timestamp": "|%H:%M:%S", col: ":.2f"},
        title=f"Survey Track Colored by {param}",
        labels={col: label(param)},
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(map_style="open-street-map", margin=dict(l=0, r=0, t=50, b=0))
    return fig
