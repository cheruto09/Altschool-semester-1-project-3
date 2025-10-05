import csv
from statistics import mean

#Safe parameter thresholds
SAFE = {
    "ph": (6.5, 8.5),
    "turbidity": (0, 10),   # Measured in NTU
    "temperature": (0, 35)  # In °C
}

# Read the CSV file
def read_data(file_path):
    data = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields from text to float
                try:
                    row["ph"] = float(row["ph"])
                    row["turbidity"] = float(row["turbidity"])
                    row["temperature"] = float(row["temperature"])
                    data.append(row)
                except ValueError:
                    # Skip rows with invalid (non-numeric) data
                    print("⚠️ Skipping invalid row:", row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return data

#  Compute statistics
def compute_stats(data, parameter):
    values = [d[parameter] for d in data if parameter in d]
    return {
        "min": min(values),
        "max": max(values),
        "average": mean(values)
    }

# Check for unsafe readings
def check_thresholds(data):
    alerts = []
    for d in data:
        for param, (low, high) in SAFE.items():
            if d[param] < low or d[param] > high:
                alerts.append({
                    "timestamp": d["timestamp"],
                    "location": d["location"],
                    "param": param,
                    "value": d[param]
                })
    return alerts

# Main program
def main():
    file_path = "water_samples.csv"  # use the csv file in the current directory
    data = read_data(file_path)

    if not data:
        print("No valid data found.")
        return

    print("\n WATER QUALITY REPORT ")
    print("=" * 40)

    # Compute and print stats
    for param in ["ph", "turbidity", "temperature"]:
        stats = compute_stats(data, param)
        print(f"{param.title()} → Min: {stats['min']:.2f}, Max: {stats['max']:.2f}, Avg: {stats['average']:.2f}")

    # Print alerts for unsafe readings
    alerts = check_thresholds(data)
    if alerts:
        print("\n ALERTS: Unsafe Readings Detected ")
        for a in alerts:
            print(f"- {a['timestamp']} | {a['location']} | {a['param'].upper()} = {a['value']}")
    else:
        print("\n All readings are within safe limits!")

if __name__ == "__main__":
    main()
