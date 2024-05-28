import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ContentRatingProfitability:
    def __init__(self, filename):
        # Define the data directory relative to the script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data')
        self.filepath = os.path.join(data_dir, filename)

    def load_data(self):
        """Load the dataset and ensure necessary data is present."""
        self.data = pd.read_csv(self.filepath)
        self.data.dropna(subset=['Gross_imdb', 'IMDB_Rating'], inplace=True)

    def categorize_and_analyze(self):
        """Categorize IMDb ratings and calculate average gross revenue for each category."""
        # Define rating categories based on the distribution of IMDb ratings
        self.data['Rating_Category'] = pd.cut(self.data['IMDB_Rating'],
                                              bins=[75, 80, 85, 90, 100],
                                              labels=['76 to 80', '81 to 85', '86 to 90', 'Above 90'])
        # Calculate average gross revenue per rating category
        profitability = self.data.groupby('Rating_Category')['Gross_imdb'].mean().sort_values(ascending=False)
        return profitability

    def plot_profitability(self, profitability):
        """Visualize the average gross revenue across different IMDb rating categories."""
        plt.figure(figsize=(10, 6))
        sns.barplot(x=profitability.index, y=profitability.values, palette='viridis')
        plt.title('Average Gross Revenue by IMDb Rating Category')
        plt.xlabel('IMDb Rating Category')
        plt.ylabel('Average Gross Revenue ($)')
        plt.show()

def main():
    # Initialize the analysis with the path to the dataset
    analysis = ContentRatingProfitability('cleaned_combined_data.csv')
    analysis.load_data()
    profitability = analysis.categorize_and_analyze()
    analysis.plot_profitability(profitability)
    print(profitability)

if __name__ == "__main__":
    main()
