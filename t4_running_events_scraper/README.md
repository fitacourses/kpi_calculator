# 🌐 Running Events Scraper

> *Web data collection — requests, BeautifulSoup, and HTML parsing.*

This project automatically collects running event data from **sportlat.lv** and converts it into a structured dataset for further analysis. The script retrieves event dates and descriptions from the event calendar and saves the results into a CSV file.

---

## 📌 Overview

This script:

- Downloads event data from sportlat.lv  
- Extracts event dates and descriptions
- Handles "INFO" entries correctly
- Structures the data into rows  
- Saves results into a CSV file  

The goal is to demonstrate basic **web scraping** and **data extraction** techniques using Python.

---

## 📂 Output

The script generates:

```
events.csv
```

Example output:

| date | event |
|------|------|
| 09.05.2026 | Ritma skrējiens 2026 Liepāja |
| 10.05.2026 | Wings for Life World Run |
| 17.05.2026 | Rimi Rīgas maratons 2026 |

---

## 🛠️ Tools & Libraries

- Python 3  
- requests  
- BeautifulSoup  
- csv  
- re (Regular Expressions)

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## ▶️ How to Run

Navigate to project folder:

```bash
cd t4_running_events_scraper
```

Run script:

```bash
python main.py
```

The script will create:

```
events.csv
```

---

## 📊 Data Source

Data is collected from:

```
https://www.sportlat.lv/kalendars/viss
```

---

## 🎯 Learning Goals

This project demonstrates:

- Web scraping fundamentals  
- HTML parsing with BeautifulSoup  
- Data extraction using regex  
- Saving structured data to CSV  

---

## 📌 Notes

- All events are collected without filtering  
- Data cleaning can be done later if needed  
- The script stays under the 40-line assignment requirement
