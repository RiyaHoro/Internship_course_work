# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# 

# %%
df = pd.read_csv("USvideos.csv")

# %%
print("First 5 rows: \n")
print(df.head())

# %%
print("Statistical description of data: ")
print(df.describe())

# %%
print(" info of data: ")
print(df.info())

# %%
print("\nShape of data:")
print(df.shape)

# %%
target_resgression = "views"
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
print("\n Histograms of views:\n")
plt.figure(figsize=(5,5))
sns.histplot(df["views"],bins=30)
plt.title("Distribution of Video Views")
plt.xlabel("Views")
plt.ylabel("Number of Videos")
plt.show()

# %%
# Scatter plot Likes vs Views
plt.figure(figsize=(8, 5))

sns.scatterplot(data=df, x="likes", y="views")

plt.title("Likes vs Views")
plt.xlabel("Likes")
plt.ylabel("Views")

plt.show()

# %%
df["title_length"] = df["title"].str.len()


# %%
df["trending_date"] = pd.to_datetime(
    df["trending_date"],
    format="%y.%d.%m"
)

df["publish_time"] = pd.to_datetime(
    df["publish_time"],
    utc=True
)

df["days_since_publish"] = (
    df["trending_date"] -
    df["publish_time"].dt.tz_localize(None)
).dt.days

# %%


# %%
print(df.columns.tolist())

# %%
correlation_columns = [
    "views",
    "likes",
    "dislikes",
    "comment_count",
    "title_length",
    "days_since_publish"
]

correlation_matrix = df[correlation_columns].corr()

print("\nCoorelation_matrix:\n",correlation_matrix)
plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Matrix")

plt.show()

# %%
print("""Observations: Views have a strong positive correlation with likes(0.795)
indicating that videos with higher number of likes have higher number of views.
Moderate positive correlation comment_count(0.575) and dislikes(0.51).
Title length (-0.05) and days_since publish (-0.026) show very weak correlation
with views in this dataset.""")

# %% [markdown]
# # Hypothesis Testing

# %%
from scipy.stats import ttest_ind

# %%
#Split the videos into high and low groups usingthe median
likes_median = df["likes"].median()
dislikes_median = df["dislikes"].median()
comments_median =df["comment_count"].median()

#Likes vs Views
high_likes_views = df.loc[df["likes"] > likes_median,"views"]
low_likes_views = df.loc[df["likes"] <= likes_median,"views"]

likes_ttest = ttest_ind(
    high_likes_views,
    low_likes_views,
    equal_var = False
)

#Dislikes vs Views
high_dislikes_views = df.loc[df["dislikes"] >dislikes_median,"views"]
low_dislikes_views = df.loc[df["dislikes"] <= dislikes_median,"views"]

dislikes_ttest = ttest_ind(
    high_dislikes_views,
    low_dislikes_views,
    equal_var = False
)

# Comment Count vs Views
high_comments_views = df.loc[df["comment_count"] > comments_median, "views"]
low_comments_views = df.loc[df["comment_count"] <= comments_median, "views"]

comments_ttest = ttest_ind(
    high_comments_views,
    low_comments_views,
    equal_var=False
)


# %%
print("Hypothesis testin result")
print("-" * 40)
print("Likes vs Views")
print('t-statistic:',likes_ttest.statistic)
print('p-value',likes_ttest.pvalue)
print("\nDislikes vs Views")
print("t-statistic:",dislikes_ttest.statistic)
print("p-value:",dislikes_ttest.pvalue)

print("\nCommnet count vs views")
print("t-statistics:",comments_ttest.statistic)
print("p-value",comments_ttest.pvalue)

# %%
alpha = 0.05

results = {
    "likes": likes_ttest.pvalue,
    "dislikes": dislikes_ttest.pvalue,
    "Comments": comments_ttest.pvalue
}
for feature,p_value in results.items():
    if p_value < alpha:
        print(f"{feature}: Reject H0 - statistically significant.")
    else:
         print(f"{feature}: Fail to reject H0 - not statistically significant.")

# %%
print("""Independent t-tests were performed to compare the views 
      of videos with high and low likes, dislikes, and comment counts. The p-values for all three features were 
      extremely small and below the significance level of 0.05. Therefore, the null hypothesis was rejected for likes, dislikes, and comment count.
      This indicates statistically significant differences in views between the high and low groups for all three engagement metrics.
      However, statistical significance does not imply causation""")

# %%



