import csv
import requests
import time

# Define the Pixoo API endpoint
PIXOO_API_URL = "http://localhost:5000/text"

# Define the CSV file path
CSV_FILE_PATH = "data/kpis.csv"

# Function to read KPI data from CSV
def read_kpis_from_csv():
    kpis = {}
    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                kpis[row["metric"]] = row["value"]
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return kpis

# Function to send KPI data to Pixoo64
def send_kpis_to_pixoo(kpis):
    kpi_display = f"👥 {kpis.get('attendance', '0/0')}  🚩 {kpis.get('red_flags', '0')}  🏁 {kpis.get('green_flags', '0')}"

    payload = {
        "text": kpi_display,
        "x": "0",
        "y": "15",
        "r": "255",
        "g": "255",
        "b": "255"
    }

    try:
        response = requests.post(PIXOO_API_URL, data=payload)
        print(f"Sent: {kpi_display} | Response: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

# Main loop to update every 5 seconds
if __name__ == "__main__":
    while True:
        kpis = read_kpis_from_csv()
        send_kpis_to_pixoo(kpis)
        time.sleep(5)
