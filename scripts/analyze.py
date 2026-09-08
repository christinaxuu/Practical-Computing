import pandas as pd

df = pd.read_csv("data/patients.csv")
print(df.describe())
print()
print(df.groupby("site")["age"].mean())
