import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the data directory relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '../data')

# Load the CSV file into a DataFrame
imdb_top_1000_path = os.path.join(data_dir, 'cleaned_imdb_top_1000.csv')
imdb_top_1000 = pd.read_csv(imdb_top_1000_path)

''' __Distribution of IMDb Ratings__ '''
sns.set(style="whitegrid")

# Plotting the distribution of IMDb ratings
plt.figure(figsize=(10, 6))
sns.histplot(imdb_top_1000['IMDB_Rating'], bins=20, kde=True, color='blue')
plt.title('Distribution of IMDb Ratings for Top 1000 Movies')
plt.xlabel('IMDb Rating')
plt.ylabel('Frequency')
plt.show()

''' __Meta Score Distribution__ '''
# Plotting the distribution of Meta scores
plt.figure(figsize=(10, 6))
sns.histplot(imdb_top_1000['Meta_score'], bins=20, kde=True, color='purple')
plt.title('Distribution of Meta Scores for Top 1000 Movies')
plt.xlabel('Meta Score')
plt.ylabel('Frequency')
plt.show()

''' __Genre Analysis__ '''
imdb_top_1000['Primary_Genre'] = imdb_top_1000['Genre'].apply(lambda x: x.split(',')[0].strip())

plt.figure(figsize=(12, 8))
genre_counts = imdb_top_1000['Primary_Genre'].value_counts()
sns.barplot(x=genre_counts.index, y=genre_counts.values, palette='viridis')
plt.xticks(rotation=45)
plt.title('Number of Movies by Primary Genre in Top 1000')
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.show()

''' __Yearly Trends__ '''
imdb_top_1000['Released_Year'] = pd.to_numeric(imdb_top_1000['Released_Year'], errors='coerce')
yearly_trends = imdb_top_1000.groupby('Released_Year')['IMDB_Rating'].mean()

plt.figure(figsize=(14, 7))
sns.lineplot(x=yearly_trends.index, y=yearly_trends.values, color='green')
plt.title('Average IMDb Rating by Release Year')
plt.xlabel('Year')
plt.ylabel('Average IMDb Rating')
plt.show()

''' __Director Analysis__ '''
top_directors = imdb_top_1000['Director'].value_counts().head(10)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='coolwarm', orient='h')
plt.title('Top 10 Directors with Most Movies in Top 1000')
plt.xlabel('Number of Movies')
plt.ylabel('Director')
plt.show()

''' __Relationship between Gross Revenue and Ratings__ '''
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Gross', y='IMDB_Rating', data=imdb_top_1000, color='red', label='IMDb Rating')
sns.scatterplot(x='Gross', y='Meta_score', data=imdb_top_1000, color='purple', label='Meta Score')
plt.title('Relationship Between Gross Revenue, IMDb Ratings, and Meta Scores')
plt.xlabel('Gross Revenue ($)')
plt.ylabel('Ratings and Scores')
plt.xscale('log')
plt.legend()
plt.show()

''' __Genre Analysis__ '''
# Extracting primary genre from the 'Genre' column
imdb_top_1000['Primary_Genre'] = imdb_top_1000['Genre'].apply(lambda x: x.split(',')[0].strip())

# Counting movies by primary genre
plt.figure(figsize=(12, 8))
genre_counts = imdb_top_1000['Primary_Genre'].value_counts()
sns.barplot(x=genre_counts.index, y=genre_counts.values, hue=genre_counts.index, palette='viridis', dodge=False)
plt.xticks(rotation=45)
plt.title('Number of Movies by Primary Genre in Top 1000')
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.legend([],[], frameon=False)  # Hides the legend
plt.show()

''' __Yearly Trends__ '''
# Convert 'Released_Year' to numeric, handling non-numeric entries
imdb_top_1000['Released_Year'] = pd.to_numeric(imdb_top_1000['Released_Year'], errors='coerce')
yearly_trends = imdb_top_1000.groupby('Released_Year')['IMDB_Rating'].mean()

# Plotting average IMDb rating by year
plt.figure(figsize=(14, 7))
sns.lineplot(x=yearly_trends.index, y=yearly_trends.values, color='green')
plt.title('Average IMDb Rating by Release Year')
plt.xlabel('Year')
plt.ylabel('Average IMDb Rating')
plt.show()

''' __Director Analysis__ '''
# Identifying top 10 directors with the most entries in the top 1000
top_directors = imdb_top_1000['Director'].value_counts().head(10)

# Plotting top directors
plt.figure(figsize=(12, 8))
sns.barplot(x=top_directors.values, y=top_directors.index, hue=top_directors.index, palette='coolwarm', orient='h', dodge=False)
plt.title('Top 10 Directors with Most Movies in Top 1000')
plt.xlabel('Number of Movies')
plt.ylabel('Director')
plt.legend([],[], frameon=False)  # Hides the legend
plt.show()

''' __Relationship between Gross Revenue and Ratings__ '''
# Plotting relationship between gross revenue and IMDb ratings
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Gross', y='IMDB_Rating', data=imdb_top_1000, color='red')
plt.title('Relationship Between Gross Revenue and IMDb Ratings')
plt.xlabel('Gross Revenue ($)')
plt.ylabel('IMDb Rating')
plt.xscale('log')  # Using log scale due to wide range of revenue values
plt.show()
