# 📌 KPI Calculator: Costs & Gross Margin

## 📌 Overview

This project is a simple Python-based KPI calculator that allows the user to input product data and generates:

- Profit per product
- Gross margin (%) per product
- Margin evaluation (Excellent / Good / Low)
- Total business performance summary
- Best and worst performing products
- Profit goal comparison

All calculations are done through a single Python script using user input.

---

## 📂 How It Works

The script asks the user to enter:

- A **profit goal**
- Number of products
- For each product:
  - Product name
  - Revenue
  - Cost

⚠️ If revenue is **0 or negative**, the product is skipped with a warning.

---

## 📊 KPIs Calculated

### ✅ Profit

`Profit = Revenue - Cost`

---

### ✅ Gross Margin (%)

`Margin = (Profit / Revenue) * 100`

---

### ✅ Margin Evaluation

- **≥ 50%** → Excellent margin  
- **20% – 49%** → Good margin  
- **< 20%** → Low margin (review costs)

---

### ✅ Totals

- Total Revenue
- Total Costs
- Total Profit

---

### ✅ Average Margin

Average margin across all valid products.

---

### ✅ Best & Worst Product

- Best product = highest margin
- Worst product = lowest margin

---

### ✅ Profit Goal Check

- If total profit ≥ goal → ✅ Goal reached  
- If not → shows how much is missing  

---

## ⚙️ Script Workflow (Step-by-Step)

1. Ask user for profit goal  
2. Ask number of products  
3. Loop through product inputs  
4. Validate revenue (skip invalid entries)  
5. Store data in lists  
6. Calculate profit and margin per product  
7. Store results in a dictionary  
8. Print KPI report with evaluations  
9. Calculate totals and averages  
10. Identify best and worst products  
11. Compare total profit to goal  

---

## 📁 Output

Console output includes:

- KPI report per product  
- Margin evaluation  
- Business summary  
- Best & worst product  
- Profit goal result  

---

## 🛠 Requirements

- Python 3.x  
- No external libraries needed  

---

## 🎓 Assignment Requirements Covered

This project includes:

- ✅ Loops (`for`)  
- ✅ Conditional logic (`if / elif / else`)  
- ✅ Lists and dictionaries  
- ✅ User input handling  
- ✅ Data processing and calculations
