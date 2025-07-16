import pandas as pd
df = pd.read_csv('electric_vehicles_spec_2025.csv')
df.loc[:, 'torque_nm'] = df['torque_nm'].fillna(0)
df.loc[:, 'towing_capacity_kg'] = df['towing_capacity_kg'].fillna(0)
df.loc[:, 'number_of_cells'] = df['number_of_cells'].fillna(df['number_of_cells'].median())
df.loc[:, 'fast_charge_port'] = df['fast_charge_port'].fillna('Unknown')
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10,6))
sns.countplot(data=df, y='brand', order=df['brand'].value_counts().index[:10])
plt.title('Top 10 Brands by Number of EV Models')
plt.xlabel('Number of Models')
plt.ylabel('Brand')
plt.show()
plt.figure(figsize=(10,6))
sns.histplot(df['battery_capacity_kWh'], kde=True)
plt.title('Battery Capacity Distribution (kWh)')
plt.xlabel('Battery Capacity (kWh)')
plt.show()


