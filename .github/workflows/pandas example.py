import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
    'Product': ['Product A', 'Product B', 'Product A', 'Product C'],
    'Quantity': [10, 5, 8, 7],
    'Price': [20, 15, 20, 30]
}


df = pd.DataFrame(data)


df['Total Sales'] = df['Quantity'] * df['Price']

Total_Sales = df['Total Sales'].sum()
print(f"Total Sales: {Total_Sales}")

best_selling_product = df.groupby('Product')['Total Sales'].sum().idxmax()
print(f'Best Selling Product: {best_selling_product}')

sales_by_date = df.groupby('Date')['Total Sales'].sum()
print(sales_by_date)

sales_by_date.plot(kind='pie')
plt.title('Total Sales by Date')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.show()
