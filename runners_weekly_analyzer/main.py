# region 1. Load data
import pandas as pd
df = pd.read_csv("data.csv") # read the CSV file into a pandas DataFrame
# endregion

# region 2. Stats calculations
# group rows by runner and calculate the stats
grouped = df.groupby("runner")

stats = grouped[["distance", "elevation", "bpm"]].agg({
    "distance": "sum",
    "elevation": "sum",
    "bpm": "mean"
})

# split time column into minutes and seconds separately
parts = df["time"].str.split(":")

# convert the MM:SS time values into decimal minutes
df["minutes_total"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)

# pace per session
df["pace"] = df["minutes_total"] / df["distance"]

# calculate each runner's average pace
total_time = df.groupby("runner")["minutes_total"].sum()
total_dist = df.groupby("runner")["distance"].sum()
avg_pace = total_time / total_dist
stats["avg_pace"] = avg_pace

# average pace conversion - allow the avg_pace column to store strings like MM:SS
stats["avg_pace"] = stats["avg_pace"].astype("object")

for runner in stats.index:
    # get this runner's average pace as a decimal number
    decimal_pace = stats.loc[runner, "avg_pace"]

    # take the whole-number part as minutes
    minutes = int(decimal_pace)

    # convert the decimal part into seconds
    seconds = round((decimal_pace - minutes) * 60)

    # format the result as MM:SS
    stats.loc[runner, "avg_pace"] = f"{minutes}:{seconds:02d}"
# endregion

# region 3. Performance scoring
DIST_MIN = 0
DIST_MAX = 30

PACE_SLOW = 8.0
PACE_FAST = 3.5

ELEV_MIN = 50
ELEV_MAX = 500

BPM_LOW = 130
BPM_HIGH = 160

BPM_MULT_MIN = 1.00
BPM_MULT_MAX = 1.20

# normalize all values to a 0-1 score based on defined min/max ranges

# longer distances gets higher scores
df["distance_score"] = (
    (df["distance"] - DIST_MIN) / (DIST_MAX - DIST_MIN)
).clip(0, 1)

# lower pace gets higher scores
df["pace_score"] = (
    (PACE_SLOW - df["pace"]) / (PACE_SLOW - PACE_FAST)
).clip(0, 1)

# higher elevation gets higher scores
df["elevation_score"] = (
    (df["elevation"] - ELEV_MIN) / (ELEV_MAX - ELEV_MIN)
).clip(0, 1)

# lower bpm gets higher scores
df["bpm_score"] = (
    (BPM_HIGH - df["bpm"]) / (BPM_HIGH - BPM_LOW)
).clip(0, 1)

# convert normalized bpm scores (0-1) into multiplier (1.00-1.15)
# higher bpm score gives larger multiplier bonus
df["bpm_multiplier"] = (
    BPM_MULT_MIN + df["bpm_score"] * (BPM_MULT_MAX - BPM_MULT_MIN)
)
# combine main score components into one base score
df["base_score"] = (
    df["distance_score"] +
    df["pace_score"] +
    df["elevation_score"]
)

# apply bpm multiplier to get final performance score
df["perf_score"] = df["base_score"] * df["bpm_multiplier"]

# calculate how much extra score bpm added
df["bpm_bonus"] = df["perf_score"] - df["base_score"]

# average component scores for each runner
stats["avg_perf_score"] = df.groupby("runner")["perf_score"].mean()
stats["avg_distance_score"] = df.groupby("runner")["distance_score"].mean()
stats["avg_pace_score"] = df.groupby("runner")["pace_score"].mean()
stats["avg_elevation_score"] = df.groupby("runner")["elevation_score"].mean()
stats["avg_bpm_bonus"] = df.groupby("runner")["bpm_bonus"].mean()
# endregion

# region 4. Leaderboard
# sort runners by average performance score
weekly_leaderboard = stats[[
    "avg_perf_score",
    "avg_distance_score",
    "avg_pace_score",
    "avg_elevation_score",
    "avg_bpm_bonus"
]].sort_values("avg_perf_score", ascending=False)

# create a separate leaderboard for each day
daily_leaderboards = {}
# loop through each day name once
for day in df["day"].unique(): 
    # filter rows to only this iterated day
    day_df = df[df["day"] == day] 
    # calculate average performance score for each runner on this day
    daily_scores = day_df.groupby("runner")["perf_score"].mean()
    # sort runners from highest to lowest score
    daily_leaderboard = daily_scores.sort_values(ascending=False)
        # store this day's leaderboard in the dictionary
    daily_leaderboards[day] = daily_leaderboard
# endregion

# region 5. Output
# round numeric values in stats table
stats = stats.round(2)

# round bpm separately to 1 decimal place
stats["bpm"] = stats["bpm"].round(1)

# round weekly leaderboard values
weekly_leaderboard = weekly_leaderboard.round(2)

# round each daily leaderboard
for day in daily_leaderboards:
    daily_leaderboards[day] = daily_leaderboards[day].round(2)

# write all tables to results.xlsx, each on its own sheet
with pd.ExcelWriter("results.xlsx") as writer:
    stats.to_excel(writer, sheet_name="Weekly Stats")
    weekly_leaderboard.to_excel(writer, sheet_name="Weekly Leaderboard")

    # write each daily leaderboard to its own sheet
    for day, table in daily_leaderboards.items():
        table.to_excel(writer, sheet_name=str(day))
# endregion
