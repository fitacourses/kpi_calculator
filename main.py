# KPI Calculator: Costs and Gross Margin

# region 1. DATA INPUT
products = []
revenues = []
costs = []

# TODO-DONE: ask the user for a profit goal (use float() to convert)
profit_goal = float(input("What's your profit goal (in $)? "))

count = int(input("How many products do you want to enter? "))

for i in range(count):
    # i counts loop iterations (0,1,2...), +1 makes it human-readable (1,2,3...)
    # \n adds empty line before each product to separate output visually
    print(f"\n--- Product {i + 1} ---")
    product = input("Product name: ")
    # TODO-DONE: collect revenue and costs (use float() to convert)
    revenue = float(input("How much did you earn from this product? "))
    cost = float(input("How much did it cost to make/buy this product? "))
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

for i in range(len(products)):
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
    print(f"Product name: {name}\n Profit: {data['profit']:.2f}$\n Margin: {data['margin']:.2f}%")
    # TODO-DONE: evaluate margin with if/elif/else:
    #       > 50% — "Excellent margin"
    #       20-50% — "Good margin"
    #       < 20% — "Low margin, review your costs"
    if data['margin'] >= 50:
        print("Excellent margin! \n")
    elif data['margin'] >= 20:
        print("Good margin \n")
    else:
        print("Low margin, review your costs... \n")
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
print(f"Total costs: {total_costs:.2f}$\n Total revenue: {total_revenue:.2f}$\n Total profit: {total_profit:.2f}$\n Average margin: {avg_margin:.2f}%\n")
# TODO-DONE: if current product margin is higher than highest so far, update best product
# TODO-DONE: if current product margin is lower than lowest so far, update worst product
best_product, worst_product = None, None
# starting point is lower/higher than anything that's iterated
best_margin, worst_margin = float('-inf'), float('inf')
# loop through all key-value pairs in results dictionary
for name, data in results.items():
    if data['margin'] > best_margin:
        best_margin = data['margin']
        best_product = name
    if data['margin'] < worst_margin:
        worst_margin = data['margin']
        worst_product = name
print(f"Best product: {best_product}\n Worst product: {worst_product}\n Best margin: {best_margin:.2f}% \n Worst margin: {worst_margin:.2f}% \n")

# TODO-DONE: compare total profit to the profit goal
if total_profit > profit_goal:
    print("Goal reached!")
else:
    print(f"Missed profit goal by {profit_goal - total_profit:.2f}$")
# endregion