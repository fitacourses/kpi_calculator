# region Imports

import streamlit as st
import pandas as pd
import altair as alt
import math
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import io

# endregion

# region App Structure

# ===== Layout =====
st.title("Running Performance Analyzer (Garmin CSV)")
st.caption(
    "Upload Garmin CSV exports to see pace trends, estimated PRs, and simple coaching signals from pace + heart rate."
)

# CSS for the coach-style recommendation boxes.
st.markdown(
    """
<style>
.coach-box {
  border-radius: 12px;
  padding: 14px 16px;
  margin: 10px 0 14px 0;
  border: 1px solid rgba(255,255,255,0.10);
}
.coach-box h4 {
  margin: 0 0 6px 0;
  font-size: 1.05rem;
  font-weight: 700;
}
.coach-box p {
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.35;
}
.coach-success { background: rgba(46, 160, 67, 0.12); border-color: rgba(46, 160, 67, 0.35); }
.coach-warn { background: rgba(245, 158, 11, 0.12); border-color: rgba(245, 158, 11, 0.35); }
.coach-error { background: rgba(239, 68, 68, 0.12); border-color: rgba(239, 68, 68, 0.35); }
.coach-info { background: rgba(59, 130, 246, 0.12); border-color: rgba(59, 130, 246, 0.35); }
</style>
""",
    unsafe_allow_html=True,
)

# ===== Data Input =====
uploaded_files = st.file_uploader(
    "Upload Garmin CSV files", type=["csv"], accept_multiple_files=True
)

# ===== Local History (optional) =====
# Saves uploaded CSVs to local disk so you can compare new activities with older ones later.
# Note: in cloud deployments, filesystem storage may be ephemeral.
HISTORY_DIR = Path(__file__).parent / ".upload_history"
INDEX_PATH = HISTORY_DIR / "index.json"


def _load_history_index():
    if not INDEX_PATH.exists():
        return {"version": 1, "files": {}}
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        # If index is corrupted, start fresh (avoid breaking the app).
        return {"version": 1, "files": {}}


def _save_history_index(index_data):
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index_data, indent=2), encoding="utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_uploaded_files_to_history(files) -> tuple[int, int]:
    """
    Save uploaded Streamlit files to HISTORY_DIR.
    Returns (saved_count, skipped_count) where skipped means "already exists".
    """
    if not files:
        return (0, 0)

    index_data = _load_history_index()
    files_index = index_data.setdefault("files", {})

    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    saved = 0
    skipped = 0

    for f in files:
        data = f.getvalue()
        file_hash = _sha256_bytes(data)
        if file_hash in files_index:
            skipped += 1
            continue

        out_path = HISTORY_DIR / f"{file_hash}.csv"
        out_path.write_bytes(data)
        files_index[file_hash] = {
            "original_name": getattr(f, "name", "uploaded.csv"),
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        saved += 1

    _save_history_index(index_data)
    return (saved, skipped)


def load_history_csvs() -> pd.DataFrame:
    index_data = _load_history_index()
    files_index = index_data.get("files", {})
    if not files_index:
        return pd.DataFrame()

    dfs = []
    for file_hash, meta in files_index.items():
        path = HISTORY_DIR / f"{file_hash}.csv"
        if not path.exists():
            continue
        try:
            df_part = pd.read_csv(path)
            df_part["source_file"] = meta.get("original_name", f"{file_hash}.csv")
            df_part["source_hash"] = file_hash
            df_part["source_kind"] = "history"
            dfs.append(df_part)
        except Exception:
            # Skip unreadable files rather than breaking the app.
            continue

    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


with st.expander("Saved history (optional)", expanded=False):
    history_index = _load_history_index()
    history_count = len(history_index.get("files", {}))
    st.caption(
        f"Saved CSV files on disk: {history_count}. Useful for comparing new uploads with older runs."
    )
    use_history = st.checkbox("Include saved history in analysis", value=False)

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button(
            "Save current uploads to history",
            disabled=not uploaded_files,
            use_container_width=True,
        ):
            saved_n, skipped_n = save_uploaded_files_to_history(uploaded_files)
            if saved_n > 0:
                st.success(f"Saved {saved_n} file(s) to history.")
            if skipped_n > 0:
                st.info(f"Skipped {skipped_n} already-saved file(s).")
    with col_h2:
        if st.button(
            "Clear saved history",
            disabled=history_count == 0,
            use_container_width=True,
        ):
            # Remove index + files. Keep it simple and safe: only touch HISTORY_DIR.
            try:
                if INDEX_PATH.exists():
                    INDEX_PATH.unlink()
                if HISTORY_DIR.exists():
                    for p in HISTORY_DIR.glob("*.csv"):
                        p.unlink(missing_ok=True)
            except Exception:
                st.error("Could not clear history (filesystem permissions).")
            else:
                st.success("Saved history cleared.")

# ===== Tabs =====
# Keep the app simple: Overview, Trends, Insights.
tab_overview, tab_trends, tab_insights = st.tabs(["Overview", "Trends", "Insights"])

# endregion

# region Raw Data Loading

df = None

dataframes = []

if "use_history" in globals() and use_history:
    history_df = load_history_csvs()
    if not history_df.empty:
        dataframes.append(history_df)

if uploaded_files:
    # Read each uploaded CSV separately
    for file in uploaded_files:
        file_bytes = file.getvalue()
        current_df = pd.read_csv(io.BytesIO(file_bytes))

        # Add source tracking (helps debugging / future comparisons).
        current_df["source_file"] = file.name
        current_df["source_hash"] = _sha256_bytes(file_bytes)
        current_df["source_kind"] = "upload"
        dataframes.append(current_df)

if dataframes:
    # Concatenate all loaded files into one unified dataset.
    df = pd.concat(dataframes, ignore_index=True)
    # Prevent double-counting if the same activity appears in both history and uploads.
    df = df.drop_duplicates().reset_index(drop=True)

# endregion

# region Data Processing

clean_df = None

if df is not None:
    # Create a clean copy for processing.
    clean_df = df.copy()

    # Remove duplicated / non-useful columns (`errors="ignore"` avoids crashing if a column is missing).
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

    # Rename columns to consistent English snake_case names.
    clean_df = clean_df.rename(
        columns={
            "Attālums": "distance_km",
            "Laiks": "duration",
            "Vid. temps": "avg_pace",
            # Heart rate (beats per minute)
            "Vid. SR": "avg_heart_rate",
            "Maks. SR": "max_heart_rate",
            "Kopējais kāpums": "elevation_gain",
            "Kopējais kritums": "elevation_loss",
            "Kalorijas": "calories",
            "Labākais temps": "best_pace",
            "Kustības laiks": "moving_time",
            "Vid. kustības temps": "avg_moving_pace",
            "Datums": "activity_date",
        }
    )
    # Convert activity_date to datetime (needed for grouping by day/week).
    clean_df["activity_date"] = pd.to_datetime(clean_df["activity_date"])

    # Normalize to day (00:00:00) so same-day activities group together.
    clean_df["activity_date"] = clean_df["activity_date"].dt.normalize()

    # Convert calories to float (some exports use comma as decimal separator).
    if "calories" in clean_df.columns:
        clean_df["calories"] = (
            clean_df["calories"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    # Coerce numeric columns once here, so the rest of the app can assume correct types.
    if "elevation_gain" in clean_df.columns:
        clean_df["elevation_gain"] = pd.to_numeric(
            clean_df["elevation_gain"], errors="coerce"
        )

    # Convert heart rate columns to numeric if they exist (some exports store them as strings).
    if "avg_heart_rate" in clean_df.columns:
        clean_df["avg_heart_rate"] = pd.to_numeric(
            clean_df["avg_heart_rate"], errors="coerce"
        )
    if "max_heart_rate" in clean_df.columns:
        clean_df["max_heart_rate"] = pd.to_numeric(
            clean_df["max_heart_rate"], errors="coerce"
        )

# endregion

# region Helpers


def get_pace_df(clean_df):
    # Convert avg_pace from "MM:SS" into decimal minutes, and add pace_x_distance for weighted averages.
    # This function is used everywhere we need reliable pace numbers.
    safe_cols = [
        "activity_date",
        "distance_km",
        "avg_pace",
        "pace_min",
        "pace_x_distance",
        "avg_heart_rate",
        "duration",
        "max_heart_rate",
    ]

    if clean_df is None:
        return pd.DataFrame(columns=safe_cols)

    if "avg_pace" not in clean_df.columns or "distance_km" not in clean_df.columns:
        return pd.DataFrame(columns=safe_cols)

    pace_df = clean_df.dropna(subset=["avg_pace"]).copy()
    pace_df = pace_df[pace_df["avg_pace"].astype(str).str.contains(":")]

    # Split "MM:SS" and convert to a single float: minutes + seconds/60.
    parts = pace_df["avg_pace"].astype(str).str.split(":")
    pace_df["pace_min"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)

    # Weighted pace component (pace * distance) for later aggregation.
    pace_df["pace_x_distance"] = pace_df["pace_min"] * pace_df["distance_km"]

    return pace_df


def get_daily_pace_df(pace_df):
    # Daily totals + distance-weighted daily pace.
    # The weighting prevents short runs from dominating the daily average.
    daily = (
        pace_df.groupby("activity_date")
        .agg(
            total_distance_km=("distance_km", "sum"),
            total_pace_x_distance=("pace_x_distance", "sum"),
        )
        .reset_index()
    )

    daily["daily_pace_min"] = (
        daily["total_pace_x_distance"] / daily["total_distance_km"]
    )

    return daily


def get_pace_df_with_types(clean_df):
    # Classify each run into a simple distance-based bucket for summaries.
    pace_df = get_pace_df(clean_df)

    if pace_df.empty or "distance_km" not in pace_df.columns:
        return pace_df

    # `pd.cut` maps a numeric value into a category based on distance bins.
    pace_df["run_type"] = pd.cut(
        pace_df["distance_km"],
        bins=[0, 7, 13, float("inf")],
        labels=["short (<7 km)", "medium (7–13 km)", "long (>13 km)"],
        include_lowest=True,
    )

    return pace_df


def get_effort_proxy_df(clean_df):
    # Return bpm + pace_min pairs (one point per run) for the Effort Proxy scatter plot.
    if clean_df is None or "avg_heart_rate" not in clean_df.columns:
        return pd.DataFrame(columns=["bpm", "pace_min"])

    pace_df = get_pace_df(clean_df)

    effort_df = pace_df.copy()
    effort_df["bpm"] = pd.to_numeric(effort_df["avg_heart_rate"], errors="coerce")

    effort_df = effort_df.dropna(subset=["bpm", "pace_min"])

    return effort_df[["bpm", "pace_min"]]


def get_effort_proxy_runs_df(clean_df):
    # Return run-level rows needed for "Insights" coaching logic.
    # We keep a minimal set of numeric columns:
    # - bpm (average HR)
    # - max_bpm (max HR, when available)
    # - pace_min (min/km as decimal)
    # - duration_min (minutes)
    if clean_df is None or "avg_heart_rate" not in clean_df.columns:
        return pd.DataFrame(
            columns=[
                "activity_date",
                "distance_km",
                "pace_min",
                "bpm",
                "duration_min",
                "max_bpm",
            ]
        )

    pace_df = get_pace_df(clean_df)

    effort_df = pace_df.copy()
    effort_df["bpm"] = pd.to_numeric(effort_df["avg_heart_rate"], errors="coerce")

    # Duration is optional in some exports; we only compute duration_min when possible.
    if "duration" in effort_df.columns:
        duration_td = pd.to_timedelta(effort_df["duration"], errors="coerce")
        effort_df["duration_min"] = duration_td.dt.total_seconds() / 60.0
    else:
        effort_df["duration_min"] = float("nan")

    required_cols = [
        "activity_date",
        "distance_km",
        "pace_min",
        "bpm",
        "duration_min",
        "max_bpm",
    ]
    effort_df = effort_df.dropna(
        subset=["activity_date", "distance_km", "pace_min", "bpm"]
    )

    # Guardrails: ignore impossible or corrupted pace values (keeps charts stable).
    # This keeps the Effort Proxy chart and Insights logic realistic.
    # - too fast: faster than 3:00 min/km
    # - too slow: slower than 10:00 min/km
    effort_df = effort_df[effort_df["pace_min"] >= 3.0]
    effort_df = effort_df[effort_df["pace_min"] <= 10.0]

    # max_bpm is optional, but helps session labeling (interval spikes).
    if "max_heart_rate" in effort_df.columns:
        effort_df["max_bpm"] = pd.to_numeric(
            effort_df["max_heart_rate"], errors="coerce"
        )
    else:
        effort_df["max_bpm"] = float("nan")

    return effort_df[required_cols]


def format_pace_min_to_mmss(pace_min):
    # Convert a pace value like 5.75 (min/km) into a string like "5:45".
    # This is only for display (tooltips/metrics), charts still use numeric `pace_min`.
    minutes = int(pace_min)
    seconds = int(round((pace_min - minutes) * 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d}"


def get_run_streaks(activity_date_series: pd.Series) -> pd.DataFrame:
    """
    Compute streaks of consecutive calendar days with at least one run.
    Returns a dataframe with: start_date, end_date, days (int).
    """
    if activity_date_series is None:
        return pd.DataFrame(columns=["start_date", "end_date", "days"])

    dates = pd.to_datetime(activity_date_series, errors="coerce").dropna()
    if dates.empty:
        return pd.DataFrame(columns=["start_date", "end_date", "days"])

    unique_days = pd.Series(dates.dt.normalize().unique()).sort_values()
    if unique_days.empty:
        return pd.DataFrame(columns=["start_date", "end_date", "days"])

    streaks = []
    start_day = unique_days.iloc[0]
    prev_day = unique_days.iloc[0]
    length_days = 1

    for day in unique_days.iloc[1:]:
        if (day - prev_day).days == 1:
            length_days += 1
        else:
            streaks.append(
                {"start_date": start_day, "end_date": prev_day, "days": length_days}
            )
            start_day = day
            length_days = 1
        prev_day = day

    streaks.append({"start_date": start_day, "end_date": prev_day, "days": length_days})
    return pd.DataFrame(streaks)


def coach_action_box(title, message, tone="info"):
    # Render a larger, colored box for important messages.
    # We use a small set of tones to keep styling consistent.
    tone_class = "coach-info"
    if tone == "success":
        tone_class = "coach-success"
    elif tone == "warning":
        tone_class = "coach-warn"
    elif tone == "error":
        tone_class = "coach-error"
    elif tone == "info":
        tone_class = "coach-info"

    st.markdown(
        f"""
<div class="coach-box {tone_class}">
  <h4>{title}</h4>
  <p>{message}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def format_minutes_to_hhmmss(time_min):
    # convert decimal minutes -> HH:MM:SS (for records display)
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

# Summary numbers used in the Overview tab.
# KPI default values
total_distance = None
avg_pace = None
total_calories = None

if clean_df is not None:
    if "distance_km" in clean_df.columns:
        total_distance = clean_df["distance_km"].sum()
    else:
        total_distance = None

    pace_df = get_pace_df(clean_df)

    if (
        not pace_df.empty
        and "distance_km" in pace_df.columns
        and pace_df["distance_km"].sum() > 0
    ):
        # Use a distance-weighted pace so short runs do not skew the average too much.
        weighted_pace_sum = (pace_df["pace_min"] * pace_df["distance_km"]).sum()
        total_distance_km = pace_df["distance_km"].sum()
        avg_pace = weighted_pace_sum / total_distance_km

    if "calories" in clean_df.columns:
        total_calories = clean_df["calories"].sum()

# endregion

# region Overview Tab

with tab_overview:
    st.subheader("Overview")

    if clean_df is not None:
        st.write("Data loaded successfully.")

        # create a copy for display so original data stays unchanged
        display_df = clean_df.copy()

        # format datetime column to show only date (no time)
        display_df["activity_date"] = display_df["activity_date"].dt.strftime(
            "%Y-%m-%d"
        )

        # Pick a small, human-friendly set of columns for the activities table.
        # (Some CSV exports may not contain all columns, so we filter to "available" ones.)
        columns_to_show = [
            "activity_date",
            "distance_km",
            "avg_pace",
            "avg_heart_rate",
            "elevation_gain",
        ]

        # Keep only columns that exist in this dataset (prevents KeyError).
        available_columns = []
        for column_name in columns_to_show:
            if column_name in display_df.columns:
                available_columns.append(column_name)
        columns_to_show = available_columns
        n_rows = st.slider("Rows to display", 5, 100, 20)

        st.subheader("Activities")

        # Show key totals right above the table (so they are seen together with the raw data).
        totals_col1, totals_col2 = st.columns(2)
        with totals_col1:
            if total_distance is not None:
                st.metric("Total distance", f"{total_distance:.2f} km")
            else:
                st.metric("Total distance", "—")
        with totals_col2:
            if avg_pace is not None:
                st.metric("Average pace", format_pace_min_to_mmss(avg_pace))
            else:
                st.metric("Average pace", "—")

        # Build the table step-by-step for readability.
        display_table = display_df[columns_to_show].head(n_rows)
        display_table = display_table.rename(
            columns={
                "activity_date": "Activity date",
                "distance_km": "Distance (km)",
                "avg_pace": "Avg pace (min/km)",
                "avg_heart_rate": "Avg HR (bpm)",
                "elevation_gain": "Elevation gain (m)",
            }
        )
        st.dataframe(display_table, hide_index=True)

        pace_df = get_pace_df_with_types(clean_df)
        if not pace_df.empty:
            pace_df_filtered = pace_df[
                (pace_df["distance_km"] > 2)
                & (pace_df["pace_min"] < 9)
                & (pace_df["pace_min"] >= 3.5)
            ]

            if not pace_df_filtered.empty:
                run_summary = pace_df_filtered.groupby("run_type", as_index=False).agg(
                    runs=("run_type", "count"),
                    avg_pace_min=("pace_min", "mean"),
                    total_distance_km=("distance_km", "sum"),
                )

                # Convert avg pace from decimal minutes to "MM:SS" for display.
                # Doing it via total seconds avoids awkward cases like "5:60".
                pace_seconds = (run_summary["avg_pace_min"] * 60).round().astype(int)
                minutes = pace_seconds // 60
                seconds = pace_seconds % 60

                run_summary["avg_pace"] = (
                    minutes.astype(str) + ":" + seconds.astype(str).str.zfill(2)
                )

                st.subheader("Run Type Summary")
                run_summary = run_summary.sort_values("run_type")
                run_summary["type_label"] = run_summary["run_type"].astype(str).map(
                    {
                        "short (<7 km)": "Short: <7 km",
                        "medium (7–13 km)": "Medium: 7-13 km",
                        "long (>13 km)": "Long: >13 km",
                    }
                )
                run_summary_table = run_summary[
                    ["type_label", "runs", "avg_pace", "total_distance_km"]
                ].rename(
                    columns={
                        "type_label": "Type",
                        "runs": "Runs",
                        "avg_pace": "Avg pace (min/km)",
                        "total_distance_km": "Total distance (km)",
                    }
                )
                st.dataframe(run_summary_table, hide_index=True)
# endregion

# region Trends Tab

with tab_trends:
    st.subheader("Trends")

    if clean_df is not None:
        # Trend charts are intentionally simple: they should be easy to interpret at a glance.
        # Put volume first, because it provides context for every other chart.
        if "activity_date" in clean_df.columns and "distance_km" in clean_df.columns:
            st.subheader("Distance Over Time")
            st.caption(
                "Cumulative distance across all runs. The line always goes up — steeper periods mean more training volume."
            )

            # Sum distance per day, then accumulate it so the line always goes up.
            daily_distance = clean_df.groupby("activity_date", as_index=False)[
                "distance_km"
            ].sum()
            daily_distance = daily_distance.sort_values("activity_date")
            daily_distance["distance_km_cumulative"] = daily_distance[
                "distance_km"
            ].cumsum()

            distance_over_time_chart = (
                alt.Chart(daily_distance)
                .mark_line()
                .encode(
                    x=alt.X("activity_date:T", title="Date"),
                    y=alt.Y(
                        "distance_km_cumulative:Q",
                        title="Cumulative distance (km)",
                    ),
                    tooltip=[
                        alt.Tooltip("activity_date:T", title="Date"),
                        alt.Tooltip(
                            "distance_km:Q",
                            title="Distance (km, day)",
                            format=".2f",
                        ),
                        alt.Tooltip(
                            "distance_km_cumulative:Q",
                            title="Cumulative distance (km)",
                            format=".2f",
                        ),
                    ],
                )
                .properties(height=240)
            )
            st.altair_chart(distance_over_time_chart, use_container_width=True)

        pace_df = get_pace_df_with_types(clean_df)
        if not pace_df.empty:
            # For the overall trend line, ignore obvious outliers (very fast paces are usually data glitches).
            pace_df_trends = pace_df[pace_df["pace_min"] >= 3.5].copy()
            if pace_df_trends.empty:
                pace_df_trends = pace_df.copy()

            # Build daily pace trend and smooth it (rolling average) so it's not too noisy.
            daily_pace_df = get_daily_pace_df(pace_df_trends)
            daily_pace_df = daily_pace_df.sort_values("activity_date")

            # Smooth pace to highlight the longer-term direction (instead of day-to-day noise).
            daily_pace_df["pace_smooth"] = (
                daily_pace_df["daily_pace_min"].rolling(window=5, min_periods=1).mean()
            )
            # Human-friendly pace string for tooltips (avoid confusing decimal minutes like 5.87).
            daily_pace_df["pace_smooth_mmss"] = daily_pace_df["pace_smooth"].apply(
                format_pace_min_to_mmss
            )

            if not daily_pace_df.empty:
                st.subheader("Pace Over Time")
                st.caption(
                    "Lower is better (faster pace). Watch the line trend down over time for improvement; spikes up often mean fatigue, heat, hills, or bad conditions."
                )
                pace_over_time_chart = (
                    alt.Chart(daily_pace_df)
                    .mark_line()
                    .encode(
                        x=alt.X("activity_date:T", title="Date"),
                        y=alt.Y(
                            "pace_smooth:Q",
                            title="Pace (min/km)",
                            scale=alt.Scale(
                                domain=[4.0, 8.0],
                                reverse=True,
                                nice=False,
                                clamp=True,
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip("activity_date:T", title="Date"),
                            alt.Tooltip("pace_smooth_mmss:N", title="Pace (min/km)"),
                        ],
                    )
                    .properties(height=260)
                )
                st.altair_chart(pace_over_time_chart, use_container_width=True)

            # Distance vs pace relationship (shown after pace trend for context).
            st.subheader("Correlation check")
            st.caption(
                "Shows how distance relates to pace (min/km): negative means longer runs tend to be faster; positive means longer runs tend to be slower."
            )

            pace_df_for_corr = pace_df.copy()
            pace_df_for_corr = pace_df_for_corr.dropna(
                subset=["distance_km", "pace_min", "run_type"]
            )

            if pace_df_for_corr.empty:
                st.info("Not enough pace + distance data to compute correlations.")
            else:
                # Use the same guardrails as the summary table so obvious outliers don't dominate.
                pace_df_for_corr = pace_df_for_corr[
                    (pace_df_for_corr["distance_km"] > 2)
                    & (pace_df_for_corr["pace_min"] < 9)
                    & (pace_df_for_corr["pace_min"] >= 3.5)
                ].copy()

                def _corr_distance_vs_pace(g: pd.DataFrame) -> float:
                    if len(g) < 2:
                        return float("nan")
                    return float(g["distance_km"].corr(g["pace_min"]))

                corr_by_type = (
                    pace_df_for_corr.groupby("run_type", as_index=False)
                    .apply(lambda g: pd.Series({"Relationship score (r)": _corr_distance_vs_pace(g)}))
                    .reset_index(drop=True)
                )
                corr_by_type = corr_by_type.rename(columns={"run_type": "Run type"})
                corr_by_type = corr_by_type.dropna(subset=["Relationship score (r)"])

                # Keep a stable order + colors so it matches the rest of the app.
                type_order = ["short (<7 km)", "medium (7–13 km)", "long (>13 km)"]
                corr_by_type["Run type"] = pd.Categorical(
                    corr_by_type["Run type"], categories=type_order, ordered=True
                )

                if corr_by_type.empty:
                    st.info(
                        "Not enough data to compute relationship scores by run type."
                    )
                else:
                    corr_bar = (
                        alt.Chart(corr_by_type)
                        .mark_bar(size=55)
                        .encode(
                            x=alt.X(
                                "Run type:N",
                                sort=type_order,
                                title=None,
                                axis=alt.Axis(labels=False, ticks=False),
                            ),
                            y=alt.Y(
                                "Relationship score (r):Q",
                                scale=alt.Scale(domain=[-1, 1], clamp=True),
                                title="Relationship score (r)",
                                axis=alt.Axis(grid=True, tickCount=9),
                            ),
                            color=alt.Color(
                                "Run type:N",
                                scale=alt.Scale(
                                    domain=type_order,
                                    range=["#2563EB", "#10B981", "#F97316"],
                                ),
                                legend=alt.Legend(
                                    title=None,
                                    orient="top",
                                    direction="horizontal",
                                    labelFontSize=12,
                                    symbolType="square",
                                    symbolSize=120,
                                ),
                            ),
                            tooltip=[
                                alt.Tooltip("Run type:N", title="Run type"),
                                alt.Tooltip(
                                    "Relationship score (r):Q",
                                    title="Score (r)",
                                    format=".2f",
                                ),
                            ],
                        )
                        .properties(height=340)
                    )

                    label_layer = (
                        alt.Chart(
                            corr_by_type[corr_by_type["Relationship score (r)"] >= 0]
                        )
                        .mark_text(
                            dy=-10, fontSize=14, fontWeight="bold", color="#111827"
                        )
                        .encode(
                            x=alt.X("Run type:N", sort=type_order, title=None),
                            y=alt.Y("Relationship score (r):Q"),
                            text=alt.Text("Relationship score (r):Q", format=".2f"),
                        )
                    )

                    label_layer_neg = (
                        alt.Chart(
                            corr_by_type[corr_by_type["Relationship score (r)"] < 0]
                        )
                        .mark_text(
                            dy=14, fontSize=14, fontWeight="bold", color="#111827"
                        )
                        .encode(
                            x=alt.X("Run type:N", sort=type_order, title=None),
                            y=alt.Y("Relationship score (r):Q"),
                            text=alt.Text("Relationship score (r):Q", format=".2f"),
                        )
                    )

                    zero_line = (
                        alt.Chart(pd.DataFrame({"y": [0]}))
                        .mark_rule(color="#6B7280", strokeWidth=2)
                        .encode(y="y:Q")
                    )

                    combined_corr_chart = (
                        zero_line + corr_bar + label_layer + label_layer_neg
                    ).properties(padding={"top": 8})
                    st.altair_chart(combined_corr_chart, use_container_width=True)

        st.subheader("Effort Proxy (Pace vs Heart Rate)")
        # Use run-level data (one point per activity).
        effort_runs_df = get_effort_proxy_runs_df(clean_df)
        effort_runs_df = effort_runs_df.dropna(
            subset=["activity_date", "bpm", "pace_min"]
        )

        if effort_runs_df.empty:
            st.info(
                "No valid heart rate data found. Upload an Activities CSV that includes average heart rate (e.g., 'Vid. SR')."
            )
        else:
            st.caption(
                "Lower is better (faster pace). Left is easier (lower heart rate). Ideal trend: down-left over time."
            )

            # Fit axes to actual data so charts don't waste space on a single outlier.
            bpm_lower = float(effort_runs_df["bpm"].min())
            bpm_upper = float(effort_runs_df["bpm"].max())

            # Round to clean 5 bpm boundaries so the grid looks nice.
            bpm_lower = math.floor(bpm_lower / 5.0) * 5.0
            bpm_upper = math.ceil(bpm_upper / 5.0) * 5.0

            # Avoid a zero-width scale if all values are identical.
            if bpm_lower == bpm_upper:
                bpm_lower -= 5.0
                bpm_upper += 5.0

            # Y-axis scaling (pace) uses min/max pace in the filtered run dataset.
            # (We invert the y-axis later: lower pace = better.)
            pace_min_lower = float(effort_runs_df["pace_min"].min())
            pace_min_upper = float(effort_runs_df["pace_min"].max())

            # Avoid a zero-height scale if all paces are identical.
            if pace_min_lower == pace_min_upper:
                pace_min_lower -= 0.1
                pace_min_upper += 0.1

            # Add a MM:SS string column for nicer hover tooltips.
            effort_runs_df = effort_runs_df.copy()
            effort_runs_df["pace_mmss"] = effort_runs_df["pace_min"].apply(
                format_pace_min_to_mmss
            )

            effort_chart = (
                alt.Chart(effort_runs_df)
                .mark_circle(size=70, opacity=0.6)
                .encode(
                    x=alt.X(
                        "bpm:Q",
                        title="Heart rate (bpm)",
                        scale=alt.Scale(
                            domain=[bpm_lower, bpm_upper], nice=False, clamp=True
                        ),
                        axis=alt.Axis(tickMinStep=5, grid=True),
                    ),
                    y=alt.Y(
                        "pace_min:Q",
                        title="Pace (min/km)",
                        scale=alt.Scale(
                            domain=[pace_min_lower, pace_min_upper],
                            reverse=True,
                            nice=False,
                            clamp=True,
                        ),
                        axis=alt.Axis(tickMinStep=0.25, grid=True),
                    ),
                    tooltip=[
                        alt.Tooltip("activity_date:T", title="Date"),
                        alt.Tooltip("bpm:Q", title="BPM", format=".0f"),
                        alt.Tooltip("pace_mmss:N", title="Pace (min/km)"),
                    ],
                )
                .properties(height=380)
            )
            st.altair_chart(effort_chart, use_container_width=True)

        if "elevation_gain" in clean_df.columns:
            st.subheader("Elevation Gain Over Time")
            st.caption(
                "Cumulative elevation gain across all runs. The line always goes up — steeper periods mean more hill volume."
            )

            # Sum elevation gain per day, then make it cumulative so the trend is always increasing.
            daily_elevation = clean_df.groupby("activity_date", as_index=False)[
                "elevation_gain"
            ].sum()
            daily_elevation = daily_elevation.sort_values("activity_date")
            daily_elevation["elevation_gain_cumulative"] = daily_elevation[
                "elevation_gain"
            ].cumsum()

            elevation_over_time_chart = (
                alt.Chart(daily_elevation)
                .mark_line()
                .encode(
                    x=alt.X("activity_date:T", title="Date"),
                    y=alt.Y(
                        "elevation_gain_cumulative:Q",
                        title="Cumulative elevation gain (m)",
                    ),
                    tooltip=[
                        alt.Tooltip("activity_date:T", title="Date"),
                        alt.Tooltip(
                            "elevation_gain:Q",
                            title="Elevation gain (m, day)",
                            format=".0f",
                        ),
                        alt.Tooltip(
                            "elevation_gain_cumulative:Q",
                            title="Cumulative elevation gain (m)",
                            format=".0f",
                        ),
                    ],
                )
                .properties(height=240)
            )
            st.altair_chart(elevation_over_time_chart, use_container_width=True)

# endregion

# region Records Calculations

# "Records" are computed once (from clean_df) and then displayed inside the Insights tab.
fastest_1km_pace_min = None
fastest_1km_date = None

most_efficient_m_per_beat = None
most_efficient_date = None
most_efficient_pace_min = None
most_efficient_bpm = None

if clean_df is not None:
    # Fastest 1 km pace:
    # Prefer Garmin's "best pace" column if present, otherwise fall back to best average pace.
    # (Without lap-level data, this is an approximation.)
    if "best_pace" in clean_df.columns:
        # `best_pace` is a string like "4:56" (min/km). We convert it to minutes as a float.
        best_pace_df = clean_df.dropna(subset=["best_pace"]).copy()
        best_pace_df["best_pace"] = best_pace_df["best_pace"].astype(str)
        best_pace_df = best_pace_df[best_pace_df["best_pace"].str.contains(":")]

        if not best_pace_df.empty:
            parts = best_pace_df["best_pace"].str.split(":")
            best_pace_df["best_pace_min"] = parts.str[0].astype(int) + (
                parts.str[1].astype(int) / 60
            )

            # Guardrail: ignore impossible paces (< 3:00 min/km).
            best_pace_df = best_pace_df[best_pace_df["best_pace_min"] >= 3.0]

            if not best_pace_df.empty:
                # `idxmin()` returns the index of the smallest pace value (fastest).
                best_row = best_pace_df.loc[best_pace_df["best_pace_min"].idxmin()]
                fastest_1km_pace_min = float(best_row["best_pace_min"])
                fastest_1km_date = best_row["activity_date"]

    if fastest_1km_pace_min is None:
        # Fallback: use the best average pace among runs that are at least 1 km.
        pace_df = get_pace_df(clean_df)
        pace_df = pace_df[pace_df["distance_km"] >= 1]
        pace_df = pace_df[pace_df["pace_min"] >= 3.0]

        if not pace_df.empty:
            # Same idea as above: pick the fastest pace value.
            best_row = pace_df.loc[pace_df["pace_min"].idxmin()]
            fastest_1km_pace_min = float(best_row["pace_min"])
            fastest_1km_date = best_row["activity_date"]

    # Most efficient run:
    # Use meters per heartbeat = distance_m / total_beats.
    # total_beats ~= duration_minutes * bpm
    runs_df = get_effort_proxy_runs_df(clean_df)
    if not runs_df.empty:
        # Only keep rows where we can approximate total beats reliably.
        efficiency_df = runs_df.dropna(
            subset=["distance_km", "duration_min", "bpm"]
        ).copy()
        efficiency_df = efficiency_df[
            (efficiency_df["duration_min"] > 0) & (efficiency_df["bpm"] > 0)
        ]

        if not efficiency_df.empty:
            # Efficiency formula:
            # - total beats is approximated from average bpm and duration
            # - meters_per_beat answers: "how many meters did I travel per heartbeat?"
            efficiency_df["total_beats"] = (
                efficiency_df["duration_min"] * efficiency_df["bpm"]
            )
            efficiency_df["meters_per_beat"] = (
                efficiency_df["distance_km"] * 1000
            ) / efficiency_df["total_beats"]

            # Pick the run with the highest meters/beat.
            eff_row = efficiency_df.loc[efficiency_df["meters_per_beat"].idxmax()]
            most_efficient_m_per_beat = float(eff_row["meters_per_beat"])
            most_efficient_date = eff_row["activity_date"]
            most_efficient_pace_min = float(eff_row["pace_min"])
            most_efficient_bpm = float(eff_row["bpm"])

# endregion

# region Insights Tab

with tab_insights:
    if clean_df is not None:
        # Show the 3 headline records first, then the coaching-style insights.
        st.subheader("Records")

        col1, col2, col3 = st.columns(3)

        streaks_df = get_run_streaks(clean_df["activity_date"])

        with col1:
            if fastest_1km_pace_min is not None:
                st.metric(
                    "Fastest pace (1 km proxy)",
                    format_pace_min_to_mmss(fastest_1km_pace_min),
                )
                if fastest_1km_date is not None:
                    st.caption(f"Date: {fastest_1km_date.strftime('%Y-%m-%d')}")
            else:
                st.metric("Fastest pace (1 km proxy)", "—")

        with col2:
            if streaks_df.empty:
                st.metric("Longest streak (days)", "—")
            else:
                best_streak = streaks_df.sort_values(
                    ["days", "end_date"], ascending=[False, False]
                ).iloc[0]

                st.metric("Longest streak (days)", int(best_streak["days"]))
                st.caption(
                    f"Period: {best_streak['start_date'].strftime('%Y-%m-%d')} → {best_streak['end_date'].strftime('%Y-%m-%d')}"
                )

        with col3:
            if most_efficient_m_per_beat is not None:
                st.metric(
                    "Most efficient run (m/beat)", f"{most_efficient_m_per_beat:.2f}"
                )
                details = []
                if most_efficient_pace_min is not None:
                    details.append(
                        f"Pace: {format_pace_min_to_mmss(most_efficient_pace_min)}"
                    )
                if most_efficient_bpm is not None:
                    details.append(f"HR: {most_efficient_bpm:.0f} bpm")
                if details:
                    st.caption(" • ".join(details))
                if most_efficient_date is not None:
                    st.caption(f"Date: {most_efficient_date.strftime('%Y-%m-%d')}")
            else:
                st.metric("Most efficient run (m/beat)", "—")

        st.divider()

        runs_df = get_effort_proxy_runs_df(clean_df)
        if runs_df.empty:
            st.info("Insights need pace + average heart rate data.")
        else:
            runs_df = runs_df.sort_values("activity_date")
            max_date = runs_df["activity_date"].max()

            # Build thresholds from your own data (quantiles).
            # This makes the auto-labeling adapt to your fitness level and dataset.
            label_pool = runs_df.copy()
            bpm_q60 = float(label_pool["bpm"].quantile(0.60))
            bpm_q85 = float(label_pool["bpm"].quantile(0.85))
            bpm_q92 = float(label_pool["bpm"].quantile(0.92))
            pace_q25 = float(label_pool["pace_min"].quantile(0.25))
            pace_q35 = float(label_pool["pace_min"].quantile(0.35))
            pace_q60 = float(label_pool["pace_min"].quantile(0.60))

            def label_run(row):
                # We keep both average and max HR:
                # - average HR is stable for easy runs
                # - max HR catches hard intervals where average can look misleading
                bpm = float(row["bpm"])

                max_bpm = bpm
                if not pd.isna(row["max_bpm"]):
                    max_bpm = float(row["max_bpm"])

                pace = float(row["pace_min"])
                dur = row["duration_min"]
                dist = float(row["distance_km"])

                # If duration is missing, approximate it from distance * pace.
                if pd.isna(dur):
                    dur = dist * pace

                # Use max_bpm for HR checks to catch interval spikes.
                if max_bpm >= bpm_q92 and pace <= pace_q25 and dur >= 25:
                    return "race"
                if max_bpm >= bpm_q85 and pace <= pace_q35 and dur >= 20:
                    return "tempo"
                if max_bpm >= bpm_q60 and pace <= pace_q60 and dur >= 25:
                    return "steady"
                return "easy"

            # Apply labeling to every run, then slice out just the last 7 days for the summary.
            label_pool["session_type"] = label_pool.apply(label_run, axis=1)

            last7 = label_pool[
                label_pool["activity_date"] >= max_date - pd.Timedelta(days=7)
            ]

            st.subheader("Last 7 days")

            if last7.empty:
                st.write(
                    "No runs logged in the last 7 days — let’s get a small streak going."
                )
            else:
                total_runs = int(len(last7))
                total_km = float(last7["distance_km"].sum())
                longest_km = float(last7["distance_km"].max())

                by_type = (
                    last7.groupby("session_type")["distance_km"]
                    .agg(["count", "sum"])
                    .rename(columns={"count": "runs", "sum": "km"})
                )

                # Session type counts (one number per label).
                easy_runs = 0
                steady_runs = 0
                tempo_runs = 0
                race_runs = 0

                if not by_type.empty:
                    easy_runs = int(by_type["runs"].get("easy", 0))
                    steady_runs = int(by_type["runs"].get("steady", 0))
                    tempo_runs = int(by_type["runs"].get("tempo", 0))
                    race_runs = int(by_type["runs"].get("race", 0))

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Runs", total_runs)
                with col2:
                    st.metric("Distance", f"{total_km:.1f} km")
                with col3:
                    st.metric("Longest run", f"{longest_km:.1f} km")

                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Easy", easy_runs)
                with m2:
                    st.metric("Steady", steady_runs)
                with m3:
                    st.metric("Tempo", tempo_runs)
                with m4:
                    st.metric("Race", race_runs)

                # Quick check: if a large share of your weekly km is "hard", recovery becomes the limiter.
                hard_km = float(
                    last7[last7["session_type"].isin(["tempo", "race"])][
                        "distance_km"
                    ].sum()
                )
                hard_ratio = 0.0
                if total_km > 0:
                    hard_ratio = hard_km / total_km

                if total_runs >= 3 and hard_ratio > 0.30:
                    st.info(
                        "A big share of your km was tempo/race. That can feel productive short-term, but fatigue accumulates fast — pay extra attention to sleep, soreness, and easy-day effort."
                    )
                elif total_runs >= 3 and (tempo_runs + race_runs) == 0:
                    st.info(
                        "Mostly easy/steady — great base work. If you want more speed, one controlled quality session is the next lever to pull."
                    )
                else:
                    st.info(
                        "Nice balance — this is the kind of week that stacks into progress."
                    )

            latest = runs_df.iloc[-1]
            latest_date = latest["activity_date"]
            latest_bpm = float(latest["bpm"])
            latest_pace = float(latest["pace_min"])

            # --- Acute stress check ---
            st.divider()
            # Compare your latest run to your historical HR at a similar pace.
            # If HR is unusually high for the same pace, it often signals fatigue/heat/sleep issues.
            pace_window = 0.2
            baseline_pool = runs_df[runs_df["activity_date"] < latest_date].copy()
            baseline_similar = baseline_pool[
                (baseline_pool["pace_min"] >= latest_pace - pace_window)
                & (baseline_pool["pace_min"] <= latest_pace + pace_window)
            ]

            if len(baseline_similar) < 4:
                pace_window = 0.3
                baseline_similar = baseline_pool[
                    (baseline_pool["pace_min"] >= latest_pace - pace_window)
                    & (baseline_pool["pace_min"] <= latest_pace + pace_window)
                ]

            baseline_bpm = None
            if len(baseline_similar) >= 3:
                # Median is robust: a few weird days won't distort it as much as a mean.
                baseline_bpm = float(baseline_similar["bpm"].median())
            else:
                # Fallback baseline: use your slower/easier runs if not enough similar-pace history exists.
                easy_cut = float(runs_df["pace_min"].quantile(0.6))
                fallback = baseline_pool[baseline_pool["pace_min"] >= easy_cut]
                if not fallback.empty:
                    baseline_bpm = float(fallback["bpm"].median())

            st.markdown("**Acute stress check**")
            heat_level = "unknown"
            if baseline_bpm is None:
                st.write(
                    f"Most recent run: {format_pace_min_to_mmss(latest_pace)} min/km @ {latest_bpm:.0f} bpm. With a bit more history, I can flag when HR is unusually high for the same workload."
                )
            else:
                delta_bpm = latest_bpm - baseline_bpm

                if delta_bpm >= 10:
                    heat_level = "red"
                    st.error(
                        f"HR is ~+{delta_bpm:.0f} bpm higher than your normal for this workload. Common causes: heat, dehydration, poor sleep, or accumulated fatigue."
                    )
                elif delta_bpm >= 6:
                    heat_level = "yellow"
                    st.warning(
                        f"HR is ~+{delta_bpm:.0f} bpm higher than usual for this workload. Conditions (heat/hills) or fatigue may be pushing stress up."
                    )
                else:
                    heat_level = "green"
                    st.success(
                        "Heart rate response looks normal for this workload."
                    )

            # --- Recovery readiness ---
            st.divider()
            st.markdown("**Recovery readiness**")
            readiness_level = "unknown"
            if last7.empty:
                st.write("Need at least a few runs in the last 7 days to judge readiness.")
            else:
                # Recovery signals (independent from the acute stress check above):
                # - volume spike vs previous 7 days
                # - a high share of "hard" km (tempo/race)
                # - total volume vs your recent 4-week average
                last7_km = float(last7["distance_km"].sum())
                prev7_km = float(
                    runs_df[
                        (runs_df["activity_date"] < max_date - pd.Timedelta(days=7))
                        & (runs_df["activity_date"] >= max_date - pd.Timedelta(days=14))
                    ]["distance_km"].sum()
                )

                volume_spike = prev7_km > 0 and last7_km > prev7_km * 1.3

                hard_km = float(
                    last7[last7["session_type"].isin(["tempo", "race"])][
                        "distance_km"
                    ].sum()
                )
                hard_ratio = 0.0
                if last7_km > 0:
                    hard_ratio = hard_km / last7_km

                weekly = (
                    runs_df.groupby(pd.Grouper(key="activity_date", freq="W-MON"))
                    .agg(weekly_km=("distance_km", "sum"))
                    .reset_index()
                    .rename(columns={"activity_date": "week_start"})
                    .sort_values("week_start")
                )
                last4_mean_km = float("nan")
                if len(weekly) >= 1:
                    last4_mean_km = float(weekly.tail(4)["weekly_km"].mean())
                vs_last4 = (
                    not math.isnan(last4_mean_km)
                    and last4_mean_km > 0
                    and last7_km > last4_mean_km * 1.25
                )

                if (volume_spike and hard_ratio > 0.25) or (vs_last4 and hard_ratio > 0.30):
                    readiness_level = "red"
                    st.error(
                        "Recovery risk is high: recent load and intensity are both elevated. Make the next few days easy (or take a rest day)."
                    )
                elif volume_spike or hard_ratio > 0.30 or vs_last4:
                    readiness_level = "yellow"
                    st.warning(
                        "Recovery may be limited: your recent load is higher than usual. A lighter/easy day will likely pay off more than adding intensity."
                    )
                else:
                    readiness_level = "green"
                    st.success(
                        "Recovery looks solid — good conditions for progress."
                    )
            st.divider()

            # --- Combined training recommendation (needs both detectors) ---
            # Pick the "worst" of the two signals (red overrides yellow, yellow overrides green).
            combined_level = "unknown"
            if heat_level == "red" or readiness_level == "red":
                combined_level = "red"
            elif heat_level == "yellow" or readiness_level == "yellow":
                combined_level = "yellow"
            elif heat_level == "green" and readiness_level == "green":
                combined_level = "green"

            if combined_level == "green":
                coach_action_box(
                    "Daily recommendation",
                    "Do your planned session — you’re good to go.",
                    tone="success",
                )
            elif combined_level == "yellow":
                coach_action_box(
                    "Daily recommendation",
                    "Dial it back. Keep it easy (no intensity) and cut the run by ~20–30%.",
                    tone="warning",
                )
            elif combined_level == "red":
                coach_action_box(
                    "Daily recommendation",
                    "Stop the grind. Rest, or do a very easy short run only. Skip intensity.",
                    tone="error",
                )
            else:
                coach_action_box(
                    "Daily recommendation",
                    "Not enough baseline yet. Keep runs easy and consistent for 1–2 weeks — then this gets sharp.",
                    tone="info",
                )

            # Weekly totals are used only for gentle trend guidance (not a strict plan).
            weekly = (
                runs_df.groupby(pd.Grouper(key="activity_date", freq="W-MON"))
                .agg(weekly_km=("distance_km", "sum"))
                .reset_index()
                .rename(columns={"activity_date": "week_start"})
                .sort_values("week_start")
            )
            # Average weekly distance across the last 4 weeks (used for gentle guidance).
            last4 = float("nan")
            if len(weekly) >= 1:
                last4 = float(weekly.tail(4)["weekly_km"].mean())

            # --- Next-week focus (from last 7 days mix) ---
            if not last7.empty:
                total_km = float(last7["distance_km"].sum())
                longest_km = float(last7["distance_km"].max())

                # "Hard" is tempo/race; if this is too high, you usually improve by absorbing, not adding.
                hard_km = float(
                    last7[last7["session_type"].isin(["tempo", "race"])][
                        "distance_km"
                    ].sum()
                )
                hard_ratio = 0.0
                if total_km > 0:
                    hard_ratio = hard_km / total_km
                tempo_runs = int((last7["session_type"] == "tempo").sum())
                race_runs = int((last7["session_type"] == "race").sum())

                prev7_km = float(
                    runs_df[
                        (runs_df["activity_date"] < max_date - pd.Timedelta(days=7))
                        & (runs_df["activity_date"] >= max_date - pd.Timedelta(days=14))
                    ]["distance_km"].sum()
                )
                volume_spike = prev7_km > 0 and total_km > prev7_km * 1.3

                allow_intensity = True
                next7_reco_emitted = False

                if volume_spike:
                    # Volume spikes are the most reliable "don't be a hero" warning.
                    st.warning(
                        "Big volume jump versus the previous week. Injury risk goes up fast here."
                    )
                    if readiness_level == "green":
                        coach_action_box(
                            "Weekly recommendation",
                            "Hold weekly distance flat (no increase). You can keep 1 controlled quality session (tempo or steady intervals), but keep everything else easy.",
                            tone="warning",
                        )
                    else:
                        allow_intensity = False
                        coach_action_box(
                            "Weekly recommendation",
                            "Hold weekly distance flat (or drop ~10%) and skip intensity. Make every run easy and relaxed.",
                            tone="warning",
                        )
                    next7_reco_emitted = True
                elif readiness_level == "red":
                    allow_intensity = False
                    next7_reco_emitted = True
                    coach_action_box(
                        "Weekly recommendation",
                        "Make it a recovery week: easy runs only, prioritize sleep and hydration, skip intensity.",
                        tone="error",
                    )
                elif readiness_level == "yellow":
                    allow_intensity = False
                    next7_reco_emitted = True
                    coach_action_box(
                        "Weekly recommendation",
                        "Keep intensity out. Easy runs only; add one steady run only if you feel noticeably better mid-week.",
                        tone="warning",
                    )

                if allow_intensity and not next7_reco_emitted:
                    if hard_ratio > 0.30 and len(last7) >= 3:
                        coach_action_box(
                            "Weekly recommendation",
                            "Last week had a lot of hard running. Cap it at 1 quality session and keep the rest easy.",
                            tone="warning",
                        )
                    elif (tempo_runs + race_runs) == 0 and len(last7) >= 3:
                        coach_action_box(
                            "Weekly recommendation",
                            "Add one controlled quality session (tempo). Keep everything else easy/steady and let the quality pop.",
                            tone="info",
                        )
                    else:
                        next7_tone = "info"
                        if readiness_level == "green":
                            next7_tone = "success"

                        coach_action_box(
                            "Weekly recommendation",
                            "Repeat a similar week. If you feel fresh, nudge distance +5–10% — but don’t increase both distance and intensity.",
                            tone=next7_tone,
                        )
# endregion
