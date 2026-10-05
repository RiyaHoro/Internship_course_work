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
# H₀: There is no significant difference in views between the high and low groups.
# 
# H₁: There is a significant difference in views between the high and low groups.

# %%
from scipy.stats import ttest_ind

# %%
#Split the videos into high and low groups using the median
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
print("Hypothesis testing result")
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
print("""The t-tests found statistically significant differences in views between the high and low groups for likes, 
      dislikes, and comment count.
      In each case, the high-engagement group had higher average views than the low-engagement group. 
      These results indicate an association between engagement metrics and views, but do not establish causation.""")

# %% [markdown]
# # Preprocess Features
# 

# %%
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Numerical features
numeric_features = [
    "likes",
    "dislikes",
    "comment_count",
    "title_length",
    "days_since_publish"
]

# Categorical features
categorical_features = [
    "channel_title",
    "category_id"
]

# All input features
features = numeric_features + categorical_features

# Input data
X = df[features]

# Targets
y_reg = df["views"]
y_cls = df["viral"]

# Split into training and testing data
X_train, X_test, y_reg_train, y_reg_test, y_cls_train, y_cls_test = train_test_split(
    X,
    y_reg,
    y_cls,
    test_size=0.2,
    random_state=42,
    stratify=y_cls
)

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# Fit on training data and transform it
X_train_processed = preprocessor.fit_transform(X_train)

# Only transform test data
X_test_processed = preprocessor.transform(X_test)

print("Original training shape:", X_train.shape)
print("Original testing shape:", X_test.shape)

print("Processed training shape:", X_train_processed.shape)
print("Processed testing shape:", X_test_processed.shape)

# %%


# %% [markdown]
# # Train linear regression model 

# %%
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Create Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train_processed, y_reg_train)

# Predict views for test data
y_pred = model.predict(X_test_processed)

# Calculate metrics
mse = mean_squared_error(y_reg_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_reg_test, y_pred)
r2 = r2_score(y_reg_test, y_pred)

print("Linear Regression Results")
print("-" * 30)
print("MSE :", mse)
print("RMSE:", rmse)
print("MAE :", mae)
print("R²  :", r2)

# %%
#feature coefficients
feature_names = preprocessor.get_feature_names_out()

coefficients = model.coef_

feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

# Absolute value helps identify strongest features
feature_importance["Absolute_Coefficient"] = (
    feature_importance["Coefficient"].abs()
)

feature_importance = feature_importance.sort_values(
    "Absolute_Coefficient",
    ascending=False
)

print("Top 15 Features:")
print(feature_importance.head(15))

# %%
top_features = feature_importance.head(15)

plt.figure(figsize=(10, 6))

plt.barh(
    top_features["Feature"],
    top_features["Absolute_Coefficient"]
)

plt.xlabel("Absolute Coefficient")
plt.ylabel("Feature")
plt.title("Top 15 Features Influencing Views")

plt.gca().invert_yaxis()

plt.show()

# %%
print("""Linear Regression was used to predict video views. The model was evaluated using MSE, RMSE, MAE and R². 
      The coefficient analysis shows which features have the strongest influence on predicted views.
      Features with larger absolute coefficients have greater influence, 
      while the sign of the coefficient indicates whether the relationship is positive or negative.""")

# %% [markdown]
# # Task 6 . Logistic Regression

# %%
from sklearn.linear_model import LogisticRegression

# Create Logistic Regression model
log_model = LogisticRegression(max_iter=1000)

# Train the model
log_model.fit(X_train_processed, y_cls_train)

# Predict 0 or 1
y_cls_pred = log_model.predict(X_test_processed)

# Predict probability of being viral
y_cls_prob = log_model.predict_proba(X_test_processed)[:, 1]

# %%
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

accuracy = accuracy_score(y_cls_test, y_cls_pred)
precision = precision_score(y_cls_test, y_cls_pred)
recall = recall_score(y_cls_test, y_cls_pred)
f1 = f1_score(y_cls_test, y_cls_pred)
roc_auc = roc_auc_score(y_cls_test, y_cls_prob)

print("Logistic Regression Results")
print("-" * 35)
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1-score :", f1)
print("ROC-AUC  :", roc_auc)

# %%
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_cls_test, y_cls_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Non-Viral", "Viral"]
)

disp.plot()

plt.title("Confusion Matrix")
plt.show()

# %%
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(
    y_cls_test,
    y_cls_prob
)

plt.figure(figsize=(8, 6))

plt.plot(
    fpr,
    tpr,
    label=f"ROC-AUC = {roc_auc:.3f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.show()

# %%
feature_names = preprocessor.get_feature_names_out()

log_coefficients = log_model.coef_[0]

log_feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": log_coefficients
})

log_feature_importance["Absolute_Coefficient"] = (
    log_feature_importance["Coefficient"].abs()
)

log_feature_importance = log_feature_importance.sort_values(
    "Absolute_Coefficient",
    ascending=False
)

print("Top 15 Features Influencing Virality:")
print(log_feature_importance.head(15))

# %%
# Features importance plot
top_features = log_feature_importance.head(15)

plt.figure(figsize=(10, 6))

plt.barh(
    top_features["Feature"],
    top_features["Absolute_Coefficient"]
)

plt.xlabel("Absolute Coefficient")
plt.ylabel("Feature")
plt.title("Top 15 Features Influencing Virality")

plt.gca().invert_yaxis()

plt.show()


# %%
print("""The Logistic Regression model was evaluated using accuracy, precision, 
      , F1-score and ROC-AUC. The coefficient analysis shows that [feature names] 
      had the strongest influence on the prediction of video virality.
      Positive coefficients indicate an association with higher viral probability,
      while negative coefficients indicate an association with lower viral probability. """)


