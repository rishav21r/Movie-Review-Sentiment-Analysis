import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')


def analyze_sentiment_vader(reviews):
    sid = SentimentIntensityAnalyzer()
    reviews['Scores'] = reviews['Content'].apply(lambda review: sid.polarity_scores(review))
    reviews['Compound'] = reviews['Scores'].apply(lambda score_dict: score_dict['compound'])
    reviews['Sentiment_Type'] = reviews['Compound'].apply(
        lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    return reviews


def visualize_sentiment_analysis(results, title):
    # Sentiment Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(x='Sentiment_Type', data=results, order=['positive', 'neutral', 'negative'])
    plt.title(f'Distribution of Sentiments for {title}')
    plt.xlabel('Sentiment Type')
    plt.ylabel('Count')
    plt.show()

    # Print sentiment type counts
    sentiment_counts = results['Sentiment_Type'].value_counts(normalize=True) * 100
    print(f"\nSentiment Distribution for {title}:")
    print(sentiment_counts)

    # Sentiment Score Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(results['Compound'], kde=True, bins=30)
    plt.title(f'Distribution of Sentiment Scores for {title}')
    plt.xlabel('Compound Score')
    plt.ylabel('Frequency')
    plt.show()


def plot_sentiment_vs_ratings(reviews, title):
    average_sentiment = reviews['Compound'].mean()
    average_rating = reviews['Rating'].mean()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=[average_sentiment], y=[average_rating])
    plt.title(f'Correlation between Sentiment Scores and Ratings for {title}')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Average Movie Rating')
    plt.grid(True)
    plt.show()

    # Print average sentiment and rating
    print(f"\nAverage Sentiment Score for {title}: {average_sentiment:.2f}")
    print(f"Average Rating for {title}: {average_rating:.2f}")


def process_movie_reviews(data_dir, filename, title):
    file_path = os.path.join(data_dir, filename)
    reviews = pd.read_csv(file_path)
    sentiment_reviews = analyze_sentiment_vader(reviews)
    visualize_sentiment_analysis(sentiment_reviews, title)
    plot_sentiment_vs_ratings(sentiment_reviews, title)


# Define the data directory relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '../data')

# List of movie
