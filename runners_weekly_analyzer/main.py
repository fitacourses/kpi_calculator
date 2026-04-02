# region 1. Load data
import pandas as pd
df = pd.read_csv("data.csv") # pandas "short for pd" reads data and stores table as "df" - dataFrame
# endregion

# region 2. TODO-DONE: Session count check
# count each runner's sessions and store a warning (or empty string) in a dictionary 
sessions_per_runner = df.groupby("runner")["day"].count()
warnings = {}
for runner, count in sessions_per_runner.items():
    if count < 6:
        warnings[runner] = f"Too few sessions ({count})"
    elif count > 11:
        warnings[runner] = f"Too many sessions ({count})"
    else:
        warnings[runner] = ""
# endregion

# region 3. TODO-DONE: Stats calculations
# group by runner and calculate the stats
stats = df.groupby("runner")[["distance", "elevation", "bpm"]].agg({"distance": "sum", "elevation": "sum", "bpm": "mean"})
# endregion

# region 3.1. TODO-DONE: Warnings
# add warning column, fill each runner's cell with warning string from the dictionary
stats["warning"] = ""
for runner in stats.index:
    stats.loc[runner, "warning"] = warnings[runner]
# endregion

# region 4. TODO-DONE: Average pace  
# split time column entries on ":" to get minutes and seconds seperately
parts = df["time"].str.split(":") 
# convert session duration to decimal minutes
df["pace"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)
# sum up total time and distance per runner, then divide to get average pace (min/km)
total_time = df.groupby("runner")["pace"].sum()
total_dist = df.groupby("runner")["distance"].sum()
stats["avg_pace"] = total_time / total_dist
# endregion

# region 4.1. TODO-DONE: Average pace conversion
# convert column dtype so any objects including strings are allowed
stats["avg_pace"] = stats["avg_pace"].astype("object")

for runner in stats.index: 
    # get decimal pace for iterated runner
    decimal_pace = stats.loc[runner, "avg_pace"]
    # strips everything after the decimal point
    minutes = int(decimal_pace)        
    # subtract the whole number (before .) from decimal pace, times 60 to convert to seconds       
    seconds = round((decimal_pace - minutes) * 60)
    # combine into MM:SS string, :02d ensures 2 digits
    stats.loc[runner, "avg_pace"] = f"{minutes}:{seconds:02d}" 
# endregion

# region 5. TODO-DONE: Performance score
# calculate performance score in new column for each session
df["perf_score"] = (df["distance"] * 0.35) + (1/df["pace"] * 10 * 0.7) + (df["elevation"]/50 * 0.6) - (df["bpm"]/1000 * 0.3)
# distance * 0.35 — more km raises score
# 1/pace * 10 * 0.7 — faster pace raises score, 1/pace flips it, *10 scales decimal up
# elevation/50 * 0.6 — more climbing raises score
# bpm/1000 * 0.3 — high heart rate lowers score (penalizes strain)
# endregion

# region 5.1. TODO-DONE: Average performance score
# calculate average performance for each runner troughout the week
stats["avg_perf_score"] = df.groupby("runner")["perf_score"].mean()
# endregion

# region 6. TODO-DONE: Consistency
# calculate deviation of runner's performance score troughout the week
stats["consistency"] = df.groupby("runner")["perf_score"].std()
# lower - more consistent performance
# endregion

# region 7. TODO-DONE: Power ranking
# combine average performance score and consistency into power ranking score
stats["power_ranking"] = (stats["avg_perf_score"] * 0.7) + (1/stats["consistency"] * 0.3)
# endregion

# region 8. TODO-DONE: Leaderboard
# create weekly leaderboards by highest to lowest power ranking score
weekly_leaderboard = stats[["avg_perf_score", "consistency", "power_ranking"]].sort_values("power_ranking", ascending=False)

# create daily leaderboard by highest to lowest performance score
daily_leaderboards = {}
# loop through each day name once
for day in df["day"].unique(): 
    # filter rows to only this iterated day
    day_df = df[df["day"] == day] 
    # group by runner, get average performance score for a day
    daily_leaderboards[day] = day_df.groupby("runner")["perf_score"].mean().sort_values(ascending=False) 
# endregion

# region 9. TODO-DONE: Rounding numbers
# round all numbers in stats to 2 decimal places, bpm to 1
stats = stats.round(2)
stats["bpm"] = stats["bpm"].round(1)

# round weekly leaderboard to 2 decimal places
weekly_leaderboard = weekly_leaderboard.round(2)

# round each daily leaderboard to 2 decimal places
for day in daily_leaderboards:
    daily_leaderboards[day] = daily_leaderboards[day].round(2)
# endregion

# region 10. TODO-DONE: Export
# open results.xlsx for writing — each table gets its own sheet
with pd.ExcelWriter("results.xlsx") as writer:
    stats.to_excel(writer, sheet_name="Weekly Stats")
    weekly_leaderboard.to_excel(writer, sheet_name="Weekly Leaderboard")
    # loop through each day and write its leaderboard to a separate sheet
    for day, table in daily_leaderboards.items():
        table.to_excel(writer, sheet_name=str(day))
# endregion
