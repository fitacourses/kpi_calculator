# region 1. Load data
import pandas as pd
pd.set_option("display.max_columns", None) 
# pandas as pd reads data and stores it in "df" - dataFrame
df = pd.read_csv("data.csv")
# endregion

# region 2. Validation
# TODO: validate session count per runner (min 6, max 11)
sessions_per_runner = df.groupby("runner")["day"].count()
for runner, count in sessions_per_runner.items():
    if count < 6:
        print(f"{runner}: You haven't ran enough sessions - {count}! Six is minimum for the week. LACE UP!")
    elif count > 11:
        print(f"{runner}: You've ran too many sessions - {count}! Eleven is maximum for the week. Try removing excess sessions.")
# endregion

# region 3. Calculations
# TODO-DONE: group by runner and calculate total distance, average pace, average heart rate, total elevation
stats  = (df.groupby("runner")[["distance", "elevation", "bpm"]].agg({"distance": "sum", "elevation": "sum", "bpm": "mean"}))
# endregion

# region 4. Average pace
# TODO-DONE: 
parts = df["time"].str.split(":") # split time on ":" to get minutes and seconds
# get elements from parts and convert to ints, divide by 60 to get pace in decimal minutes, store in new column "pace"
df["pace"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)
# add average pace per runner to stats table
total_time = df.groupby("runner")["pace"].sum()
total_dist = df.groupby("runner")["distance"].sum()
stats["avg_pace"] = total_time / total_dist
# endregion

# region 5. Performance score
# TODO-DONE: calculate performance score for each session
# distance * 0.35 — more km raises score
# 1/pace * 10 * 0.7 — faster pace raises score, 1/pace flips it, *10 scales decimal up
# elevation/50 * 0.6 — more climbing raises score
# bpm/1000 * 0.3 — high heart rate lowers score (penalizes strain)
df["perf_score"] = (df["distance"] * 0.35) + (1/df["pace"] * 10 * 0.7) + (df["elevation"]/50 * 0.6) - (df["bpm"]/1000 * 0.3)

# TODO-DONE: calculate average performance for each runner and store in stats
stats["avg_perf_score"] = df.groupby("runner")["perf_score"].mean()
# endregion

# region 6. Best day
# TODO: find the day with highest performance for each runner and store in stats
daily_perf = df.groupby(["runner", "day"])["perf_score"].mean() # get average performance per day
best_day = daily_perf.groupby("runner").idxmax().str[1] # find day with highest average performance, extract day number
stats["best_day"] = best_day
# endregion

# region 7. Consistency
# TODO-DONE: # calculate deviation of runner performance troughout the week(lower = more consistent performance)
stats["consistency"] = df.groupby("runner")["perf_score"].std()
# endregion

# region 8. Winner score
# TODO-DONE: combine average performance and consistency into final ranking
stats["power_ranking"] = (stats["avg_perf_score"] * 0.7) + (1/stats["consistency"] * 0.3)
# endregion

# region 9. Leaderboard
# TODO-DONE: ask user to input for example "Friday" for daily leaderboard or "full" for full weekly leaderboard
day = input("Enter day (e.g. 'Friday') or 'Full' for weekly leaderboard: ")
if day == "full":
    leaderboard = stats[["avg_perf_score", "consistency", "power_ranking"]].sort_values("power_ranking", ascending=False)
    print(leaderboard)
else:
    day_df = df[df["day"] == day] # filter df to only rows where day matches user input
    leaderboard = day_df.groupby("runner")["perf_score"].mean().sort_values(ascending=False) # sort best first
    print(leaderboard)
# endregion

# region 10. Export
# TODO: save stats table to results.xlsx
# hint: stats.to_excel("results.xlsx")
# endregion