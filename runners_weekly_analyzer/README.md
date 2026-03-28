# KPI File Reader — Weekly Running Competition

Python script that reads running data from a CSV file and calculates weekly KPIs and efficiency scores for a group of runners competing against each other.

**Status:** In Progress

---

## Dataset

Weekly training data for 6 runners across 7 days. Each runner logs 6–11 sessions per week, some days with two sessions.

Columns: `runner`, `day`, `distance`, `time`, `elevation`, `bpm`

---

## KPIs Calculated

- Total distance per runner (km)
- Total elevation gain per runner (m)
- Average pace per runner (min/km, converted from MM:SS)
- Average heart rate per runner (bpm)
- Performance score per session — weighted formula using distance, pace, elevation and heart rate
- Average performance score per runner — determines the weekly winner
- Best training day per runner — day with highest performance score
- Consistency score per runner — standard deviation of daily distance (lower = more consistent)
- Weekly winner score — combined average performance and consistency score

---

## Stages

- [x] 1. Load data — read CSV file using pandas
- [x] 2. Validation — check if any runner has fewer than 6 or more than 11 sessions
- [x] 3. Calculations — calculate KPIs for each runner (distance, elevation, pace, bpm)
- [x] 4. Pace — convert MM:SS to decimal minutes per km and calculate average pace
- [] 5. Performance score — calculate weighted perf_score per session
- [ ] 6. Consistency — calculate standard deviation of daily distance per runner
- [ ] 7. Best day — determine each runner's most efficient training day
- [ ] 8. Leaderboard — print daily or weekly leaderboard based on user input
- [ ] 9. Winner score — combine average performance and consistency into final ranking
- [ ] 10. Export — save final leaderboard to results.xlsx using openpyxl

---

## Requirements

- Max 40 lines of code (excluding comments and blank lines)
- At least one `.txt` or `.csv` file for data storage
- Data aggregation — grouping, summarizing
- At least one `if/elif/else` block
- At least one `for` or `while` loop
- Only `pandas` and `openpyxl` allowed
