import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class RevenueAnalysis:
    def __init__(self, filename):
        # Define the data directory relative to the script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '../data')
        self.filepath = os.path.join(data_dir, filename)
        self.data = None

    def load_data(self):
        """Load and prepare the data for analysis."""
        self.data = pd.read_csv(self.filepath)
        self.data.dropna(subset=['Gross_imdb', 'IMDB_Rating', 'Meta_score', 'tomatometer_rating', 'audience_rating'],
                         inplace=True)

    def plot_correlations_with_regression(self):
        """Visualize correlations with regression lines for enhanced impact."""
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # Changed to 1 row, 2 columns and adjusted figsize
        features = ['IMDB_Rating', 'Meta_score']
        titles = ['IMDb Rating', 'Meta Score']

        for i, (feature, title) in enumerate(zip(features, titles)):
            ax = axs[i]  # Simplified indexing since there is only one row
            sns.regplot(x=feature, y='Gross_imdb', data=self.data, ax=ax, scatter_kws={'alpha': 0.5})
            ax.set_title(f'{title} vs Gross Revenue')
            ax.set_xlabel(title)
            ax.set_ylabel('Gross Revenue ($)')
            ax.grid(True)

        plt.tight_layout()
        plt.show()

    def perform_and_plot_regression(self):
        """Perform regression and plot results with optional lowess smoothing."""
        try:
            import statsmodels
            lowess = True
        except ImportError:
            lowess = False
            print("statsmodels is not installed. Lowess smoothing will be disabled.")

        model = LinearRegression()
        features = ['IMDB_Rating', 'Meta_score']

        for feature in features:
            X = self.data[[feature]]
            y = self.data['Gross_imdb']
            model.fit(X, y)
            predictions = model.predict(X)
            residuals = y - predictions

            plt.figure(figsize=(6, 4))
            sns.residplot(x=predictions, y=residuals, lowess=lowess)
            plt.title(f'Residual Plot for {feature}')
            plt.xlabel('Predicted Values')
            plt.ylabel('Residuals')
            plt.grid(True)
            plt.show()

            print(f'Regression results for {feature}:')
            print(f'Coefficient: {model.coef_[0]:.2f}')
            print(f'Intercept: {model.intercept_:.2f}')
            print(f'R-squared: {r2_score(y, predictions):.4f}')

def main():
    analysis = RevenueAnalysis('cleaned_combined_data.csv')
    analysis.load_data()
    analysis.plot_correlations_with_regression()
    analysis.perform_and_plot_regression()

if __name__ == "__main__":
    main()
