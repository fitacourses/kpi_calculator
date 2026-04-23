# 🏃 Running Performance Analyzer

> *Streamlit app for analyzing Garmin CSV running data — pace trends, heart rate insights, and coaching signals.*

This project provides a web-based application to analyze running performance data exported from Garmin devices. Upload CSV files to visualize pace trends, estimate personal records, and receive simple coaching recommendations based on pace and heart rate data.

---

## 📌 Overview

This app:

- Processes Garmin CSV activity exports  
- Calculates pace trends and daily summaries  
- Visualizes effort proxy (heart rate vs. pace)  
- Provides coaching insights and records  
- Supports multiple file uploads for combined analysis  

The goal is to demonstrate **data analysis** and **interactive visualization** techniques using Python and Streamlit.

---

## 📂 Features

The app includes three main tabs:

- **Overview**: Activity table, totals, and run type summaries  
- **Trends**: Cumulative distance chart and pace progression  
- **Insights**: Personal records and coaching recommendations  

Example insights:

- Fastest pace estimates  
- Elevation gain records  
- Effort proxy scatter plots  
- Coaching signals based on heart rate and pace  

---

## 🛠️ Tools & Libraries

- Python 3  
- Streamlit  
- Pandas  
- Altair  
- Math  

Install dependencies:

```bash
pip install streamlit pandas altair
```

---

## ▶️ How to Run

Navigate to project folder:

```bash
cd running_app
```

Run the app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📊 Data Source

Data is loaded from Garmin CSV exports containing columns like:

- Activity date  
- Distance (km)  
- Average pace  
- Heart rate (avg/max)  
- Elevation gain/loss  
- Calories  

Upload multiple files to combine data from different periods.

---

## 🎯 Learning Goals

This project demonstrates:

- Interactive web app development with Streamlit  
- Data cleaning and processing with Pandas  
- Chart creation with Altair  
- User interface design for data analysis  

---

## 📌 Notes

- Supports Latvian language column names in Garmin exports  
- Handles multiple CSV uploads for comprehensive analysis  
- Provides guardrails for realistic pace and heart rate values  
- Focuses on distance-weighted averages for accurate trends</content>
<parameter name="filePath">/home/sandis_linards/workspace/ai_data_analytics_python/running_app/README.md