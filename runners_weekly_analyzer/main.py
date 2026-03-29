# region 1. Load data
# to import pd as short for pandas for this main
import pandas as pd
# pandas reads data.csv and stores it as a table in df (dataFrame - datu tabula)
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
# TODO-DONE: split "time" column by ":" to get minutes and seconds
parts = df["time"].str.split(":") # split each rows "time" and give list of elements
# get elements from parts and convert to ints, divide by 60 to get pace in decimal minutes, store in new column "pace"
df["pace"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)
# add average pace per runner to stats table
total_time = df.groupby("runner")["pace"].sum()
total_dist = df.groupby("runner")["distance"].sum()
stats["avg_pace"] = total_time / total_dist
# endregion

# region 5. Performance score
# TODO-DONE: calculate efficiency score per session
# distance * 0.35 — more km raises score
# 1/pace * 10 * 0.7 — faster pace raises score, 1/pace flips it, *10 scales decimal up
# elevation/50 * 0.6 — more climbing raises score
# bpm/1000 * 0.3 — high heart rate lowers score (penalizes strain)
df["perf_score"] = (df["distance"] * 0.35) + (1/df["pace"] * 10 * 0.7) + (df["elevation"]/50 * 0.6) - (df["bpm"]/1000 * 0.3)

# TODO-DONE: calculate average perf_score per runner and store in stats
stats["avg_perf_score"] = df.groupby("runner")["perf_score"].mean()
# endregion

# region 6. Best day
# TODO: find the day with highest perf_score per runner
daily_perf = df.groupby(["runner", "day"])["perf_score"].mean() # group by runner and day, average performance per day
day_names = {1: "Pirmdiena", 2: "Otrdiena", 3: "Trešdiena", 4: "Ceturtdiena", 5: "Piektdiena", 6: "Sestdiena", 7: "Svētdiena"}
best_day = daily_perf.groupby("runner").idxmax().str[1] # find day with highest average performance for runners, extract day number
best_day = best_day.map(day_names)
stats["best_day"] = best_day
# endregion

# region 7. Consistency
# TODO: calculate standard deviation of daily distance per runner
# endregion

# region 8. Leaderboard
# TODO: ask user to input a day number (1-7) or 0 for full weekly leaderboard
# if day == 0 — print full stats sorted by winner_score
# else — filter df by day and print sorted by perf_score
# endregion

# region 9. Winner score
# TODO: combine avg perf_score and consistency into final ranking
# print winner — runner with highest winner_score
# endregion

# region 10. Export
# TODO: save stats table to results.xlsx
# hint: stats.to_excel("results.xlsx")
# endregion