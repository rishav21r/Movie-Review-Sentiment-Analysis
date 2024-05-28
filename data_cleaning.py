import os
import pandas as pd

# Print the current working directory
print("Current Working Directory:", os.getcwd())


# Function to Clean and Preprocess 'imdb_top_1000.csv' & 'rotten_tomatoes_movies_1.csv'
def clean_dataset(file_path):
    # Load the dataset
    try:
        data = pd.read_csv(file_path)
        print(f"Loaded dataset: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        # List files in the directory you believe contains your file
        print("Files in the current directory:", os.listdir('.'))
        raise

    # Specific cleaning steps for each dataset based on known structure
    if 'imdb_top_1000.csv' in file_path:
        # Fill missing 'Meta_score' with the median of the column
        data['Meta_score'].fillna(data['Meta_score'].median(), inplace=True)
        # For 'Certificate', use the most common certificate if not specified
        data['Certificate'].fillna(data['Certificate'].mode()[0], inplace=True)
        # Convert 'Gross' to numeric, removing non-numeric characters
        data['Gross'] = data['Gross'].replace(r'[\$,]', '', regex=True).astype(float)
        data['Gross'].fillna(data['Gross'].median(), inplace=True)
        data['IMDB_Rating'] = data['IMDB_Rating'].astype(float)

    elif 'rotten_tomatoes_movies_1.csv' in file_path:
        # Fill missing values in 'tomatometer_rating' and 'audience_rating'
        data['tomatometer_rating'].fillna(data['tomatometer_rating'].median(), inplace=True)
        data['audience_rating'].fillna(data['audience_rating'].median(), inplace=True)
        # Convert date fields to datetime
        data['original_release_date'] = pd.to_datetime(data['original_release_date'], errors='coerce')
        data['streaming_release_date'] = pd.to_datetime(data['streaming_release_date'], errors='coerce')

    # Save cleaned dataset
    cleaned_path = 'cleaned_' + os.path.basename(file_path)
    data.to_csv(cleaned_path, index=False)
    print(f"Cleaned data saved to: {cleaned_path}")

    return data


# List of files to clean
files = [
    'imdb_top_1000.csv',
    'rotten_tomatoes_movies_1.csv',
]

# Apply cleaning to all datasets
for file in files:
    clean_dataset(file)
