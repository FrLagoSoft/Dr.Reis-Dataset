# 🌊 Biscayne Bay Water Quality Explorer

An interactive Streamlit dashboard for exploring water-quality data collected by an autonomous surface vehicle in Biscayne Bay, Miami.

**Live app:** https://drreis-dataset-2vrsizndymopdhnsrtopdy.streamlit.app/ 

Built for **CIS 3590 – Internship-Ready Software Development** (Prof. Gregory Reis Targaryan the dragon slayer, FIU, Fall 2026).

## Purpose

Raw sensor logs are hard to read: this dataset has 942 rows and 70 columns. The app turns them into something a non-programmer can explore: filter by time, compare parameters, see where readings were taken, and read plain-English takeaways.

## Dataset

`biscayneBay_waterquality.csv` comes from the course repository ([studentgreg/CIS3590-Fall2026](https://github.com/studentgreg/CIS3590-Fall2026)). It holds about 16 minutes of one-per-second readings logged on February 4, 2022 (16:18–16:34) near 25.912° N, 80.137° W.

Parameters used in the app:

| Parameter | Column | Unit |
|---|---|---|
| Temperature | `Temperature (c)` | °C |
| Salinity | `Salinity (ppt)` | ppt |
| pH | `pH` | – |
| Dissolved Oxygen | `ODO mg/L` | mg/L |
| Oxygen Saturation | `ODOsat %` | % |
| Specific Conductance | `SpCond mS/cm` | mS/cm |
| Turbidity | `Turbid+ NTU` | NTU |
| Chlorophyll | `Chl ug/L` | µg/L |
| Water Column Depth | `Total Water Column (m)` | m |

**Cleaning:** column names are stripped of trailing spaces, a real timestamp is built from `Date m/d/y` + `Time hh:mm:ss` (the original `Time` column only holds minutes:seconds), and readings are grouped into Shallow / Medium / Deep zones by water-column depth. Turbidity and chlorophyll contain many negative values, which are physically impossible; the app flags this as a calibration issue instead of hiding it.

## Features

| Section | What you can do |
|---|---|
| **Sidebar** | Upload your own CSV (same format) and filter all views by a time window |
| **📋 Overview** | Read what the app is for; see average temperature, salinity, pH, and oxygen |
| **🗂️ Data Explorer** | Choose which columns to show, view summary statistics, download the filtered data |
| **📈 Charts** | Time series with optional rolling average, any-vs-any scatter, histograms, correlation heatmap |
| **🗺️ Map** | See the vehicle's track colored by any parameter |
| **💡 Insights** | Takeaways and data-quality warnings that recalculate for the selected time window |

## How to use

1. Open the live app (or run it locally, below).
2. Use the **Time window** slider in the sidebar to focus on part of the survey. Every tab updates.
3. Move through the tabs from left to right. Hover over any chart for exact values; drag to zoom and double-click to reset.

## Run locally

```bash
git clone https://github.com/FrLagoSoft/Dr.Reis-Dataset.git
cd Dr.Reis-Dataset
pip install -r requirements.txt
streamlit run app.py        # or: python -m streamlit run app.py
```

## Project structure

```
├── app.py                         # Streamlit UI: sidebar, tabs, page layout
├── data_utils.py                  # Loading, cleaning, filtering, summaries
├── charts.py                      # Plotly figure builders
├── biscayneBay_waterquality.csv   # Dataset
├── requirements.txt               # Dependencies
├── AGILE.md                       # User stories, sprints, retrospective
└── .streamlit/config.toml         # Theme
```

## Tech stack

Python · Streamlit · pandas · Plotly · GitHub · Streamlit Community Cloud

## Project management

Built with Agile practices: user stories, a prioritized backlog, short sprints tracked on a GitHub Projects board, and a retrospective. See [AGILE.md](AGILE.md).
