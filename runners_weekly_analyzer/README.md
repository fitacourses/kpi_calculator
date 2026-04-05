# 📊 Runners Weekly Analyzer

## 📌 Overview

This project reads weekly running session data from a CSV file and generates:

- Individual runner statistics  
- Normalized performance scores  
- Component-based performance breakdown  
- Daily and weekly leaderboards  
- A full Excel report (`results.xlsx`)  

All calculations are done automatically by a single Python script.

---

## 📂 Dataset Format (`data.csv`)

Your input file must include the following columns:

| Column     | Description              |
|------------|--------------------------|
| runner     | Runner name              |
| day        | Day of the week          |
| distance   | Distance run (km)        |
| time       | Duration (MM:SS)         |
| elevation  | Elevation gain (m)       |
| bpm        | Average heart rate (bpm) |

---

## 📊 KPIs the Script Calculates

### ✅ Total Distance
Total distance per runner.

### ✅ Total Elevation
Total elevation gain per runner.

### ✅ Average Heart Rate
Average BPM per runner.

### ✅ Average Pace

The script:

- Converts `MM:SS` into minutes  
- Calculates average pace per runner  
- Converts result back into `MM:SS`  

---

## ✅ Performance Score

Each session receives a normalized performance score based on:

- Distance (0–30 km)
- Pace (8:00–3:30 min/km)
- Elevation (50–500 m)

Each metric is normalized to a **0–1 range**:

```
Base Score = Distance + Pace + Elevation
```

Heart rate is applied as an efficiency multiplier:

```
Final Score = Base Score × BPM Multiplier
```

### BPM Multiplier

- Range: **1.00 – 1.20**
- Lower heart rate → higher multiplier
- Rewards efficient runs without dominating performance

---

## 📊 Weekly Performance Metrics

The script calculates:

- Average Performance Score  
- Average Distance Score  
- Average Pace Score  
- Average Elevation Score  
- Average BPM Bonus  

This allows you to understand **why a runner performed well**.

---

## 🏆 Leaderboards

### Weekly Leaderboard

Runners ranked by:

- Average performance score

### Daily Leaderboards

Each day shows:

- Best runner  
- Performance score per session  

---

## ⚙️ Script Workflow

1. Load CSV file  
2. Calculate base statistics  
3. Convert time to pace  
4. Normalize performance metrics  
5. Apply BPM multiplier  
6. Calculate session scores  
7. Compute weekly averages  
8. Build leaderboards  
9. Round values  
10. Export to Excel  

---

## 📁 Output

The script generates:

- Weekly Stats  
- Weekly Leaderboard  
- One sheet per day  

---

## 🛠 Requirements

- Python 3.10+
- pandas
- openpyxl

Install dependencies:

```bash
pip install pandas openpyxl
```

---

## 🎯 Project Goal

This project demonstrates:

- Data processing with pandas  
- Normalized scoring systems  
- Performance analytics  
- Leaderboard generation  
- Excel export automation
