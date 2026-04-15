# region App Structure

# ===== Imports =====
import streamlit as st
import pandas as pd

# ===== Layout =====
st.title("AI Running Performance Analyzer")
st.caption("Upload your Garmin data to explore trends, records, and training insights.")

# ===== Data Input =====
uploaded_file = st.file_uploader("Upload Garmin CSV file", type=["csv"])

df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# ===== Tabs =====
tab_overview, tab_trends, tab_records, tab_insights = st.tabs(
    ["Overview", "Trends", "Records", "Insights"]
)

with tab_overview:
    st.subheader("Overview")

    if df is not None:
        st.write("Data loaded successfully.")

        df = df.drop(
    columns=[
        "Unnamed: 0",
        "Soļu veids",
        "Intervāls",
        "Kumulatīvais laiks",
        "Distance"
    ]
)
        
        df = df.rename(
    columns={
        "Attālums": "distance_km",
        "Laiks": "duration",
        "Vid. temps": "avg_pace",
        "Vid. SR": "avg_cadence",
        "Maks. SR": "max_cadence",
        "Kopējais kāpums": "elevation_gain",
        "Kopējais kritums": "elevation_loss",
        "Kalorijas": "calories",
        "Labākais temps": "best_pace",
        "Kustības laiks": "moving_time",
        "Vid. kustības temps": "avg_moving_pace",
    }
)

        st.dataframe(df.head())
        st.write(df.columns)

with tab_trends:
    st.subheader("Trends")

with tab_records:
    st.subheader("Records")

with tab_insights:
    st.subheader("Insights")

# endregion