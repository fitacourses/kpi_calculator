# KPI Calculator: Costs and Gross Margin
# Task: enter data for multiple products and view the results

# region 1. DATA INPUT
products = []
revenues = []
costs = []

# TODO: ask the user for a profit goal (use float() to convert)
profit = float(input("What's your profit goal?"))

count = int(input("How many products do you want to enter? "))

for i in range(count):
    # i counts loop iterations (0,1,2...), +1 makes it human-readable (1,2,3...)
    # \n adds empty line before each product to separate output visually
    print(f"\n--- Product {i + 1} ---")
    name = input("Product name: ")
    # TODO: collect revenue and costs (use float() to convert)
    # TODO: if revenue is 0 or less, print a warning and skip this product
# endregion

# region 2. CALCULATIONS
results = {}  # dictionary: product name -> {profit, margin_percent}

for i in range(count):
    # TODO: calculate profit (revenue - costs)
    # TODO: calculate gross margin % (profit / revenue * 100)
    # TODO: store profit and margin in results dictionary
    pass
# endregion

# region 3. DECISION LOGIC & REPORT
print("\n===== KPI REPORT =====")

for name, data in results.items():
    # TODO: print product name, profit and margin
    # TODO: evaluate margin with if/elif/else:
    #       > 50% — "Excellent margin"
    #       20-50% — "Good margin"
    #       < 20% — "Low margin, review your costs"
    pass
# endregion

# region 4. SUMMARY
# TODO: calculate total revenue, total costs and total profit using sum()
# TODO: calculate average margin across all products
# TODO: print all summary values

# TODO: find and print the product with the highest margin
# TODO: find and print the product with the lowest margin

# TODO: compare total profit to the profit goal using if/else
#       if reached — "Goal reached!"
#       if not — print how much is still missing
# endregion