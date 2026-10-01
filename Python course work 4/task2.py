import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


DATASET_PATH = r"D:\Python Course work\courseWork4\Sport car price.csv"
OUTPUT_PATH = "cleaned_sports_car_prices.csv"


# 1. Load dataset
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df


def get_first_five_rows(df):
    return df.head(5)


# 2. Clean dataset
def clean_dataset(df):
    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows with missing values
    df = df.dropna()

    # Convert numeric columns to numeric data
    numeric_columns = [
        "Year",
        "Engine Size (L)",
        "Horsepower",
        "Torque (lb-ft)",
        "0-60 MPH Time (seconds)",
        "Price (in USD)"
    ]

    for column in numeric_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("L", "", regex=False)
            .str.strip()
        )

        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove rows that became missing after conversion
    df = df.dropna()

    return df


# 3. Calculate summary statistics
def calculate_summary_statistics(df):
    statistics = {}

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):

            statistics[column] = {
                "Mean": df[column].mean(),
                "Median": df[column].median(),
                "Mode": df[column].mode().iloc[0],
                "Standard Deviation": df[column].std(),
                "Range": df[column].max() - df[column].min()
            }

    return pd.DataFrame(statistics).T


# 4. Average price for each car make
def calculate_average_price_by_make(df):
    result = df.groupby("Car Make")["Price (in USD)"].mean()

    return result


# 5. Average horsepower for each year
def calculate_average_horsepower_by_year(df):
    result = df.groupby("Year")["Horsepower"].mean()

    return result


# 6. Scatter plot with linear regression line
def create_price_horsepower_plot(df):

    x = df["Horsepower"].to_numpy()
    y = df["Price (in USD)"].to_numpy()

    # Calculate regression coefficients
    coefficients = np.polyfit(x, y, 1)

    # Create regression equation
    regression_line = np.poly1d(coefficients)

    # Generate x values for the regression line
    x_line = np.linspace(x.min(), x.max(), 100)

    # Calculate predicted y values
    y_line = regression_line(x_line)

    # Create scatter plot
    plt.figure(figsize=(8, 5))

    plt.scatter(x, y, alpha=0.7)
    plt.plot(x_line, y_line)

    plt.xlabel("Horsepower")
    plt.ylabel("Price (USD)")
    plt.title("Price vs Horsepower")
    plt.grid(True)

    plt.show()

    return coefficients


# 7. Histogram of 0-60 MPH times
def create_acceleration_histogram(df):

    minimum = np.floor(df["0-60 MPH Time (seconds)"].min())
    maximum = np.ceil(df["0-60 MPH Time (seconds)"].max())

    bins = np.arange(minimum, maximum + 0.5, 0.5)

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["0-60 MPH Time (seconds)"],
        bins=bins,
        edgecolor="black"
    )

    plt.xlabel("0-60 MPH Time (seconds)")
    plt.ylabel("Number of Cars")
    plt.title("Distribution of 0-60 MPH Times")
    plt.grid(axis="y")

    plt.show()

    return bins


# 8. Filter cars with price greater than $500,000
def filter_expensive_cars(df):

    result = df[df["Price (in USD)"] > 500000]

    result = result.sort_values(
        by="Horsepower",
        ascending=False
    )

    return result


# 9. Export cleaned dataset
def export_cleaned_dataset(df, file_path):

    df.to_csv(file_path, index=False)

    return file_path


# Main program
if __name__ == "__main__":

    
    df = load_dataset(DATASET_PATH)

    print("\n1. FIRST 5 ROWS")
    print(get_first_five_rows(df))


    
    cleaned_df = clean_dataset(df)

    print("\n2. CLEANED DATASET")
    print(cleaned_df.head())

    summary = calculate_summary_statistics(cleaned_df)

    print("\n3. SUMMARY STATISTICS")
    print(summary)

    average_price = calculate_average_price_by_make(cleaned_df)

    print("\n4. AVERAGE PRICE BY CAR MAKE")
    print(average_price)
    
    average_horsepower = calculate_average_horsepower_by_year(cleaned_df)

    print("\n5. AVERAGE HORSEPOWER BY YEAR")
    print(average_horsepower)

    regression_coefficients = create_price_horsepower_plot(cleaned_df)

    print("\n6. LINEAR REGRESSION COEFFICIENTS")
    print(regression_coefficients)

    histogram_bins = create_acceleration_histogram(cleaned_df)

    print("\n7. HISTOGRAM BINS")
    print(histogram_bins)

    expensive_cars = filter_expensive_cars(cleaned_df)

    print("\n8. CARS WITH PRICE GREATER THAN $500,000")
    print(expensive_cars)

    output_file = export_cleaned_dataset(
        cleaned_df,
        OUTPUT_PATH
    )

    print("\n9. CLEANED DATASET EXPORTED")
    print("File:", output_file)