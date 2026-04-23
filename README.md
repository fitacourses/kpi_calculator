# 🐍 Data Analysis Fundamentals & Python Programming

> **Course:** "Datu analīzes pamati un programmēšana ar Python" — FITA  
> **Level:** Beginner-friendly  
> **Language:** Python 3

---

## 👋 Welcome

This repository is my personal workspace for storing all projects and assignments from the **"Data Analysis Fundamentals and Programming with Python"** course by FITA.

It includes **4 course assignments** plus a **capstone project** — all grouped in one place to keep everything organized and easy to navigate.

---

## 📚 What I'm learning

- **Syntax & Logic** — Variables, conditions, loops, functions  
- **Data Processing** — Working with files, the Pandas library  
- **Visualization** — Turning raw data into meaningful charts  
- **Web Scraping** — Automating data collection from online sources  
- **Interactive Apps** — Building web interfaces with Streamlit  

---

## 📁 Projects & Assignments

This repository contains **4 assignments** and **1 capstone project**, covering different modules of the course.

### 🏃 Capstone Project (running_app) — Running Performance Analyzer

> *Interactive web app — Streamlit, data analysis, and visualization.*

A Streamlit-based web application for analyzing running performance data from Garmin CSV exports. Upload activity files to visualize pace trends, heart rate insights, and receive coaching recommendations. Features three tabs: Overview (activity summaries), Trends (progression charts), and Insights (personal records and signals).

---

### 📝 Task 1 (t1_margin_calculator) — KPI Product Margin Calculator

> *Syntax & Logic — Python fundamentals with conditions, loops, and dictionaries.*

A terminal-based script that calculates business KPIs — revenue, costs, profit, and gross margin — based on manually entered data. It evaluates each product's margin, prints a full KPI report, and checks whether the total profit reaches a user-defined goal. No files and no external libraries — just pure Python logic.

---

### 📊 Task 2 (t2_runner_analysis)— KPI File Reader: Runners Weekly Analyzer

> *Data Processing — CSV files, pandas, and openpyxl.*

A script that reads weekly running training data from a CSV file and calculates normalized performance KPIs for a group of runners. It processes total distance, elevation, average pace, heart rate, and session performance scores using a normalized scoring model with a BPM efficiency multiplier. The results are exported into an Excel report with weekly statistics and leaderboard sheets.

---

### 📈 Task 3 (t3_runner_visualization) — Runner KPI Visualization

> *Visualization — pandas and matplotlib.*

A Python script that reads running session data from a CSV file and visualizes runner performance using a stacked bar chart. Each session is scored using normalized distance, pace, and elevation metrics, with heart rate applied as an efficiency multiplier. The final chart helps compare runners and shows which score components contributed most to their overall performance.

---

### 🌐 Task 4 (t4_sports_events_scraper) — Web Scraping

> *Web data collection — requests, BeautifulSoup, and HTML parsing.*

A Python script that automatically collects all sports event data from sportlat.lv and converts it into a structured dataset for analysis. The script retrieves event information such as names, dates, and locations, then saves the extracted data into a CSV file for further processing and visualization.

---

## 🛠️ Tools & Libraries Used

- **Python 3** — core programming language
- **pandas** — data manipulation and analysis
- **openpyxl** — Excel file export
- **matplotlib** — data visualization
- **requests / BeautifulSoup** — web scraping
- **Streamlit** — interactive web apps
- **Altair** — advanced data visualization
- **VS Code** — code editor used for development

---

## 🚀 Getting Started

1. Clone this repository  
2. Open the project folder you want to work on  
3. Make sure Python 3 is installed on your machine  
4. Install dependencies if needed  
5. Run the appropriate script or app  

Examples:

```bash
# For assignments (t1-t4)
pip install pandas openpyxl matplotlib requests beautifulsoup4
python main.py 

# For capstone project (running_app)
pip install streamlit pandas altair
streamlit run app.py
```

## 📌 Notes

- Each assignment and project is stored in its own folder
- Every project includes its own README.md with more details on the goal, stages, and expected output
- I've tried to keep the code readable, structured, and beginner-friendly
- The goal is not perfect code, but steady progress through practical tasks
- The capstone project demonstrates integration of all learned skills into an interactive application

---

## 🏫 About the Course

**FITA** offers practical, hands-on IT courses designed for people at all levels. This course is built around real-world data tasks, so that everything you learn can be applied immediately.

---
