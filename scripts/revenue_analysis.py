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

    def plot_correlations_with_regression(self, color='blue'):
        """Visualize correlations with regression lines for enhanced impact."""
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))
        features = ['IMDB_Rating', 'Meta_score']
        titles = ['IMDb Rating', 'Meta Score']

        for i, (feature, title) in enumerate(zip(features, titles)):
            ax = axs[i]
            sns.regplot(x=feature, y='Gross_imdb', data=self.data, ax=ax, scatter_kws={'alpha': 0.5}, color=color)
            ax.set_title(f'{title} vs Gross Revenue')
            ax.set_xlabel(title)
            ax.set_ylabel('Gross Revenue ($)')
            ax.grid(True)

        plt.tight_layout()
        plt.show()

    def perform_and_plot_regression(self, color='blue'):
        """Perform regression and plot results with optional lowess smoothing."""
        try:
            import statsmodels
            lowess = True
        except ImportError:
            lowess = False
            print("statsmodels is not installed. Lowess smoothing will be disabled.")

        model = LinearRegression()
        features = ['IMDB_Rating', 'Meta_score']

        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        for i, feature in enumerate(features):
            X = self.data[[feature]]
            y = self.data['Gross_imdb']
            model.fit(X, y)
            predictions = model.predict(X)
            residuals = y - predictions

            sns.residplot(x=predictions, y=residuals, lowess=lowess, color=color, ax=axs[i])
            axs[i].set_title(f'Residual Plot for {feature}')
            axs[i].set_xlabel('Predicted Values')
            axs[i].set_ylabel('Residuals')
            axs[i].grid(True)

            print(f'Regression results for {feature}:')
            print(f'Coefficient: {model.coef_[0]:.2f}')
            print(f'Intercept: {model.intercept_:.2f}')
            print(f'R-squared: {r2_score(y, predictions):.4f}')

        plt.tight_layout()
        plt.show()

def main():
    analysis = RevenueAnalysis('cleaned_combined_data.csv')
    analysis.load_data()
    analysis.plot_correlations_with_regression(color='green')  # Change color as needed
    analysis.perform_and_plot_regression(color='orange')  # Change color as needed

if __name__ == "__main__":
    main()
