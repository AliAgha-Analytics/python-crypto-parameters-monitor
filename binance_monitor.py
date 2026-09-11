import requests
import pandas as pd
import time
import schedule

# -- Telegram Config --
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"   # enables bold/italic formatting
    }
    requests.post(url, data=payload)

# -- Public Contract Info --
def fetch_binance_contracts(watchlist):
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    data = requests.get(url).json()["symbols"]
    records = []
    for s in data:
        if s["symbol"] in watchlist:
            tick_size, step_size, min_qty, max_qty, min_price, max_price = None, None, None, None, None, None
            for f in s.get("filters", []):
                if f["filterType"] == "PRICE_FILTER":
                    min_price = f.get("minPrice")
                    max_price = f.get("maxPrice")
                    tick_size = f.get("tickSize")
                if f["filterType"] == "LOT_SIZE":
                    min_qty = f.get("minQty")
                    max_qty = f.get("maxQty")
                    step_size = f.get("stepSize")

            records.append({
                "exchange": "Binance",
                "symbol": s["symbol"],
                "contractType": s.get("contractType"),
                "marginAsset": s.get("marginAsset"),
                "status": s.get("status"),
                "pricePrecision": s.get("pricePrecision"),
                "quantityPrecision": s.get("quantityPrecision"),
                "tickSize": tick_size,
                "minPrice": min_price,
                "maxPrice": max_price,
                "minQty": min_qty,
                "maxQty": max_qty,
                "stepSize": step_size
            })
    return pd.DataFrame(records)

# -- Snapshot Save/Load --
def save_snapshot(df, file="binance_snapshot.csv"):
    df.to_csv(file, index=False)

def load_snapshot(file="binance_snapshot.csv"):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        return pd.DataFrame()

# --- Comparison Logic ---
def detect_changes(new_df, old_df):
    changes = []
    if old_df.empty:
        return ["No previous snapshot found. Initial run."]
    
    merged = new_df.merge(old_df, on=["exchange","symbol"], suffixes=("_new","_old"))
    
    for _, row in merged.iterrows():
        for col in new_df.columns:
            if col in ["exchange","symbol"]: 
                continue
            if str(row.get(f"{col}_new")) != str(row.get(f"{col}_old")):
                # Bold coin, italic parameter
                changes.append(
                    f"*{row['symbol']}*: _{col}_ changed from {row.get(f'{col}_old')} to {row.get(f'{col}_new')}"
                )
    return changes

# -- Monitor Task --
def monitor_binance():
    watchlist = [
        "BTCUSDT","ETHUSDT","BCHUSDT","XRPUSDT","LTCUSDT","SOLUSDT",
        "ADAUSDT","DOGEUSDT","DOTUSDT","BNBUSDT"
    ]
    new_df = fetch_binance_contracts(watchlist)
    old_df = load_snapshot()
    changes = detect_changes(new_df, old_df)

    # Output with emojis
    if changes:
        message = "🔴 *Binance Parameters Monitor:*\n" + "\n".join([f" - {c}" for c in changes])
    else:
        message = "🟢 *Binance Parameters Monitor:*\nNo changes detected."

    print(message)              # Console
    send_telegram_message(message)  # Telegram
    save_snapshot(new_df)

# -- Scheduler --
schedule.every(30).minutes.do(monitor_binance)

print("Binance Parameters Monitor started. Checking every 30 minutes...\n")
send_telegram_message("🟢 *Binance Parameters Monitor started.* Checking every 30 minutes...")

# Run immediately once so you don’t wait 30 minutes
monitor_binance()

while True:
    schedule.run_pending()
    time.sleep(1)
