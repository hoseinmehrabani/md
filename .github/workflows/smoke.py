import pandas as pd
import matplotlib.pyplot as plt


data = {
    'Smoker': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']
}

# ایجاد DataFrame
df = pd.DataFrame(data)

smoker_counts = df['Smoker'].value_counts()
smoker_percentage = smoker_counts / smoker_counts.sum() * 100


print(smoker_percentage)


labels = smoker_percentage.index
sizes = smoker_percentage.values
colors = ['lightcoral', 'lightskyblue']
explode = (0.1, 0)  # جدا کردن قسمت سیگاری‌ها

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # برای دایره‌ای بودن نمودار
plt.title('Percentage of Smokers vs Non-Smokers')
plt.show()
