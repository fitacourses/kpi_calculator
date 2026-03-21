# KPI Calculator: Costs and Gross Margin
# Task: enter data for multiple products and view the results

# -------------------------------------------------------
# 1. DATA INPUT
# Collect data for multiple products and store in lists
# -------------------------------------------------------

products = []
revenues = []
costs = []

count = int(input("How many products do you want to enter? "))

for i in range(count):
    print(f"\n--- Product {i + 1} ---")
    name = input("Product name: ")
    # TODO: collect revenue and costs (use float() to convert)

# -------------------------------------------------------
# 2. CALCULATIONS
# Use a for loop to calculate for each product:
#   - profit (revenue - costs)
#   - gross margin % ( profit / revenue * 100 )
# -------------------------------------------------------

results = {}  # dictionary: product name -> {profit, margin_percent}

for i in range(count):
    # TODO: calculate profit and margin
    pass

# -------------------------------------------------------
# 3. DECISION LOGIC
# Use if/elif/else to evaluate the margin for each product:
#   > 50% — "Excellent margin"
#   20–50% — "Good margin"
#   < 20% — "Low margin, review your costs"
# -------------------------------------------------------

print("\n===== KPI REPORT =====")

for name, data in results.items():
    # TODO: print results and add if/elif/else evaluation
    pass

# -------------------------------------------------------
# 4. SUMMARY
# TODO: calculate and print:
#   - total revenue (sum())
#   - total costs (sum())
#   - total profit
#   - average margin across all products
# -------------------------------------------------------