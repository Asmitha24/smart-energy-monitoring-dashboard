"""Flask app for Smart Energy data visualization."""
from flask import Flask, render_template, request, send_file
import pandas as pd
import sqlite3
import io

app = Flask(__name__)
DB_PATH = "smart_energy.db"

def load_data(country=None, fuel_type=None):
    """Loads energy data from the SQLite database based on filters."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM energy_data"
    filters = []

    if country:
        filters.append(f"country = '{country}'")
    if fuel_type:
        filters.append(f"fuel_type = '{fuel_type}'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    data_frame = pd.read_sql_query(query, conn)
    conn.close()
    return data_frame

def get_chart_data(data_frame):
    """Generates data for the energy consumption chart."""
    if data_frame.empty:
        return {
            "years": [],
            "used": [],
            "generated": [],
            "saved": [],
            "wasted": [],
            "difference": []
        }

    grouped = data_frame.groupby("year").sum(numeric_only=True).reset_index()
    used = grouped["energy_consumption_ej"]
    generated = used * 1.10
    saved = generated - used
    wasted = generated * 0.02
    difference = generated - used

    return {
        "years": list(grouped["year"]),
        "used": list(used.round(2)),
        "generated": list(generated.round(2)),
        "saved": list(saved.round(2)),
        "wasted": list(wasted.round(2)),
        "difference": list(difference.round(2))
    }

def compute_stats(data_frame):
    """Computes summary statistics for energy data."""
    used = data_frame["energy_consumption_ej"].sum()
    generated = used * 1.10
    saved = generated - used
    wasted = generated * 0.02
    return {
        "used": round(used, 2),
        "generated": round(generated, 2),
        "saved": round(saved, 2),
        "wasted": round(wasted, 2)
    }

def get_filters():
    """Fetches distinct country and fuel type values for dropdown filters."""
    conn = sqlite3.connect(DB_PATH)
    data_frame = pd.read_sql_query("SELECT DISTINCT country, fuel_type FROM energy_data", conn)
    conn.close()
    return {
        "countries": data_frame["country"].dropna().unique().tolist(),
        "fuel_types": data_frame["fuel_type"].dropna().unique().tolist()
    }

@app.route('/')
def index():
    """Renders the main index page with energy data and filters."""
    country = request.args.get('country')
    fuel_type = request.args.get('fuel_type')

    data_frame = load_data(country, fuel_type)
    stats = compute_stats(data_frame)
    chart_data = get_chart_data(data_frame)
    filters = get_filters()

    return render_template(
        "index.html",
        filters=filters,
        selected_country=country,
        selected_fuel_type=fuel_type,
        energy_stats=stats,
        chart_data=chart_data
    )

@app.route('/download')
def download_csv():
    """Downloads the currently filtered energy data as a CSV file."""
    data_frame = load_data()
    output = io.StringIO()
    data_frame.to_csv(output, index=False)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv',
                     download_name='filtered_energy_data.csv',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
