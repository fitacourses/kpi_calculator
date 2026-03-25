# KPI Calculator: Costs and Gross Margin
# Task: enter data for multiple products and view the results

# region 1. DATA INPUT
products = []
revenues = []
costs = []

# TODO-DONE: ask the user for a profit goal (use float() to convert)
profit_goal = float(input("What's your profit goal (in €)? "))

count = int(input("How many products do you want to enter? "))

for i in range(count):
    # i counts loop iterations (0,1,2...), +1 makes it human-readable (1,2,3...)
    # \n adds empty line before each product to separate output visually
    print(f"\n--- Product {i + 1} ---")
    product = input("Product name: ")
    # TODO-DONE: collect revenue and costs (use float() to convert)
    revenue = float(input("How much did you earn from this product (in €)? "))
    cost = float(input("How much did it cost to make/buy this product (in €)? "))
    # TODO-DONE: if revenue is 0 or less, print a warning and skip this product
    if revenue <= 0:
        print(f"Warning: invalid revenue for product {product} ({revenue})")
        continue
    # TODO-DONE: store valid products, revenues and costs into lists
    products.append(product)
    revenues.append(revenue)
    costs.append(cost)
# endregion

# region 2. CALCULATIONS
results = {}  # dictionary: product name -> {profit, margin}

for i in range(count):
    # TODO-DONE: calculate profit by getting values at index position in each list for current iteration
    profit = revenues[i] - costs[i]
    # TODO-DONE: calculate gross margin % by dividing profit by revenue for the current product, times 100 to get percent
    margin = (profit / revenues[i]) * 100
    # TODO-DONE: store profit and margin for each product and build a dictionary with keys
    results[products[i]] = {'profit': profit, 'margin': margin}
# endregion

# region 3. DECISION LOGIC & REPORT
print("\n===== KPI REPORT =====")

# loop trough each key-value pair, product name and nested dictionary with profit and margin
for name, data in results.items():
    # TODO-DONE: print product name, profit and margin
    print(f"Product name: {name}\n Profit: {data['profit']}\n Margin: {data['margin']}")
    # TODO-DONE: evaluate margin with if/elif/else:
    #       > 50% — "Excellent margin"
    #       20-50% — "Good margin"
    #       < 20% — "Low margin, review your costs"
    if data['margin'] >= 50:
        print("Excellent margin")
    elif data['margin'] >= 20:
        print("Good margin")
    else:
        print("Low margin, review your costs")
# endregion

# region 4. SUMMARY
# TODO-DONE: calculate total revenue, total costs and total profit
total_costs = sum(costs)
total_revenue = sum(revenues)
# sum all key "profit" values by iterating through each nested dictionary in results
total_profit = sum(value['profit'] for value in results.values())
# TODO-DONE: calculate average margin across all products
avg_margin = sum(percent['margin'] for percent in results.values()) / len(results)
# TODO-DONE: print all summary values
print(f"Total costs: {total_costs}\n Total revenue: {total_revenue}\n Total profit: {total_profit}\n Average margin: {avg_margin}")
# TODO-DONE: if current product margin is higher than highest so far, update best product
# TODO-DONE: if current product margin is lower than lowest so far, update worst product
best_product = None
best_margin = float('-inf') # starting point is worse than anything that's iterated
worst_product = None
worst_margin = float('inf') # starting point is better than anything that's iterated
# loop through all key-value pairs in results dictionary
for name, data in results.items():
    if data['margin'] > best_margin:
        best_margin = data['margin']
        best_product = name
    elif data['margin'] < worst_margin:
        worst_margin = data['margin']
        worst_product = name
print(f"Best product {best_product}\n Worst product: {worst_product}\n Best margin: {best_margin} \n Worst margin: {worst_margin}")

# TODO: compare total profit to the profit goal using if/else
#       if reached — "Goal reached!"
#       if not — print how much is still missing
# endregion