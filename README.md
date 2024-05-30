# Unlocking Viewer Insights: Leveraging Reviews and Ratings to Propel Movie Success


The project aims to analyze IMDb and Rotten Tomatoes (RT) datasets, supplemented with new user review data collected from IMDb, to understand the impact of viewer insights on movie success.

The analysis reveals a significant correlation between user ratings and movie success and identifies the influence of user sentiment on viewership. Key findings include:
- Ratings and Revenue: Both IMDb audience and professional ratings show a positive correlation with gross revenue, suggesting that higher ratings can predict financial success.
- Sentiment Analysis: The sentiment from user reviews impacts movie reception. Positive sentiments are linked to higher viewership and can be leveraged in marketing strategies.
- Viewer Insights for Marketing: The data suggests that understanding viewer sentiment and ratings can help tailor marketing strategies to enhance movie success and viewer engagement.


Based on the analysis, production firms can benefit by leveraging positive user sentiments in promotional activities, addressing negative feedback to improve future projects, and using detailed content analysis to align movie elements with audience preferences. These strategies are designed to enhance engagement and optimize marketing efforts for better reception and success of movies.

## Background
In the dynamic landscape of the film industry, production companies' strategic decisions are increasingly influenced by audience awareness and critical reception.  This study investigates how these factors shape the varying reception of films across diverse audiences and influential platforms.

By analyzing datasets from IMDb and Rotten Tomatoes, this research focuses on key performance indicators (KPIs) that offer both qualitative and quantitative measures of success. These KPIs encompass box office performance, audience and critic ratings, and engagement metrics such as review volume and user interactions.  Through an examination of these KPIs, this study aims to provide a comprehensive understanding of each film's reception and its implications for future productions. 

## Data Inspection
**Dataset 1: imdb_top_1000.csv**
- Contents: This dataset contains details about the top 1000 movies on IMDb, including titles, directors, genres, year of release, IMDb ratings, etc.

**Dataset 2: rotten_tomatoes_movies_1.csv**
- Contents: This dataset includes movie titles, Rotten Tomatoes scores, audience scores, critic counts, and more.

**Datasets 3, 4, 5: User Review Datasets** (imdbreviews_3idiots2009.csv, imdbreviews_saw2004.csv, imdbreviews_thelionking1994.csv)
- Contents: These datasets contain user reviews for the movies "3 Idiots", "Saw", and "The Lion King".

*Datasets 3, 4, and 5 consist of user review data from IMDb, collected through web scraping. The specific methodology and code used for this process are documented in this repository.* [Scraping IMDB Reviews in R](https://github.com/rishav21r/Scraping-IMDB-Review-in-R)

## Data Cleaning
Steps for cleaning the IMDb and Rotten Tomatoes datasets, focusing on handling missing values and ensuring correct data types. 
```python
    """ Specific cleaning steps for each dataset based on known structure. """
    if 'imdb_top_1000.csv' in file_path:
        # Fill missing 'Meta_score' with the median of the column
        data['Meta_score'].fillna(data['Meta_score'].median(), inplace=True)
        # For 'Certificate', use the most common certificate if not specified
        data['Certificate'].fillna(data['Certificate'].mode()[0], inplace=True)
        # Convert 'Gross' to numeric, removing non-numeric characters
        data['Gross'] = data['Gross'].replace(r'[\$,]', '', regex=True).astype(float)
        data['Gross'].fillna(data['Gross'].median(), inplace=True)
        data['IMDB_Rating'] = data['IMDB_Rating'].astype(float)

    elif 'rotten_tomatoes_movies_1.csv' in file_path:
        # Fill missing values in 'tomatometer_rating' and 'audience_rating'
        data['tomatometer_rating'].fillna(data['tomatometer_rating'].median(), inplace=True)
        data['audience_rating'].fillna(data['audience_rating'].median(), inplace=True)
        # Convert date fields to DateTime
        data['original_release_date'] = pd.to_datetime(data['original_release_date'], errors='coerce')
        data['streaming_release_date'] = pd.to_datetime(data['streaming_release_date'], errors='coerce')
```

## Data Integration & Prepration
IMDb ratings were standardized to a 0-100 scale, matching Rotten Tomatoes. Both databases were integrated via a full outer join, and movie titles were normalized for consistency.

```python
def normalize_and_prepare_data(self):
        """ Normalize IMDb ratings and prepare data by merging datasets. """
        self.imdb_data['IMDB_Rating'] = self.imdb_data['IMDB_Rating'] * 10
        self.imdb_data['platform'] = 'IMDb'
        self.rotten_tomatoes_data['platform'] = 'Rotten Tomatoes'
        self.imdb_data.rename(columns={'Series_Title': 'movie_title'}, inplace=True)
        self.imdb_data['movie_title_lower'] = self.imdb_data['movie_title'].str.lower()
        self.rotten_tomatoes_data['movie_title_lower'] = self.rotten_tomatoes_data['movie_title'].str.lower()
        self.combined_data = pd.merge(self.imdb_data, self.rotten_tomatoes_data, on='movie_title_lower', how='outer', suffixes=('_imdb', '_rt'))
        self.combined_data.rename(columns={'Gross': 'Gross_imdb'}, inplace=True)
        print("Data normalized and prepared.")
```


## Data Analysis
This comprehensive analysis unfolds in several stages:
- **Descriptive and Distributional Analysis:** To track rating trends across IMDb and Rotten Tomatoes to reveal how audiences and critics perceive films.
- **Comparative Analysis:** Employing statistical tests, the aim is to highlight significant differences between audience and critic ratings, offering insights into potential biases or preferences.
- **Sentiment Analysis:** By linking user review sentiments to movie ratings, uncover how emotional responses impact overall evaluations.
- **Revenue Analysis:** To explore the correlation between ratings and box office success to understand the financial implications of critical and popular acclaim.
- **Content Rating Profitability:** This examines revenue data to guide genre choices and inform future production strategies.



## Key Findings

### Descriptive and Distributional Analysis:
#### Histogram 
*_The histogram plots aim to explore the distribution of four metrics: IMDb Audience Rating (IMDB rating), IMDb Professional Rating (Meta score), RT Audience Rating and RT Professional Rating (Tomatometer rating)._*
- The IMDb audience rating distribution is right-skewed, with most scores concentrated above 70, while the Rotten Tomatoes audience rating distribution more closely resembles a normal distribution with a wider range. This suggests that IMDb users tend to rate films more generously than Rotten Tomatoes users.

- The IMDb professional rating distribution is approximately normal, peaking at around 80, while the Rotten Tomatoes professional rating distribution is left-skewed, peaking at 100 with a wider spread. This indicates that IMDb professionals are more likely to give moderate ratings, while Rotten Tomatoes professionals tend to give more extreme ratings, both high and low.

![alt text][logo1]

[logo1]: plots/histogram.png "Histogram of Ratings"

#### Cumulative Distribution Functions (CDFs)
CDFs offer a clear visual representation of the proportion of ratings that fall below specific values. The CDF for IMDb Ratings reveals a steep rise at higher rating values, indicating a concentration of higher scores. In contrast, the CDF for Tomatometer Ratings displays a more gradual increase, suggesting a more diverse distribution of ratings across the spectrum.

![alt text][logo2]

[logo2]: plots/cdf.png "Cumulative Distribution Functions"

#### Rating Distribution
Violin plots offer a more detailed understanding of the distribution of film ratings across different platforms.  IMDb Meta_scores tend to cluster more tightly, with fewer low ratings compared to Tomatometer Ratings, which span a broader range and show a more even distribution across the rating scale. Audience Ratings on Rotten Tomatoes are slightly skewed towards higher scores but still demonstrate considerable variation, particularly in the mid-range.

![alt text][logo3]

[logo3]: plots/violinplot.png "Violin Plot for all Ratings"

#### Yearly Trends
IMDb ratings have demonstrated a consistent standard over time, with a slight upward trend in recent years, suggesting enduring audience preferences on the platform. In contrast, Meta_scores and Tomatometer ratings have fluctuated notably, reflecting the evolving nature of critical reception, potentially influenced by shifts in film quality, genre trends, or critical standards. Despite these variations, all rating types generally average high, indicating an overall positive sentiment from both critics and audiences. However, a minor decline in audience ratings recently hints at evolving viewer expectations or a potential shift in preferences towards newer films.
