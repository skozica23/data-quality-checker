import pandas as pd
import os
import time

# START TIMER
start_time = time.time()


# LOAD DATA
print("Loading data...")


df = pd.read_csv(
    "data/yellow_tripdata_2021-01.csv", 
    low_memory=False,
  #  nrows=100000 
)

columns_to_check = ["tolls_amount", "tip_amount", "passenger_count", "fare_amount"]

# BASIC DATA QUALITY CHECKS
print("Running basic data quality checks...")
missing_values = df[columns_to_check].isnull().sum()
duplicate_count = df.duplicated().sum()

invalid_counts = {}
for col in columns_to_check:
    numeric_series = pd.to_numeric(df[col], errors="coerce")
    invalid_counts[col] = numeric_series.isnull().sum() - missing_values[col]
    df[col] = numeric_series

negative_counts = {}
for col in ["tolls_amount", "tip_amount", "fare_amount"]:
    negative_counts[col] = (df[col] < 0).sum()

invalid_passenger_logic = ((df["passenger_count"] <= 0) | (df["passenger_count"] > 6)).sum()

# ADVANCED DATA ANALYSIS
print("Running advanced analysis...")
df["pickup_time"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["dropoff_time"] = pd.to_datetime(df["tpep_dropoff_datetime"])
df["trip_duration_sec"] = (df["dropoff_time"] - df["pickup_time"]).dt.total_seconds()

short_trips = (df["trip_duration_sec"] < 60).sum()
zero_distance_paid = ((df["trip_distance"] == 0) & (df["fare_amount"] > 0)).sum()
tip_greater_than_fare = (df["tip_amount"] > df["fare_amount"]).sum()
no_tip_high_fare = ((df["fare_amount"] > 30) & (df["tip_amount"] == 0)).sum()

passenger_distribution = df["passenger_count"].value_counts().to_dict()
fare_stats = df["fare_amount"].describe().to_dict()
tip_stats = df["tip_amount"].describe().to_dict()

# STOP TIMER
end_time = time.time()
execution_time = round(end_time - start_time, 2)

# BUILD FINAL REPORT
print("Generating report file...")
report_lines = [
    "=== DATA QUALITY & ANALYSIS REPORT ===",
    f"Total rows analyzed: {len(df)}",
    f"Execution time: {execution_time} seconds\n",
    "Basic Data Quality:"
]

report_lines.extend([f"  Missing {col}: {val}" for col, val in missing_values.items()])
report_lines.extend([f"  Invalid {col}: {val}" for col, val in invalid_counts.items()])
report_lines.extend([f"  Negative {col}: {val}" for col, val in negative_counts.items()])

report_lines.extend([
    f"  Invalid passenger count: {invalid_passenger_logic}",
    f"  Duplicates: {duplicate_count}",
    "\nAdvanced Analysis:",
    f"  Trips under 1 minute: {short_trips}",
    f"  Zero distance but paid rides: {zero_distance_paid}",
    f"  Tip greater than fare: {tip_greater_than_fare}",
    f"  No tip on expensive rides (>30$): {no_tip_high_fare}",
    "\nPassenger distribution:"
])

for k, v in passenger_distribution.items():
    report_lines.append(f"  {k}: {v}")

report_lines.append("\nFare statistics:")
for k, v in fare_stats.items():
    report_lines.append(f"  {k}: {round(v, 2)}")

report_lines.append("\nTip statistics:")
for k, v in tip_stats.items():
    report_lines.append(f"  {k}: {round(v, 2)}")
    
# The following insights are based on initial data exploration and are 
# included in the automated report to provide business context.
report_lines.extend([
    "\n=========================================",
    "💡 BUSINESS INSIGHTS & ACTIONS",
    "=========================================",
    "- DATA QUALITY: The raw dataset contains significant anomalies. Negative fares and 0-distance paid rides highly indicate system errors, refunds, or test logs that need filtering.",
    "- USER BEHAVIOR: A massive volume of expensive rides (>$30) resulted in $0 tip. This strongly suggests cash tipping is not being logged by the system, rather than actual lack of tips.",
    "- DEMOGRAPHICS: The vast majority of trips are single-passenger rides. From a fleet optimization perspective, standard sedans are highly preferable and more cost-effective than large SUVs or vans.",
    "- ML READINESS: The dataset is currently NOT ready for Machine Learning. It requires a mandatory cleaning pipeline (removing negative values, unparseable strings, and extreme outliers) before any predictive modeling."
])

#  SAVE REPORT
os.makedirs("output", exist_ok=True)
with open("output/report.txt", "w") as f:
    f.write("\n".join(report_lines))

print(f"Report generated successfully in {execution_time} seconds!")