import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, pearsonr, linregress


class ComparativeAnalysis:
    def __init__(self, filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data')
        self.filepath = os.path.join(data_dir, filename)

    def load_data(self):
        self.data = pd.read_csv(self.filepath)
        self.data.dropna(subset=['IMDB_Rating', 'tomatometer_rating', 'audience_rating'], inplace=True)

    def plot_average_ratings(self):
        rating_comparison_data = self.data[['IMDB_Rating', 'Meta_score', 'tomatometer_rating', 'audience_rating']]
        rating_comparison_data.columns = ['IMDb Rating', 'IMDb Meta Score', 'Tomatometer Rating', 'Audience Rating']
        # Define Custom Colors
        colors = ["mediumslateblue", "forestgreen", "tomato", "gold"]  # One color for each category
        plt.figure(figsize=(10, 6))
        barplot = sns.barplot(data=rating_comparison_data.melt(var_name='Rating Type', value_name='Score'),
                              x='Rating Type', y='Score', errorbar=None, palette=colors)
        # Add Value Labels to Bars (optional)
        for p in barplot.patches:
            barplot.annotate(format(p.get_height(), '.2f'),
                             (p.get_x() + p.get_width() / 2., p.get_height()),
                             ha='center', va='center',
                             xytext=(0, 9),
                             textcoords='offset points')

        plt.title('Average Ratings Comparison')
        plt.ylabel('Average Score')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def perform_statistical_tests(self):
        t_stat, p_value = ttest_ind(self.data['Meta_score'], self.data['tomatometer_rating'])
        imdb_rt_correlation, _ = pearsonr(self.data['IMDB_Rating'], self.data['audience_rating'])
        meta_tomato_correlation, _ = pearsonr(self.data['Meta_score'], self.data['tomatometer_rating'])

        means = self.data[['Meta_score', 'tomatometer_rating']].mean()
        errors = self.data[['Meta_score', 'tomatometer_rating']].std()
        plt.figure(figsize=(8, 5))
        means.plot.bar(yerr=errors, capsize=4)
        plt.title('Mean Critic Scores with Error Bars')
        plt.ylabel('Score')

        # Correct x-axis labels cut off:
        plt.xticks(rotation=0, ha="center")
        plt.tight_layout()  # Adjust layout to prevent overlapping

        plt.show()

        fig, ax = plt.subplots(1, 2, figsize=(16, 6))
        # Customize Colors
        imdb_color = 'coral'  # Choose your desired color
        meta_color = 'coral'  # Choose your desired
        sns.regplot(x='IMDB_Rating', y='audience_rating', data=self.data, ax=ax[0], scatter_kws={'color': imdb_color}, line_kws={'color': imdb_color})  # Added color arguments
        ax[0].set_title('Correlation between IMDb Ratings and RT Audience Ratings')
        sns.regplot(x='Meta_score', y='tomatometer_rating', data=self.data, ax=ax[1], scatter_kws={'color': meta_color}, line_kws={'color': meta_color})  # Added color arguments
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
