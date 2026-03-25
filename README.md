# KPI Calculator

Python script that calculates business KPIs — costs, revenue, and gross margin — based on manually entered data.

## Status: In Progress

## Stages

- [x] **1. Data Input** — collect product names, revenues, costs and profit goal from user
- [x] **2. Calculations** — calculate profit and gross margin % for each product
- [x] **3. Decision Logic & Report** — evaluate each product's margin and print KPI report
- [x] **4. Summary** — total revenue, costs, profit, average margin, best/worst product, profit goal check

## Current Structure

```python
# region 1. DATA INPUT
# TODO: ask the user for a profit goal ✓ DONE
# TODO: collect revenue and costs for each product ✓ DONE
# TODO: if revenue is 0 or less, print a warning and skip this product ✓ DONE
# endregion

# region 2. CALCULATIONS
# TODO: calculate profit (revenue - costs) ✓ DONE
# TODO: calculate gross margin % (profit / revenue * 100) ✓ DONE
# TODO: store profit and margin in results dictionary ✓ DONE
# endregion

# region 3. DECISION LOGIC & REPORT
# TODO: print product name, profit and margin ✓ DONE
# TODO: evaluate margin with if/elif/else: ✓ DONE
#       > 50% — "Excellent margin"
#       20-50% — "Good margin"
#       < 20% — "Low margin, review your costs"
# endregion

# region 4. SUMMARY
# TODO: calculate total revenue, total costs and total profit using sum() ✓ DONE
# TODO: calculate average margin across all products ✓ DONE
# TODO: find and print the product with the highest margin ✓ DONE
# TODO: find and print the product with the lowest margin ✓ DONE
# TODO: compare total profit to the profit goal using if/else ✓ DONE
# endregion
```

## Requirements

- Max 50 lines of code (excluding comments and blank lines)
- No custom functions (def not allowed)
- At least one list and one dictionary for data storage
- No file I/O — all data entered via input()
- At least one if/elif/else block
- At least one for or while loop
