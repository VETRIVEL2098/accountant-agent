import pandas as pd
import requests

def get_exchange_rate(base="USD", target="INR"):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        res = requests.get(url, timeout=10)
        data = res.json()
        return data["rates"].get(target, 83.0)
    except:
        return 83.0

def load_transactions(path):
    df = pd.read_csv(path)
    df.columns = [c.lower().strip() for c in df.columns]

    if "currency" in df.columns:
        for i, row in df.iterrows():
            if row["currency"].upper() == "USD":
                rate = get_exchange_rate("USD", "INR")
                df.at[i, "amount"] = float(row["amount"]) * rate
                df.at[i, "currency"] = "INR"

    df["amount"] = df["amount"].astype(float)
    return df
