"""Module for loading and cleaning energy data."""
import pandas as pd

CSV_FILE = "energy_dataset.csv"  # Adjust if necessary

print("🔹 Loading dataset...")
df = pd.read_csv(CSV_FILE)

print("\n✅ Dataset Loaded Successfully! First 5 Rows:")
print(df.head())

print("\n🔹 Dataset Information:")
print(df.info())

print("\n🔹 Missing Values in Each Column:")
print(df.isnull().sum())

df.dropna(inplace=True)

if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

if 'energy_consumption' in df.columns:
    df['energy_consumption'] = df['energy_consumption'].astype(float)

df.to_csv("energy_dataset.csv", index=False)

print("\n energy_dataset.csv")
