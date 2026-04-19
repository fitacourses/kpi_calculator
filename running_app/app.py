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
    "Upload Garmin CSV files", type=["csv"], accept_multiple_files=True
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
        ],
        # ignore not existing columns
        errors="ignore",
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
            "Datums": "activity_date",
        }
    )
    # convert activity_date to datetime for time-based analysis
    clean_df["activity_date"] = pd.to_datetime(clean_df["activity_date"])

    # normalize datetime so runs from the same day can be grouped together
    clean_df["activity_date"] = clean_df["activity_date"].dt.normalize()

    # convert calories from string with comma decimal separator to numeric float
    if "calories" in clean_df.columns:
        clean_df["calories"] = (
            clean_df["calories"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    if "elevation_gain" in clean_df.columns:
        clean_df["elevation_gain"] = pd.to_numeric(
            clean_df["elevation_gain"], errors="coerce"
        )

# endregion

# region Helpers


def get_pace_df(clean_df):
    # keep only rows with valid avg_pace values and convert pace to numeric minutes

    # create a copy so the original cleaned dataframe stays unchanged
    pace_df = clean_df.dropna(subset=["avg_pace"]).copy()

    # keep only pace values that look like "MM:SS"
    pace_df = pace_df[pace_df["avg_pace"].str.contains(":")]

    # split pace string into minutes and seconds parts
    parts = pace_df["avg_pace"].str.split(":")

    # convert "MM:SS" pace into decimal minutes
    # example: 5:30 -> 5.5
    pace_df["pace_min"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)

    # create weighted pace component so daily pace can be calculated
    # as sum(pace * distance) / sum(distance)
    pace_df["pace_x_distance"] = pace_df["pace_min"] * pace_df["distance_km"]

    return pace_df


def get_daily_pace_df(pace_df):
    # Aggregate session-level pace data into one weighted pace value per day

    # group all runs by date so each day becomes one row
    daily = (
        pace_df.groupby("activity_date")
        .agg(
            total_distance_km=("distance_km", "sum"),
            total_pace_x_distance=("pace_x_distance", "sum"),
        )
        .reset_index()
    )

    # calculate weighted daily pace
    daily["daily_pace_min"] = (
        daily["total_pace_x_distance"] / daily["total_distance_km"]
    )

    return daily


def get_pace_df_with_types(clean_df):
    # start from the existing pace helper
    pace_df = get_pace_df(clean_df)

    # classify each run by distance
    pace_df["run_type"] = pd.cut(
        pace_df["distance_km"],
        bins=[0, 7, 13, float("inf")],
        labels=["short (<7 km)", "medium (7–13 km)", "long (>13 km)"],
        include_lowest=True,
    )

    return pace_df


def format_minutes_to_hhmmss(time_min):
    total_seconds = int(round(time_min * 60))

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


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

            # create a copy for display so original data stays unchanged
            display_df = clean_df.copy()

            # format datetime column to show only date (no time)
            display_df["activity_date"] = display_df["activity_date"].dt.strftime(
                "%Y-%m-%d"
            )

            if "calories" in clean_df.columns:
                total_calories = clean_df["calories"].sum()
                st.metric("Total Calories", int(total_calories))

            columns_to_show = [
                "activity_date",
                "distance_km",
                "avg_pace",
                "calories",
            ]
            n_rows = st.slider("Rows to display", 5, 100, 20)

            st.dataframe(display_df[columns_to_show].head(n_rows))
# endregion

# region Trends Tab

with tab_trends:
    st.subheader("Trends")

    if clean_df is not None:
        pace_df = get_pace_df_with_types(clean_df)

        if not pace_df.empty:

            # remove very short or very slow runs from the summary
            # so unusual recovery runs or noisy entries do not distort the averages
            pace_df_filtered = pace_df[
                (pace_df["distance_km"] > 2) & (pace_df["pace_min"] < 9)
            ]

            # summarise each run category to compare volume and pace by run type
            run_summary = pace_df_filtered.groupby("run_type", as_index=False).agg(
                runs=("run_type", "count"),
                avg_pace_min=("pace_min", "mean"),
                total_distance_km=("distance_km", "sum"),
            )

            minutes = run_summary["avg_pace_min"].astype(int)
            seconds = ((run_summary["avg_pace_min"] - minutes) * 60).round().astype(int)

            run_summary["avg_pace"] = (
                minutes.astype(str) + ":" + seconds.astype(str).str.zfill(2)
            )

            st.subheader("Run Type Summary")
            st.dataframe(
                run_summary[["run_type", "runs", "avg_pace", "total_distance_km"]]
            )

            # aggregate session-level runs into one weighted pace value per day
            daily_pace_df = get_daily_pace_df(pace_df)

            # sort by date before creating any rolling trend calculation
            daily_pace_df = daily_pace_df.sort_values("activity_date")

            # smooth the daily pace line so the chart shows trend more clearly
            # instead of only day-to-day noise
            daily_pace_df["pace_smooth"] = (
                daily_pace_df["daily_pace_min"].rolling(window=5, min_periods=1).mean()
            )

            # convert numeric pace into MM:SS format for easier human reading
            minutes = daily_pace_df["daily_pace_min"].astype(int)
            seconds = (
                ((daily_pace_df["daily_pace_min"] - minutes) * 60).round().astype(int)
            )
            daily_pace_df["pace_str"] = (
                minutes.astype(str) + ":" + seconds.astype(str).str.zfill(2)
            )

            if not daily_pace_df.empty:
                st.subheader("Pace Over Time")

                # plot the smoothed pace line to make the trend easier to interpret
                st.line_chart(daily_pace_df.set_index("activity_date")["pace_smooth"])

            st.subheader("Pace vs Distance")

            # use session-level data for each point
            st.scatter_chart(pace_df, x="distance_km", y="pace_min")

            # show time-based charts only if activity_date exists
            if "activity_date" in clean_df.columns:
                st.subheader("Distance Over Time")

                # combine all runs from the same day into one total daily distance
                daily_distance = clean_df.groupby("activity_date", as_index=False)[
                    "distance_km"
                ].sum()

                # sort by date so the timeline is drawn in the correct order
                daily_distance = daily_distance.sort_values("activity_date")

                # plot total distance per day
                st.line_chart(daily_distance.set_index("activity_date")["distance_km"])

            if "elevation_gain" in clean_df.columns:
                st.subheader("Elevation Gain vs Distance")

                st.scatter_chart(clean_df, x="distance_km", y="elevation_gain")

                st.subheader("Calories Over Time")

                daily_calories = clean_df.groupby("activity_date", as_index=False)[
                    "calories"
                ].sum()

                daily_calories = daily_calories.sort_values("activity_date")

                st.line_chart(daily_calories.set_index("activity_date")["calories"])

# endregion

# region Records Calculations

# default values for records
longest_run = None
best_5k_time = None
best_10k_time = None
best_21k_time = None

if clean_df is not None:
    # get the longest distance from the cleaned dataset
    longest_run = clean_df["distance_km"].max()

    # get the full row of the fastest run
    fastest_run = pace_df.loc[pace_df["pace_min"].idxmin()]

    # reuse pace preprocessing for pace-based records
    pace_df = get_pace_df(clean_df)

    if not pace_df.empty:
        # find runs long enough for each target distance
        runs_5k = pace_df[pace_df["distance_km"] >= 5]
        runs_10k = pace_df[pace_df["distance_km"] >= 10]
        runs_21k = pace_df[pace_df["distance_km"] >= 21]

        # estimate best target times from the fastest eligible run pace
        if not runs_5k.empty:
            best_5k_time = runs_5k["pace_min"].min() * 5

        if not runs_10k.empty:
            best_10k_time = runs_10k["pace_min"].min() * 10

        if not runs_21k.empty:
            best_21k_time = runs_21k["pace_min"].min() * 21
        # endregion

# region Records Tab

with tab_records:
    st.subheader("Records")

    if clean_df is not None:
        if longest_run is not None:
            st.metric("Longest Run (km)", f"{longest_run:.2f}")

        if best_5k_time is not None:
            st.metric("Best 5K Time", format_minutes_to_hhmmss(best_5k_time))

        if best_10k_time is not None:
            st.metric("Best 10K Time", format_minutes_to_hhmmss(best_10k_time))

        if best_21k_time is not None:
            st.metric("Best 21K Time", format_minutes_to_hhmmss(best_21k_time))


# endregion

# region Insights Tab

with tab_insights:
    st.subheader("Insights")

    if clean_df is not None:
        pace_df = get_pace_df_with_types(clean_df)

        if not pace_df.empty:
            # --- METRICS ---
            avg_distance = pace_df["distance_km"].mean()

            runs_per_week = (
                pace_df.set_index("activity_date")
                .resample("W")["distance_km"]
                .count()
                .mean()
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Average distance per run", f"{avg_distance:.2f} km")

            with col2:
                st.metric("Average runs per week", f"{runs_per_week:.1f}")

            # --- INSIGHTS ---
            daily_pace_df = get_daily_pace_df(pace_df)

            if not daily_pace_df.empty:
                recent = daily_pace_df.tail(7)["daily_pace_min"].mean()
                older = daily_pace_df.head(7)["daily_pace_min"].mean()

                if recent < older:
                    st.success("You are getting faster recently.")
                else:
                    st.warning("Pace has slowed down recently.")

            corr = pace_df["distance_km"].corr(pace_df["pace_min"])

            if corr > 0.2:
                st.info("You tend to slow down as distance increases.")
            elif corr < -0.2:
                st.info("You maintain or improve pace on longer runs.")
            else:
                st.info("Your pace is relatively independent of distance.")
# endregion
