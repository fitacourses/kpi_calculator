# 📌 Running Data Analysis Project

## 📌 Overview

This project reads weekly running session data from a CSV file and generates:

- Individual runner statistics
- Performance and consistency scores
- Daily and weekly leaderboards
- A full Excel report (`results.xlsx`)

All calculations are done automatically by a single Python script.

---

## 📂 Dataset Format (`data.csv`)

Your input file **must include the following columns**:

| Column     | Description                  |
|------------|------------------------------|
| runner     | Runner's name                |
| day        | Day of the week              |
| distance   | Distance run (km)            |
| time       | Duration in MM:SS            |
| elevation  | Elevation gain (m)           |
| bpm        | Average heart rate (bpm)     |

✅ Each runner should log **6–11 sessions per week** — the script warns you if not.

---

## 📊 KPIs the Script Calculates

### ✅ Total Distance

Sum of all distance values for the runner.

### ✅ Total Elevation

Total climbing in meters.

### ✅ Average Heart Rate

Average BPM across all sessions.

### ✅ Average Pace

The script:

- Converts every `MM:SS` time into minutes
- Calculates the average pace per km
- Converts it back into a clean `MM:SS` format

---

### ✅ Performance Score

Each session gets a score based on:

- Distance
- Pace
- Elevation
- Heart rate

---

### ✅ Weekly Average Performance

Average of all performance scores.

---

### ✅ Consistency Score

Standard deviation of performance scores.

- Lower = more consistent

---

### ✅ Power Ranking

A combined score based on:

- Performance
- Consistency

➡️ Higher score = stronger training week.

---

### ✅ Leaderboards

- Weekly leaderboard (overall ranking)
- Daily leaderboards (best performance per day)

---

## ⚙️ Script Workflow (Step-By-Step)

1. Load data from CSV  
2. Check session counts and apply warnings  
3. Calculate base stats (distance, elevation, BPM)  
4. Convert `MM:SS` times into minutes and compute pace  
5. Format pace back into `MM:SS`  
6. Calculate performance score for each session  
7. Compute weekly averages  
8. Calculate consistency  
9. Generate power ranking  
10. Build weekly and daily leaderboards  
11. Round values for readability  
12. Export everything to `results.xlsx`  

---

## 📁 Output

✅ `results.xlsx` contains:

- Weekly Stats sheet  
- Weekly Leaderboard sheet  
- One sheet per day with daily rankings  

All formatted clearly and ready to read.

---

## 🛠 Requirements

You will need:

- Python 3.10+
- pandas
- openpyxl
- A valid `data.csv` file

---

## 🎓 Assignment Requirements Covered

This project includes:

- ✅ At least one loop  
- ✅ At least one if-statement  
- ✅ File reading and writing  
- ✅ Data processing
