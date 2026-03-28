# to import pd as short for pandas for this main
import pandas as pd
# pandas reads data.csv and stores it as a table in df (dataFrame - datu tabula)
df = pd.read_csv("data.csv")

# TODO-DONE: group by runner and calculate total distance, average pace, average heart rate, total elevation
# hint: df.groupby("runner")["kolonna"].sum() / .mean()
kpi = (df.groupby("runner")[["distance", "time", "elevation", "bpm"]].agg({"distance": "sum", "elevation": "sum", "bpm": "mean"}))
kpi["bpm"] = kpi["bpm"].round(1) # round bpm to decimal
print(kpi)

# TODO-DONE: convert time column from MM:SS to decimal minutes (pace)
# split "time" column by ":" to get minutes and seconds
parts = df["time"].str.split(":") # split each rows "time" and give list of 2 strings: ["142", "51"]
# get elements from parts and convert to ints, divide by 60 to get pace in decimal minutes, save in new column "pace"
df["pace"] = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)

# TODO-DONE: calculate efficiency score per session
# efficiency score per session:
# distance * 0.35 — more km raises score
# 1/pace * 10 * 0.7 — faster pace raises score, 1/pace flips it, *10 scales decimal up
# elevation/100 * 0.6 — more climbing raises score
# bpm/1000 * 0.3 — high heart rate lowers score (penalizes strain)
df["efficiency"] = (df["distance"] * 0.35) + (1/df["pace"] * 10 * 0.7) + (df["elevation"]/100 * 0.6) - (df["bpm"]/1000 * 0.3)