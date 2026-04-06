# region 1. Import libraries and load data
import pandas as pd
import matplotlib.pyplot as plt
# read the CSV file into a pandas 
df = pd.read_csv("data.csv") 
# endregion

# region 2. Pace calculations
# split the time column into minutes and seconds separately
parts = df["time"].str.split(":")

# convert the MM:SS time values into decimal minutes
minutes_total = parts.str[0].astype(int) + (parts.str[1].astype(int) / 60)
df["pace"] = (minutes_total/ df["distance"]).round(2)
# debug - print(df[["time", "distance", "pace"]].head())
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
# longer distances get higher scores
df["distance_score"] = (
    (df["distance"] - DIST_MIN) / (DIST_MAX - DIST_MIN)
).clip(0, 1)

# lower pace get higher scores
df["pace_score"] = (
    (PACE_SLOW - df["pace"]) / (PACE_SLOW - PACE_FAST)
).clip(0, 1)

# higher elevation get higher scores
df["elevation_score"] = (
    (df["elevation"] - ELEV_MIN) / (ELEV_MAX - ELEV_MIN)
).clip(0, 1)

# lower bpm get higher scores
df["bpm_score"] = (
    (BPM_HIGH - df["bpm"]) / (BPM_HIGH - BPM_LOW)
).clip(0, 1)

# convert normalized bpm scores (0-1) into multiplier
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

# group by runner and calculate average for each score
grouped = df.groupby("runner")
avg_perf_score = grouped[["distance_score", "pace_score", "elevation_score", "bpm_bonus"]].mean()
avg_perf_score = avg_perf_score.round(2)
# endregion

# region 4. Build stacked bar chart
# create figure and axes and save into fig and ax
fig, ax = plt.subplots()

# plot one stacked bar of average performance score per runner
avg_perf_score.plot(
    kind="bar", 
    stacked=True,
    # store the plot in ax, to customize later
    ax=ax)

# add labels inside stacked bars
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f", label_type="center", fontsize=7)

# set title and axis name
ax.set_title("Runner Performance Comparison")
ax.set_xlabel("Runner")
ax.set_ylabel("Average Performance Score")

# rename and reposition legend
ax.legend(
    ["Distance", "Pace", "Elevation", "BPM Bonus"],
    loc="upper center",
    bbox_to_anchor=(0.5, 1.25),
    ncol=4
)

# "x" axe labels/numbers rotation
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.6)

# adjust spacing, so it fits in figure
plt.tight_layout()
# endregion

# region 5. Show result
# debug - print(avg_perf_score)
plt.savefig("runner_performance.png")
# endregion
