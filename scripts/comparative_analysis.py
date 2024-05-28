import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, pearsonr, linregress

class ComparativeAnalysis:
    def __init__(self, filename):
        # Define the data directory relative to the script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data')
        self.filepath = os.path.join(data_dir, filename)

    def load_data(self):
        """Load the combined dataset."""
        self.data = pd.read_csv(self.filepath)
        self.data.dropna(subset=['IMDB_Rating', 'tomatometer_rating', 'audience_rating'], inplace=True)

    def plot_average_ratings(self):
        """Visualize the average ratings by type."""
        rating_comparison_data = self.data[['IMDB_Rating', 'Meta_score', 'tomatometer_rating', 'audience_rating']]
        rating_comparison_data.columns = ['IMDb Rating', 'IMDb Meta Score', 'Tomatometer Rating', 'Audience Rating']
        plt.figure(figsize=(10, 6))
        sns.barplot(data=rating_comparison_data.melt(var_name='Rating Type', value_name='Score'),
                    x='Rating Type', y='Score', errorbar=None)
        plt.title('Average Ratings Comparison')
        plt.ylabel('Average Score')
        plt.xticks(rotation=45)
        plt.show()

    def perform_statistical_tests(self):
        """Perform t-tests and correlation analysis with visual output."""
        t_stat, p_value = ttest_ind(self.data['Meta_score'], self.data['tomatometer_rating'])
        imdb_rt_correlation, _ = pearsonr(self.data['IMDB_Rating'], self.data['audience_rating'])
        meta_tomato_correlation, _ = pearsonr(self.data['Meta_score'], self.data['tomatometer_rating'])

        # Visualizing the mean scores with error bars for t-test
        means = self.data[['Meta_score', 'tomatometer_rating']].mean()
        errors = self.data[['Meta_score', 'tomatometer_rating']].std()
        plt.figure(figsize=(8, 5))
        means.plot.bar(yerr=errors, capsize=4)
        plt.title('Mean Critic Scores with Error Bars')
        plt.ylabel('Score')
        plt.show()

        # Correlation visualizations with regression lines
        fig, ax = plt.subplots(1, 2, figsize=(16, 6))
        sns.regplot(x='IMDB_Rating', y='audience_rating', data=self.data, ax=ax[0])
        ax[0].set_title('Correlation between IMDb Ratings and RT Audience Ratings')
        sns.regplot(x='Meta_score', y='tomatometer_rating', data=self.data, ax=ax[1])
        ax[1].set_title('Correlation between IMDb Meta Scores and RT Tomatometer Ratings')
        plt.tight_layout()
        plt.show()

        print(f"T-statistic: {t_stat}, P-value: {p_value}")
        print(f"Correlation between IMDb Ratings and RT Audience Ratings: {imdb_rt_correlation}")
        print(f"Correlation between IMDb Meta Scores and RT Tomatometer Ratings: {meta_tomato_correlation}")

def main():
    analysis = ComparativeAnalysis('cleaned_combined_data.csv')
    analysis.load_data()
    analysis.plot_average_ratings()
    analysis.perform_statistical_tests()

if __name__ == "__main__":
    main()
