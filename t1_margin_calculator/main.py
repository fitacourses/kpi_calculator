# region 1. TODO-DONE: Data store and input
products = []
revenues = []
costs = []

# input profit goal and number of products
profit_goal = float(input("What's your profit goal? ")) # use float() to convert (also need cents)
count = int(input("How many products do you want to enter? "))

# input products, revenue and costs
for i in range(count):
    print(f"\n--- Product {i + 1} ---")
    product = input("Product name: ")
    revenue = float(input("How much did you earn from this product? "))
    cost = float(input("How much did it cost to make/buy this product? "))

    if revenue <= 0:
        print(f"Warning: invalid revenue for product {product} ({revenue})")
        continue

# store values into lists
    products.append(product)
    revenues.append(revenue)
    costs.append(cost)
# endregion

# region 2. TODO-DONE: Calculations
# store each product's calculated profit and margin
results = {}
for i in range(len(products)):
    # getting values at index position in each list
    profit = revenues[i] - costs[i]
    margin = (profit / revenues[i]) * 100
    results[products[i]] = {'profit': profit, 'margin': margin}
# endregion

# region 3. TODO-DONE: Decision logic
print("\n===== KPI REPORT =====")
# calculate profit and margin for each product
for name, data in results.items(): 
    print(f"Product name: {name}")
    print(f"    Profit: {data['profit']:.2f}$") # round to 2 decimal places
    print(f"    Margin: {data['margin']:.2f}%") # round to 2 decimal places
    # find the products with the highest and lowest margin
    if data['margin'] >= 50:
        print("Excellent margin!\n")
    elif data['margin'] >= 20:
        print("Good margin\n")
    else:
        print("Low margin, review your costs...\n")
# endregion

# region 4. TODO-DONE: Summary
total_costs = sum(costs)
total_revenue = sum(revenues)

# sum all key "profit" values by iterating through each nested dictionary in results
total_profit = sum(value['profit'] for value in results.values())
# sum all key "margin" values by iterating through each nested dictionary in results + calculate average margin 
avg_margin = sum(percent['margin'] for percent in results.values()) / len(results)

print("===== SUMMARY =====")
print(f"Total costs: {total_costs:.2f}$")
print(f"Total revenue: {total_revenue:.2f}$")
print(f"Total profit: {total_profit:.2f}$")
print(f"Average margin: {avg_margin:.2f}%\n")

# starting values for tracking the best and worst margins
best_product = None
worst_product = None
best_margin = float('-inf')
worst_margin = float('inf')

# update best and worst product based on margin
for name, data in results.items():
    if data["margin"] > best_margin:
        best_margin = data["margin"]
        best_product = name

    if data["margin"] < worst_margin:
        worst_margin = data["margin"]
        worst_product = name

print(f"Best product: {best_product} ({best_margin:.2f}%)")
print(f"Worst product: {worst_product} ({worst_margin:.2f}%)\n")

# compare total profit to the profit goal
if total_profit >= profit_goal:
    print("Goal reached!")
else:
    missed_amount = profit_goal - total_profit
    print(f"Missed profit goal by {missed_amount:.2f}$")
# endregion