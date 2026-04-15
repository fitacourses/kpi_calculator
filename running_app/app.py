# region App Structure

# ===== Imports =====
import streamlit as st
import pandas as pd

# ===== Layout =====
st.title("AI Running Performance Analyzer")
st.caption("Upload your Garmin data to explore trends, records, and training insights.")

# ===== Data Input =====
uploaded_files = st.file_uploader(
    "Upload Garmin CSV files",
    type=["csv"],
    accept_multiple_files=True
)

df = None

if uploaded_files:
    # Read each uploaded CSV separately, then combine them into one dataframe
    dataframes = []

for file in uploaded_files:
    current_df = pd.read_csv(file)

    # Add source file name to track where data comes from
    current_df["source_file"] = file.name

    dataframes.append(current_df)

    df = pd.concat(dataframes, ignore_index=True)

# ===== Tabs =====
tab_overview, tab_trends, tab_records, tab_insights = st.tabs(
    ["Overview", "Trends", "Records", "Insights"]
)

with tab_overview:
    st.subheader("Overview")

    if df is not None:
        st.write("Data loaded successfully.")

        # Remove columns that are technical, duplicated, or not useful for the current analysis
        df = df.drop(
            columns=[
                "Unnamed: 0",
                "Soļu veids",
                "Intervāls",
                "Kumulatīvais laiks",
                "Distance"
            ]
        )

        # Rename key columns to consistent English snake_case names
        # so the rest of the code is easier to read and maintain
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