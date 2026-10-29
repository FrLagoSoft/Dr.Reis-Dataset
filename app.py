"""
app.py
------
Biscayne Bay Water Quality Explorer
CIS 3590 - Internship-Ready Software Development (Prof. Gregory Reis)

Entry point for the Streamlit app. Run locally with:
    streamlit run app.py
(or: python -m streamlit run app.py)

Layout:
    Sidebar  -> data source + global time-window filter
    Tabs     -> Overview | Data Explorer | Charts | Map | Insights
"""

import streamlit as st

import charts
from data_utils import (
    PARAMETERS, filter_by_time, label, load_data, quality_flags, summary_table,
)

st.set_page_config(page_title="Biscayne Bay Water Quality", page_icon="🌊", layout="wide")


# ---------------------------------------------------------------- sidebar
def sidebar_controls():
    """Render the sidebar and return the filtered DataFrame plus the full one."""
    st.sidebar.title("🌊 Controls")

    st.sidebar.subheader("1. Data source")
    uploaded = st.sidebar.file_uploader(
        "Upload your own CSV (optional)", type=["csv"],
        help="Must have the same columns as the Biscayne Bay dataset.",
    )
    try:
        df = load_data(uploaded) if uploaded else load_data()
        st.sidebar.success("Using uploaded file" if uploaded else "Using sample dataset")
    except Exception as err:  # bad upload -> fall back instead of crashing
        st.sidebar.error(f"Couldn't read that file ({err}). Showing the sample dataset.")
        df = load_data()

    st.sidebar.subheader("2. Time window")
    t_min, t_max = df["Timestamp"].min().to_pydatetime(), df["Timestamp"].max().to_pydatetime()
    start, end = st.sidebar.slider(
        "Readings between", min_value=t_min, max_value=t_max,
        value=(t_min, t_max), format="HH:mm:ss",
    )
    filtered = filter_by_time(df, start, end)
    st.sidebar.caption(f"Showing **{len(filtered):,}** of {len(df):,} readings.")

    st.sidebar.divider()
    st.sidebar.caption("CIS 3590 · Fall 2026 · Built with Streamlit + Plotly")
    return df, filtered


# ---------------------------------------------------------------- helpers
def describe_r(r):
    """Turn a correlation coefficient into plain English."""
    strength = "strong" if abs(r) >= 0.7 else "moderate" if abs(r) >= 0.3 else "weak"
    direction = "positive" if r > 0 else "negative"
    return f"{strength} {direction}"


# ---------------------------------------------------------------- tabs
def overview_tab(df):
    st.subheader("What is this app?")
    st.markdown(
        "This dashboard explores water-quality data collected by an **autonomous "
        "surface vehicle** in **Biscayne Bay, Miami** on February 4, 2022. Over about "
        "16 minutes the boat logged a reading every second: GPS position, temperature, "
        "salinity, pH, dissolved oxygen, and more.\n\n"
        "**How to use it:** narrow the time window in the sidebar, then move through "
        "the tabs. Every chart and table updates to match your selection."
    )
    st.markdown("#### Averages for the selected window")
    cols = st.columns(4)
    for c, name in zip(cols, ["Temperature", "Salinity", "pH", "Dissolved Oxygen"]):
        col, unit, desc = PARAMETERS[name]
        c.metric(name, f"{df[col].mean():.2f} {unit}".strip(), help=desc)

    with st.expander("What do these parameters mean?"):
        for name, (_, unit, desc) in PARAMETERS.items():
            st.markdown(f"- **{label(name)}**: {desc}")


def data_tab(df):
    st.subheader("Data Explorer")
    st.markdown("Pick the columns you care about to keep the table readable.")
    default = ["Timestamp"] + [PARAMETERS[p][0] for p in ["Temperature", "Salinity", "pH", "Dissolved Oxygen"]]
    chosen = st.multiselect("Columns to display", options=list(df.columns), default=default)
    if chosen:
        st.dataframe(df[chosen], width="stretch", height=350)
    else:
        st.info("Select at least one column to show the table.")

    st.markdown("#### Summary statistics")
    st.dataframe(summary_table(df), width="stretch")
    st.download_button(
        "⬇️ Download filtered data (CSV)", df.to_csv(index=False).encode(),
        file_name="biscayne_bay_filtered.csv", mime="text/csv",
    )


def charts_tab(df):
    names = list(PARAMETERS)
    st.subheader("Trends over time")
    c1, c2 = st.columns([2, 1])
    param = c1.selectbox("Parameter", names, key="ts_param")
    smooth = c2.checkbox("Show rolling average", value=True)
    window = c2.slider("Smoothing window (readings)", 5, 60, 20, disabled=not smooth)
    st.plotly_chart(charts.time_series(df, param, window if smooth else 0), width="stretch")
    st.caption("A rolling average hides second-to-second sensor noise so the real trend is easier to see.")

    st.divider()
    st.subheader("Relationships between parameters")
    c1, c2 = st.columns(2)
    x = c1.selectbox("X axis", names, index=names.index("Temperature"))
    y = c2.selectbox("Y axis", names, index=names.index("Dissolved Oxygen"))
    st.plotly_chart(charts.relationship(df, x, y), width="stretch")
    st.caption("Points are grouped into depth zones (thirds of the measured water-column depth).")

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("Distribution")
        dist_param = st.radio("Parameter", ["Temperature", "Salinity", "Dissolved Oxygen", "pH"], horizontal=True)
        st.plotly_chart(charts.distribution(df, dist_param), width="stretch")
    with right:
        st.subheader("Correlations")
        st.plotly_chart(charts.correlation_heatmap(df), width="stretch")


def map_tab(df):
    st.subheader("Where were the readings taken?")
    param = st.selectbox("Color the track by", list(PARAMETERS), key="map_param")
    st.plotly_chart(charts.track_map(df, param), width="stretch")
    st.caption("Hover over any point to see the exact time and value. Scroll to zoom.")


def insights_tab(df):
    st.subheader("Key insights")
    temp, sal, odo, depth = (PARAMETERS[p][0] for p in
                             ["Temperature", "Salinity", "Dissolved Oxygen", "Water Column Depth"])
    r_temp_odo = df[temp].corr(df[odo])
    r_depth_sal = df[depth].corr(df[sal])
    st.markdown(f"""
- **Water was warm and stable.** Temperature ranged only {df[temp].min():.1f}–{df[temp].max():.1f} °C in this window.
- **Salinity was high for a bay** (mean {df[sal].mean():.1f} ppt, open ocean is ~35), which is typical of shallow,
  sun-warmed areas where evaporation concentrates salt.
- **Oxygen looked healthy.** Dissolved oxygen averaged {df[odo].mean():.2f} mg/L; values above ~4 mg/L
  generally support fish and seagrass.
- **Depth vs. salinity** correlation is r = {r_depth_sal:.2f}
  ({describe_r(r_depth_sal)}).
""")
    # Physics says warmer water holds less oxygen (negative r). Explain whichever we observe.
    if r_temp_odo < -0.1:
        note = "a negative relationship, matching the physics: warmer water holds less dissolved oxygen."
    else:
        note = ("not the negative relationship physics would predict for warmer water. Over a short "
                "16-minute survey, location (e.g. seagrass producing oxygen, or the warmer water at "
                "the start of the run) likely matters more than temperature itself. Check the Map tab.")
    st.markdown(f"- **Temperature vs. oxygen** correlation is r = {r_temp_odo:.2f}, {note}")
    st.caption("These numbers recalculate whenever you change the time window.")

    flags = quality_flags(df)
    if flags:
        st.markdown("#### ⚠️ Data quality notes")
        for f in flags:
            st.warning(f)


# ---------------------------------------------------------------- main
def main():
    df_full, df = sidebar_controls()

    st.title("🌊 Biscayne Bay Water Quality Explorer")
    st.caption("CIS 3590 – Internship-Ready Software Development · Prof. Gregory Reis")

    if df.empty:
        st.warning("No readings in this time window. Widen the slider in the sidebar.")
        return

    tabs = st.tabs(["📋 Overview", "🗂️ Data Explorer", "📈 Charts", "🗺️ Map", "💡 Insights"])
    for tab, render in zip(tabs, [overview_tab, data_tab, charts_tab, map_tab, insights_tab]):
        with tab:
            render(df)


if __name__ == "__main__":
    main()
