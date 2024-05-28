import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    def __init__(self, filename):
        # Define the data directory relative to the script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data')
        self.data_path = os.path.join(data_dir, filename)

    def load_data(self):
        """ Load data from a CSV file """
        return pd.read_csv(self.data_path)

    def plot_histograms(self, data):
        """ Plot histograms with KDE for all ratings """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.histplot(data['IMDB_Rating'], kde=True, color='blue', bins=20, ax=axes[0, 0])
        axes[0, 0].set_title('Histogram of IMDb Ratings')
        sns.histplot(data['Meta_score'], kde=True, color='green', bins=20, ax=axes[0, 1])
        axes[0, 1].set_title('Histogram of IMDb Meta Scores')
        sns.histplot(data['tomatometer_rating'], kde=True, color='red', bins=20, ax=axes[1, 0])
        axes[1, 0].set_title('Histogram of Tomatometer Ratings')
        sns.histplot(data['audience_rating'], kde=True, color='orange', bins=20, ax=axes[1, 1])
        axes[1, 1].set_title('Histogram of Audience Ratings')
        plt.tight_layout()
        plt.show()

    def plot_cdf(self, data):
        """ Plot CDF for all types of ratings """
        plt.figure(figsize=(14, 7))
        sns.ecdfplot(data['IMDB_Rating'], label='IMDb Rating', color='blue')
        sns.ecdfplot(data['Meta_score'], label='Meta Score', color='green')
        sns.ecdfplot(data['tomatometer_rating'], label='Tomatometer Rating', color='red')
        sns.ecdfplot(data['audience_rating'], label='Audience Rating', color='orange')
        plt.title('CDF of All Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Cumulative Probability')
        plt.legend()
        plt.show()

    def plot_violin(self, data):
        """ Plot violin plots for all ratings """
        plt.figure(figsize=(12, 6))
        ratings_data = data[['IMDB_Rating', 'Meta_score', 'tomatometer_rating', 'audience_rating']].dropna()
        sns.violinplot(data=ratings_data)
        plt.title('Violin Plots of All Ratings')
        plt.ylabel('Rating')
        plt.show()

    def plot_yearly_trends(self, data):
        """ Plot the yearly trends for all types of ratings """
        plt.figure(figsize=(14, 7))
        data['Released_Year'] = pd.to_numeric(data['Released_Year'], errors='coerce')
        yearly_data = data.groupby('Released_Year').agg({
            'IMDB_Rating': 'mean',
            'Meta_score': 'mean',
            'tomatometer_rating': 'mean',
            'audience_rating': 'mean'
        }).dropna()
        sns.lineplot(data=yearly_data)
        plt.title('Yearly Trends in All Ratings')
        plt.xlabel('Year')
        plt.ylabel('Average Rating')
        plt.legend(['IMDb Rating', 'Meta Score', 'Tomatometer Rating', 'Audience Rating'])
        plt.show()

    def plot_pairwise_comparisons(self, data):
        """ Plot pairwise ratings comparisons for all combinations """
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))

        # IMDb Rating vs. Other Scores
        sns.scatterplot(x='IMDB_Rating', y='Meta_score', data=data, ax=axes[0, 0], alpha=0.6)
        axes[0, 0].set_title('IMDb Ratings vs. Meta Scores')

        sns.scatterplot(x='IMDB_Rating', y='tomatometer_rating', data=data, ax=axes[0, 1], alpha=0.6)
        axes[0, 1].set_title('IMDb Ratings vs. Tomatometer Ratings')

        sns.scatterplot(x='IMDB_Rating', y='audience_rating', data=data, ax=axes[0, 2], alpha=0.6)
        axes[0, 2].set_title('IMDb Ratings vs. Audience Ratings')

        # Meta Score vs. Other Ratings
        sns.scatterplot(x='Meta_score', y='tomatometer_rating', data=data, ax=axes[1, 0], alpha=0.6)
        axes[1, 0].set_title('Meta Scores vs. Tomatometer Ratings')

        sns.scatterplot(x='Meta_score', y='audience_rating', data=data, ax=axes[1, 1], alpha=0.6)
        axes[1, 1].set_title('Meta Scores vs. Audience Ratings')

        # Tomatometer Rating vs. Audience Rating
        sns.scatterplot(x='tomatometer_rating', y='audience_rating', data=data, ax=axes[1, 2], alpha=0.6)
        axes[1, 2].set_title('Tomatometer Ratings vs. Audience Ratings')

        plt.tight_layout()
        plt.show()

def main():
    analysis = DataAnalysis('cleaned_combined_data.csv')
    data = analysis.load_data()
    analysis.plot_histograms(data)
    analysis.plot_cdf(data)
    analysis.plot_violin(data)
    analysis.plot_yearly_trends(data)
    analysis.plot_pairwise_comparisons(data)

if __name__ == "__main__":
    main()
