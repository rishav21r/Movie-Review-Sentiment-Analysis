import pandas as pd
import os

class DataPreparer:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.imdb_data_path = os.path.join(base_directory, 'cleaned_imdb_top_1000.csv')
        self.rotten_tomatoes_data_path = os.path.join(base_directory, 'cleaned_rotten_tomatoes_movies_1.csv')
        self.output_data_path = os.path.join(base_directory, 'cleaned_combined_data.csv')

    def load_data(self):
        """Load datasets from CSV files."""
        self.imdb_data = pd.read_csv(self.imdb_data_path)
        self.rotten_tomatoes_data = pd.read_csv(self.rotten_tomatoes_data_path)
        print("Data loaded successfully.")

    def normalize_and_prepare_data(self):
        """Normalize IMDb ratings and prepare data by merging datasets."""
        self.imdb_data['IMDB_Rating'] = self.imdb_data['IMDB_Rating'] * 10
        self.imdb_data['platform'] = 'IMDb'
        self.rotten_tomatoes_data['platform'] = 'Rotten Tomatoes'
        self.imdb_data.rename(columns={'Series_Title': 'movie_title'}, inplace=True)
        self.imdb_data['movie_title_lower'] = self.imdb_data['movie_title'].str.lower()
        self.rotten_tomatoes_data['movie_title_lower'] = self.rotten_tomatoes_data['movie_title'].str.lower()
        self.combined_data = pd.merge(self.imdb_data, self.rotten_tomatoes_data, on='movie_title_lower', how='outer', suffixes=('_imdb', '_rt'))
        self.combined_data.rename(columns={'Gross': 'Gross_imdb'}, inplace=True)
        print("Data normalized and prepared.")

    def clean_and_save_data(self):
        """Clean the dataset by removing unnecessary columns and save the cleaned data."""
        columns_to_drop = ['Poster_Link', 'Certificate', 'Runtime', 'Overview', 'Star1', 'Star2', 'Star3', 'Star4',
                           'No_of_Votes', 'movie_title_lower', 'original_release_date', 'actors', 'streaming_release_date']
        cleaned_data = self.combined_data.drop(columns=columns_to_drop)
        simplified_data = cleaned_data[['movie_title_imdb', 'Released_Year', 'Genre', 'IMDB_Rating', 'Meta_score',
                                        'platform_imdb', 'movie_title_rt', 'tomatometer_rating', 'audience_rating',
                                        'platform_rt', 'Gross_imdb']]
        simplified_data.to_csv(self.output_data_path, index=False)
        print("Data cleaned and saved successfully.")

def main():
    base_directory = os.getcwd()
    data_preparer = DataPreparer(base_directory)
    data_preparer.load_data()
    data_preparer.normalize_and_prepare_data()
    data_preparer.clean_and_save_data()

if __name__ == "__main__":
    main()
