import requests
import pandas as pd
import time
from datetime import datetime

symbol = "BTCUSDT"
url = "https://api.binance.com/api/v3/ticker/bookTicker"

data = []
iterations = 10800

print(f"Начинаю сбор данных для {symbol}")

try:
    for i in range(iterations):
        try:
            r = requests.get(url, params={"symbol": symbol}, timeout=5).json()

            bid_price = float(r["bidPrice"])
            bid_qty = float(r["bidQty"])
            ask_price = float(r["askPrice"])
            ask_qty = float(r["askQty"])

            mid_price = (bid_price + ask_price) / 2

            imbalance = (bid_qty - ask_qty) / (bid_qty + ask_qty)

            row = {
                "timestamp": int(time.time()),
                "bid_price": bid_price,
                "bid_qty": bid_qty,
                "ask_price": ask_price,
                "ask_qty": ask_qty,
                "mid_price": mid_price,
                "imbalance": imbalance
            }
            data.append(row)

            if i % 10 == 0:
                print(f"Собрано {i}/{iterations}. Imbalance: {imbalance:.4f}")

        except Exception as e:
            print(f"Ошибка на итерации {i}: {e}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Сбор прерван. Сохраняю то, что есть")

df = pd.DataFrame(data)
filename = f"btc_bookticker_{int(time.time())}.csv"
df.to_csv(filename, index=False)

print(f"Готово! Данные сохранены в {filename}")
print(df.head())