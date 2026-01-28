import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

filename = 'btc_bookticker_1767701380.csv'
df = pd.read_csv(filename)

print(f"Загружено {len(df)} строк.")
df['future_price'] = df['mid_price'].shift(-1)
df['price_change'] = df['future_price'] - df['mid_price']

data = df.dropna()

X = data[['imbalance']]
y = data['price_change']
model = LinearRegression()
model.fit(X, y)

weight = model.coef_[0]    # slope
bias = model.intercept_    # bias

y_pred = model.predict(X)

r_squared = r2_score(y, y_pred)

print("\n" + "="*30)
print("КОЭФФИЦИЕНТЫ")
print("="*30)
print(f"#define MODEL_WEIGHT  {weight:.8f}")
print(f"#define MODEL_BIAS    {bias:.8f}")
print(f"#define MODEL_R2_SCORE  {r_squared:.8f}")
print("="*30)
