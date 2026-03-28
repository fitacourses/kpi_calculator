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
        print(f"{runner}: You haven't ran enough sessions - {count}! Six is minimum. LACE UP!")
    elif count > 11:
        print(f"{runner}: You've ran too many sessions - {count}! Eleven is maximum. You've overworked! Try removing excess sessions.")
# endregion

# region 3. Calculations
# TODO-DONE: group by runner and calculate total distance, average pace, average heart rate, total elevation
# hint: df.groupby("runner")["kolonna"].sum() / .mean()
stats  = (df.groupby("runner")[["distance", "time", "elevation", "bpm"]].agg({"distance": "sum", "elevation": "sum", "bpm": "mean"}))
# endregion

# region 4. Average pace
# TODO-DONE: split "time" column by ":" to get minutes and seconds
parts = df["time"].str.split(":") # split each rows "time" and give list of 2 strings: ["142", "51"]
# get elements from parts and convert to ints, divide by 60 to get pace in decimal minutes, save in new column "pace"
df["pace"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)
# add average pace per runner to stats table
total_time = df.groupby("runner")["pace"].sum() # df already has "pace" calculated
total_dist = df.groupby("runner")["distance"].sum()
stats["avg_pace"] = total_time / total_dist
# endregion
print(stats)

# region 5. Performance score
# TODO-DONE: calculate efficiency score per session
# efficiency score per session:
# distance * 0.35 — more km raises score
# 1/pace * 10 * 0.7 — faster pace raises score, 1/pace flips it, *10 scales decimal up
# elevation/50 * 0.6 — more climbing raises score
# bpm/1000 * 0.3 — high heart rate lowers score (penalizes strain)
df["perf_score"] = (df["distance"] * 0.35) + (1/df["pace"] * 10 * 0.7) + (df["elevation"]/50 * 0.6) - (df["bpm"]/1000 * 0.3)
# endregion

# region 6. Consistency
# TODO: calculate standard deviation of daily distance per runner
# hint: df.groupby("runner")["distance"].std()
# store in stats["consistency"]
# lower std = more consistent runner
# endregion

# region 7. Best day
# TODO: find the day with highest perf_score per runner
# hint: df.groupby("runner")["perf_score"].idxmax() gives row index of best session
# use that index to get the day: df.loc[...]["day"]
# endregion

# region 8. Leaderboard
# TODO: ask user to input a day number (1-7) or 0 for full weekly leaderboard
# hint: day = int(input("Enter day (0 for weekly leaderboard): "))
# if day == 0 — print full stats sorted by winner_score
# else — filter df by day and print sorted by perf_score
# endregion

# region 9. Winner score
# TODO: combine avg perf_score and consistency into final ranking
# hint: stats["avg_perf"] = df.groupby("runner")["perf_score"].mean()
# hint: winner_score = avg_perf * 0.7 + (1/consistency) * 0.3
# print winner — runner with highest winner_score
# endregion

# region 10. Export
# TODO: save stats table to results.xlsx
# hint: stats.to_excel("results.xlsx")
# endregion