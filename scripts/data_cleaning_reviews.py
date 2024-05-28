import os
import pandas as pd

def clean_and_process_data():
    # Define the data directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '../data')

    # Paths to the data files
    path_saw = os.path.join(data_dir, 'imdbreviews_saw2004.csv')
    path_3idiots = os.path.join(data_dir, 'imdbreviews_3idiots2009.csv')
    path_lionking = os.path.join(data_dir, 'imdbreviews_thelionking1994.csv')

    # Load the datasets
    data_saw = pd.read_csv(path_saw)
    data_3idiots = pd.read_csv(path_3idiots)
    data_lionking = pd.read_csv(path_lionking)

    # Convert 'Rating' from '9/10' format to numeric for The Lion King 1994 dataset
    data_lionking['Rating'] = data_lionking['Rating'].str.split('/').str[0].astype(float)

    # Remove rows with missing values from all datasets
    data_saw_clean = data_saw.dropna()
    data_3idiots_clean = data_3idiots.dropna()
    data_lionking_clean = data_lionking.dropna()

    # Write the cleaned data back to new CSV files
    data_saw_clean.to_csv(os.path.join(data_dir, 'cleaned_imdbreviews_saw2004.csv'), index=False)
    data_3idiots_clean.to_csv(os.path.join(data_dir, 'cleaned_imdbreviews_3idiots2009.csv'), index=False)
    data_lionking_clean.to_csv(os.path.join(data_dir, 'cleaned_imdbreviews_thelionking1994.csv'), index=False)

    # Return the cleaned data
    return data_saw_clean, data_3idiots_clean, data_lionking_clean

# Clean the data
cleaned_data_saw, cleaned_data_3idiots, cleaned_data_lionking = clean_and_process_data()

# Print the number of entries for each dataset
print(f"Saw (2004): {cleaned_data_saw.shape[0]} entries.")
print(f"3 Idiots (2009): {cleaned_data_3idiots.shape[0]} entries.")
print(f"The Lion King (1994): {cleaned_data_lionking.shape[0]} entries.")
