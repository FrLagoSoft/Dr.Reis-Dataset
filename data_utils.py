"""
data_utils.py
-------------
Data loading, cleaning, and summary helpers for the Biscayne Bay
Water Quality Explorer. Keeping this logic out of app.py makes the
UI code shorter and lets each function be tested on its own.
"""

import pandas as pd
import streamlit as st

DEFAULT_CSV = "biscayneBay_waterquality.csv"

# Friendly parameter names -> (CSV column, unit, short description).
# One dictionary drives every dropdown, label, and metric in the app,
# so adding a new parameter only requires adding one line here.
PARAMETERS = {
    "Temperature": ("Temperature (c)", "°C", "Water temperature from the CTD sensor."),
    "Salinity": ("Salinity (ppt)", "ppt", "Dissolved salt content, in parts per thousand."),
    "pH": ("pH", "", "Acidity/alkalinity of the water (7 = neutral)."),
    "Dissolved Oxygen": ("ODO mg/L", "mg/L", "Oxygen available to marine life."),
    "Oxygen Saturation": ("ODOsat %", "%", "Dissolved oxygen as a percent of saturation."),
    "Specific Conductance": ("SpCond mS/cm", "mS/cm", "Ability of water to conduct electricity."),
    "Turbidity": ("Turbid+ NTU", "NTU", "Cloudiness of the water."),
    "Chlorophyll": ("Chl ug/L", "µg/L", "Proxy for algae concentration."),
    "Water Column Depth": ("Total Water Column (m)", "m", "Distance from surface to seafloor."),
}

# Columns the app cannot run without (used to validate uploaded files).
REQUIRED_COLUMNS = ["Latitude", "Longitude", "Date m/d/y", "Time hh:mm:ss"] + [
    col for col, _, _ in PARAMETERS.values()
]


def label(name: str) -> str:
    """Return an axis label like 'Temperature (°C)' for a friendly parameter name."""
    unit = PARAMETERS[name][1]
    return f"{name} ({unit})" if unit else name


@st.cache_data
def load_data(source=DEFAULT_CSV) -> pd.DataFrame:
    """Read a CSV (path or uploaded file) and return a cleaned DataFrame.

    Cleaning steps:
      1. Strip stray whitespace from column names ("Date m/d/y   " -> "Date m/d/y").
      2. Build a real Timestamp from the sonde's date and time columns
         (the original 'Time' column only holds minutes:seconds).
      3. Sort chronologically and add 'Elapsed (min)' since mission start.
      4. Add a categorical 'Depth Zone' used to color charts with a legend.
    """
    df = pd.read_csv(source)
    df.columns = df.columns.str.strip()

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df["Timestamp"] = pd.to_datetime(
        df["Date m/d/y"].astype(str).str.strip() + " " + df["Time hh:mm:ss"].astype(str),
        format="%m/%d/%y %H:%M:%S",
        errors="coerce",
    )
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp").reset_index(drop=True)
    df["Elapsed (min)"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds() / 60

    depth_col = PARAMETERS["Water Column Depth"][0]
    df["Depth Zone"] = pd.qcut(
        df[depth_col], q=3, labels=["Shallow", "Medium", "Deep"], duplicates="drop"
    ).astype(str)
    return df


def filter_by_time(df: pd.DataFrame, start, end) -> pd.DataFrame:
    """Keep only rows whose Timestamp falls within [start, end]."""
    return df[(df["Timestamp"] >= start) & (df["Timestamp"] <= end)]


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Min / mean / max / std for every tracked parameter, with friendly names."""
    rows = []
    for name, (col, unit, _) in PARAMETERS.items():
        s = df[col]
        rows.append({
            "Parameter": name,
            "Unit": unit,
            "Min": s.min(),
            "Mean": s.mean(),
            "Max": s.max(),
            "Std Dev": s.std(),
        })
    return pd.DataFrame(rows).set_index("Parameter").round(2)


def quality_flags(df: pd.DataFrame) -> list[str]:
    """Return plain-English warnings about physically impossible readings."""
    flags = []
    for name in ["Turbidity", "Chlorophyll"]:
        col = PARAMETERS[name][0]
        pct = (df[col] < 0).mean() * 100
        if pct > 0:
            flags.append(
                f"**{name}**: {pct:.0f}% of readings are negative, which is physically "
                "impossible. This usually means the sensor needed recalibration, so "
                "treat these values as relative, not absolute."
            )
    return flags
