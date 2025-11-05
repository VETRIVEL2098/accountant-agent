import numpy as np

def find_anomalies(df):
    anomalies = []
    avg = df["amount"].mean()
    std = df["amount"].std()

    for _, row in df.iterrows():
        if row["amount"] > avg + 2 * std:
            anomalies.append(f"High-value ₹{row['amount']} ({row['description']})")
    return anomalies
