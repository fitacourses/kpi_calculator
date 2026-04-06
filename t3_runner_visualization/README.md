# 📊 Runner Performance Visualization

## 📌 Overview

This project reads weekly running session data from a CSV file and generates a stacked bar chart comparing runner performance.

The visualization is based on a normalized performance scoring system and shows how each metric contributes to the final score.

All calculations are performed automatically using a single Python script.

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

Each row represents **one running session**.

---

## 📊 KPIs the Script Calculates

- ✅ Distance Score  
- ✅ Pace Score  
- ✅ Elevation Score  
- ✅ BPM Bonus  

---

## ✅ Performance Score

Each session receives a normalized **base performance score (0–1 per metric)** based on:

- Distance (0–30 km)
- Pace (8:00–3:30 min/km)
- Elevation (50–500 m)
- Heart rate is applied as an efficiency multiplier (1.00–1.20)

```
Base Score = Distance + Pace + Elevation
Final Score = Base Score × BPM Multiplier
```

---

## 📊 Visualization

The script generates a **stacked bar chart** showing:

- Distance contribution  
- Pace contribution  
- Elevation contribution  
- BPM bonus  

Each bar represents **average performance per runner**.

This allows you to:

- Compare runners  
- Understand performance strengths  
- See score contribution breakdown  

---

## ⚙️ Script Workflow

1. Load CSV data  
2. Convert time to pace  
3. Normalize performance metrics  
4. Apply BPM multiplier  
5. Calculate session scores  
6. Group data by runner  
7. Build stacked bar chart  
8. Customize chart  
9. Save visualization  

---

## 📈 Output

The script generates:

```
runner_performance.png
```

The image contains a stacked bar chart comparing runner performance.

---

## 🛠 Requirements

- Python 3.10+
- pandas
- matplotlib

Install dependencies:

```bash
pip install pandas matplotlib
```

---

## 🎯 Project Goal

This project demonstrates:

- Data processing with pandas  
- Normalized scoring systems  
- Data visualization with matplotlib  
- Performance analytics  
- Stacked bar chart visualization
