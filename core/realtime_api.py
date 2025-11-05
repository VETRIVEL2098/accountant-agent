import requests

def get_realtime_data():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/INR"
        res = requests.get(url, timeout=10)
        data = res.json()
        usd = 1 / data["rates"]["USD"]
        return f"1 USD = ₹{usd:.2f}"
    except:
        return "Live INR/USD data unavailable"
