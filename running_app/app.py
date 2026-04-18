# region Imports

import streamlit as st
import pandas as pd

# endregion

# region App Structure

# ===== Layout =====
st.title("AI Running Performance Analyzer")
st.caption("Upload your Garmin data to explore trends, records, and training insights.")

# ===== Data Input =====
uploaded_files = st.file_uploader(
    "Upload Garmin CSV files",
    type=["csv"],
    accept_multiple_files=True
)

# ===== Tabs =====
tab_overview, tab_trends, tab_records, tab_insights = st.tabs(
    ["Overview", "Trends", "Records", "Insights"]
)

# endregion

# region Raw Data Loading

df = None

if uploaded_files:
    dataframes = []

    # read each uploaded CSV separately
    for file in uploaded_files:
        current_df = pd.read_csv(file)

        # add source file name to track where data comes from
        current_df["source_file"] = file.name
        dataframes.append(current_df)

    # concatenate all loaded files into one unified dataset
    df = pd.concat(dataframes, ignore_index=True)

# endregion

# region Data Processing

clean_df = None

if df is not None:
    # create a clean copy of raw data for processing
    clean_df = df.copy()

    # remove columns that are duplicated/not useful for the current analysis
    clean_df = clean_df.drop(
        columns=[
            "Unnamed: 0",
            "Soļu veids",
            "Intervāls",
            "Kumulatīvais laiks",
            "Distance",
        ]
    )

    # rename key columns to consistent English snake_case names
    clean_df = clean_df.rename(
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

# endregion

# region Helpers

def get_pace_df(clean_df):
    """
    Returns a dataframe with valid pace rows and numeric pace_min column.
    Does not modify the original clean_df.
    """
    # create a copy to avoid mutating original dataframe
    pace_df = clean_df.dropna(subset=["avg_pace"]).copy()

    # keep only rows with valid "MM:SS" format
    pace_df = pace_df[pace_df["avg_pace"].str.contains(":")]

    # split pace string into minutes and seconds
    parts = pace_df["avg_pace"].str.split(":")

    # convert pace to numeric minutes
    pace_df["pace_min"] = (
        parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)
    )

    return pace_df

# endregion

# region KPIs

# KPI default values if no data is loaded
total_distance = None
avg_pace = None
weighted_avg_pace = None

if clean_df is not None:
    # calculate total distance from full dataset
    total_distance = clean_df["distance_km"].sum()

    # reuse preprocessing logic
    pace_df = get_pace_df(clean_df)

    # simple average pace
    avg_pace = pace_df["pace_min"].mean()

    # create weighted pace contribution
    pace_df["weighted_pace"] = pace_df["pace_min"] * pace_df["distance_km"]

    # calculate weighted average pace safely
    if pace_df["distance_km"].sum() > 0:
        weighted_avg_pace = (
            pace_df["weighted_pace"].sum() / pace_df["distance_km"].sum()
        )

# endregion

# region Overview Tab

with tab_overview:
    st.subheader("Overview")

    if clean_df is not None:
        st.write("Data loaded successfully.")

        if total_distance is not None:
            st.metric("Total Distance (km)", f"{total_distance:.2f}")

        if avg_pace is not None:
                minutes = int(avg_pace)
                seconds = int(round((avg_pace - minutes) * 60))
                pace_str = f"{minutes}:{seconds:02d}"
                st.metric("Average Pace (min/km)", pace_str)

        if weighted_avg_pace is not None:
                # convert weighted average pace back from decimal minutes to "MM:SS"
                weighted_minutes = int(weighted_avg_pace)
                weighted_seconds = int(round((weighted_avg_pace - weighted_minutes) * 60))
                weighted_pace_str = f"{weighted_minutes}:{weighted_seconds:02d}"

                st.metric("Weighted Average Pace (min/km)", weighted_pace_str)

        n_rows = st.slider("Rows to display", 5, 100, 20)
        st.dataframe(clean_df.head(n_rows))

        # st.write(clean_df.columns)
        # st.write(clean_df["avg_pace"].isna().sum())
        # st.write(clean_df[clean_df["avg_pace"].isna()])
        # st.write(clean_df["avg_pace"].dtype)

# endregion

# region Trends Tab

with tab_trends:
    st.subheader("Trends")

    if clean_df is not None:
        # reuse the same preprocessing function
        pace_df = get_pace_df(clean_df)

        if not pace_df.empty:
            st.subheader("Pace Distribution")

            # group pace values into bins (e.g. 10 intervals across the data range)
            bins = pd.cut(pace_df["pace_min"], bins=10)

            # count how many values fall into each bin and sort them in order
            hist_data = bins.value_counts().sort_index()

            # convert Series → DataFrame so it can be used in a chart
            hist_df = hist_data.reset_index()

            # rename columns for clarity
            hist_df.columns = ["pace_range", "count"]

            # convert interval objects (e.g. (5.0, 5.5]) to strings for chart compatibility
            hist_df["pace_range"] = hist_df["pace_range"].astype(str)

            # set pace_range as index so it becomes the X-axis in the chart
            st.bar_chart(hist_df.set_index("pace_range"))

# endregion

# region Records Tab

with tab_records:
    st.subheader("Records")

# endregion

# region Insights Tab

with tab_insights:
    st.subheader("Insights")

# endregion