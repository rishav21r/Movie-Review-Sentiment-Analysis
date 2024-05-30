import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# Function to analyze sentiment using TextBlob
def analyze_sentiment_textblob(reviews):
    reviews['Polarity'] = reviews['Content'].apply(lambda review: TextBlob(review).sentiment.polarity)
    reviews['Sentiment_Type'] = reviews['Polarity'].apply(
        lambda p: 'positive' if p > 0 else ('negative' if p < 0 else 'neutral'))
    return reviews

# Function to visualize sentiment analysis
def visualize_sentiment_analysis(results, title):
    # Sentiment Distribution (with custom colors)
    plt.figure(figsize=(10, 5))

    # Define a dictionary to map sentiment types to colors
    sentiment_colors = {'positive': 'palegreen', 'neutral': 'gold', 'negative': 'tomato'}

    # Use the palette argument to set colors based on sentiment_colors
    sns.countplot(x='Sentiment_Type', data=results, order=sentiment_colors.keys(),
                  palette=sentiment_colors)

    plt.title(f'Distribution of Sentiments for {title}')
    plt.xlabel('Sentiment Type')
    plt.ylabel('Count')

    # Add labels to each bar (count and percentage)
    for p in plt.gca().patches:
        height = p.get_height()
        percentage = f'{height / len(results) * 100:.1f}%'
        plt.gca().text(p.get_x() + p.get_width() / 2., height + 2, f'{height}\n({percentage})', ha="center",
                       va="bottom")

    plt.show()

    # Print sentiment type counts
    sentiment_counts = results['Sentiment_Type'].value_counts(normalize=True) * 100
    print(f"\nSentiment Distribution for {title}:")
    print(sentiment_counts)

    # Sentiment Score Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(results['Polarity'], kde=True, bins=30)
    plt.title(f'Distribution of Sentiment Scores for {title}')
    plt.xlabel('Polarity Score')
    plt.ylabel('Frequency')
    plt.show()

# Function to plot sentiment vs ratings
def plot_sentiment_vs_ratings(reviews, title):
    average_sentiment = reviews['Polarity'].mean()
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

# Function to process movie reviews
def process_movie_reviews(data_dir, filename, title):
    file_path = os.path.join(data_dir, filename)
    reviews = pd.read_csv(file_path)
    sentiment_reviews = analyze_sentiment_textblob(reviews)
    visualize_sentiment_analysis(sentiment_reviews, title)
    plot_sentiment_vs_ratings(sentiment_reviews, title)

# Define the data directory relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '../data')

# Define file paths and titles
file_paths_and_titles = [
    ('cleaned_imdbreviews_thelionking1994.csv', 'The Lion King (1994)'),
    ('cleaned_imdbreviews_saw2004.csv', 'Saw (2004)'),
    ('cleaned_imdbreviews_3idiots2009.csv', '3 Idiots (2009)')
]

# Process each movie review dataset
for filename, title in file_paths_and_titles:
    process_movie_reviews(data_dir, filename, title)
