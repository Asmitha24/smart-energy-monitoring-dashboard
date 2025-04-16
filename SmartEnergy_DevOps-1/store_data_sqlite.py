# store_data_sqlite.py
"""Module to store energy data into an SQLite database."""
import sqlite3
import pandas as pd

# Load your actual dataset
df = pd.read_csv('energy_dataset.csv')

# Optional cleanup
df.columns = (df.columns.str.strip().str.lower().str.replace(' ', '_')
              .str.replace('[^a-zA-Z0-9_]', '', regex=True))

# Connect to SQLite DB
conn = sqlite3.connect('smart_energy.db')
cursor = conn.cursor()

# Drop old table if it exists
cursor.execute("DROP TABLE IF EXISTS energy_data")

# Store the dataset
df.to_sql('energy_data', conn, index=False, if_exists='replace')

conn.commit()
conn.close()

print("✅ Data saved to smart_energy.db in 'energy_data' table.")
