# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv("USvideos.csv")

# %%
print("First 5 rows: \n")
print(df.head())

# %%
print("\nStatistical description of data: ")
print(df.describe())

# %%
print("\n Info of data: ")
print(df.info())

# %%
print("\nShape of data:")
print(df.shape)

# %%
target_regression = "views"
#calculate top 25% quantile of views
viral_threshold = df["views"].quantile(0.75)
print("\nViral Threshold:",viral_threshold)



# %%
#Create Classification target 
df["viral"] = (df["views"] > viral_threshold).astype(int)

# %%
# Viral column
print("\n Viral Column:")
print(df[["views","viral"]].head(10))

# %%



