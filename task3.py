# Import necessary libraries for data analysis and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set a style for the plots for a professional look
sns.set_style('whitegrid')

# --- Helper Function for Robust Column Name Finding ---
# This function helps to find the correct column name in case it varies in the dataset.
def find_column_name(df, possible_names):
    """
    Checks for a list of possible column names and returns the first one found.
    If none are found, it raises a KeyError.
    """
    for name in possible_names:
        if name in df.columns:
            return name
    raise KeyError(f"None of the expected columns were found: {possible_names}")

# --- Step 1: Load and Clean the Dataset ---
# This part of the code prepares the data for visualization.
try:
    # Corrected path to the file on the Desktop.
    # The folder name 'task3_ Data Visualization' has a space, which is handled here.
    file_path = r"C:\Users\pc\Desktop\task3DataVisualization\imdbmoviesDataset.csv"
    df = pd.read_csv(file_path)
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: The 'imdb_movies.csv' file was not found.")
    print(f"Please make sure the file is in the correct path: {file_path}")
    exit()

# Handle missing values and convert data types.
missing_percentage = df.isnull().sum() / len(df) * 100
columns_to_drop = missing_percentage[missing_percentage > 50].index
df_cleaned = df.drop(columns=columns_to_drop, axis=1)

# --- Clean and standardize column names ---
try:
    # Finding the correct names for key columns using our helper function
    budget_col = find_column_name(df_cleaned, ['budget_x', 'Budget'])
    revenue_col = find_column_name(df_cleaned, ['revenue', 'gross'])
    score_col = find_column_name(df_cleaned, ['score', 'imdb_score'])
    date_col = find_column_name(df_cleaned, ['date_x', 'release_date'])
    genre_col = find_column_name(df_cleaned, ['genre', 'genres'])
    title_col = find_column_name(df_cleaned, ['names', 'title'])

    print(f"Found column names: budget={budget_col}, revenue={revenue_col}, score={score_col}, date={date_col}, genre={genre_col}, title={title_col}")

except KeyError as e:
    print(f"Error: {e}")
    print("Please check your CSV file for the correct column names.")
    exit()

# Define a function to clean monetary columns by removing '$' and ','
def clean_money_column(column):
    if pd.isna(column):
        return np.nan
    try:
        cleaned_value = float(str(column).replace('$', '').replace(',', ''))
        return cleaned_value
    except ValueError:
        return np.nan

# Apply the cleaning function to revenue and budget
if revenue_col:
    df_cleaned[revenue_col] = df_cleaned[revenue_col].apply(clean_money_column)
    df_cleaned[revenue_col].fillna(df_cleaned[revenue_col].mean(), inplace=True)
if budget_col:
    df_cleaned[budget_col] = df_cleaned[budget_col].apply(clean_money_column)
    df_cleaned[budget_col].fillna(df_cleaned[budget_col].mean(), inplace=True)


# --- Step 2: Create Visualizations ---
# Each visual helps to tell a part of the data story.

# Visualization 1: Top 10 Most Popular Movie Genres
if genre_col and title_col:
    all_genres = df_cleaned[genre_col].str.split(', ').explode().str.strip()
    genre_counts = all_genres.value_counts().head(10)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
    plt.title('Top 10 Most Popular Movie Genres', fontsize=16)
    plt.xlabel('Number of Movies', fontsize=12)
    plt.ylabel('Genre', fontsize=12)
    plt.tight_layout()
    plt.show()

# Visualization 2: Relationship between Budget and Revenue
if budget_col and revenue_col:
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=budget_col, y=revenue_col, data=df_cleaned, alpha=0.6, color='salmon')
    plt.title('Relationship between Budget and Revenue', fontsize=16)
    plt.xlabel('Budget ($)', fontsize=12)
    plt.ylabel('Revenue ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

# Visualization 3: Average IMDb Score Over the Years
if date_col and score_col:
    try:
        df_cleaned['year'] = pd.to_datetime(df_cleaned[date_col], errors='coerce').dt.year
        avg_score_by_year = df_cleaned.groupby('year')[score_col].mean().reset_index()

        plt.figure(figsize=(12, 8))
        sns.lineplot(x='year', y=score_col, data=avg_score_by_year, marker='o', color='teal')
        plt.title('Average IMDb Score Over the Years', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Average Score', fontsize=12)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error plotting line chart: {e}")

print("\nAll visualizations have been generated successfully.")



