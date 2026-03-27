# KPI File Reader — Weekly Running Competition

Python script that reads running data from a CSV file and calculates weekly KPIs for a group of runners competing against each other.

## Status: In Progress

## Dataset

Weekly training data for 6 runners across 7 days.
Each runner logs 6–11 sessions per week, some days with two sessions.

Columns: `runner`, `day`, `distance_km`, `pace_min_per_km`, `heart_rate_bpm`

## KPIs Calculated

- Total distance per runner
- Average pace per runner
- Average heart rate per runner
- Efficiency score per session (based on distance, pace and heart rate)
- Average efficiency per runner — determines the weekly winner

## Stages

- [ ] **1. Load data** — read CSV file using pandas
- [ ] **2. Calculations** — calculate KPIs for each runner
- [ ] **3. Efficiency** — calculate efficiency score per session and average per runner
- [ ] **4. Report** — print results and determine the most efficient runner of the week

## Requirements

- Max 40 lines of code (excluding comments and blank lines)
- At least one .txt or .csv file for data storage
- Data aggregation — grouping, summarizing
- At least one if/elif/else block
- At least one for or while loop
- Only pandas and openpyxl allowed
