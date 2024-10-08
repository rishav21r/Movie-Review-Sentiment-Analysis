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

### Descriptive and Distributional Analysis
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
Violin plots offer a more detailed understanding of the distribution of film ratings across different platforms.  IMDb Meta scores tend to cluster more tightly, with fewer low ratings compared to Tomatometer Ratings, which span a broader range and show a more even distribution across the rating scale. Audience Ratings on Rotten Tomatoes are slightly skewed towards higher scores but still demonstrate considerable variation, particularly in the mid-range.

![alt text][logo3]

[logo3]: plots/violinplot.png "Violin Plot for all Ratings"

#### Yearly Trends
IMDb ratings have demonstrated a consistent standard over time, with a slight upward trend in recent years, suggesting enduring audience preferences on the platform. In contrast, Meta_scores and Tomatometer ratings have fluctuated notably, reflecting the evolving nature of critical reception, potentially influenced by shifts in film quality, genre trends, or critical standards. Despite these variations, all rating types generally average high, indicating an overall positive sentiment from both critics and audiences. However, a minor decline in audience ratings recently hints at evolving viewer expectations or a potential shift in preferences towards newer films.

![alt text][logo4]

[logo4]: plots/yearlytrends.png "Yearly trends for all Ratings"

### Comparative Analysis

#### Average Rating Comparison
IMDb audience ratings and Rotten Tomatoes audience scores show a close alignment, indicating a general consistency in public opinion across both platforms. While Meta scores and RT Tomatometer ratings also exhibit similarity, a slight divergence suggests some variability in critical assessments between the two platforms.

![alt text][logo5]

[logo5]: plots/ratingcomparison.png "Average Rating Comparison"

#### Mean Critic Scores with Error Bars
While the average Meta_score marginally surpasses the average Tomatometer rating, the overlapping error bars suggest this difference might not be statistically significant. This implies that, while a slight trend exists, the two scores are practically interchangeable for most purposes. The notable standard deviations further emphasize the inherent variability in critical opinions, underscoring that individual film ratings can diverge significantly despite the overall agreement in average scores.

![alt text][logo6]

[logo6]: plots/errorbars.png "Mean Critic Scores with Error Bars"

#### Correlation between Ratings
**T-test Results:**
- T-statistic: -10.49
- P-value: 6.88e-25

  The t-test results show a significant difference between the mean Meta_score and Tomatometer ratings, indicating that critics' scores on IMDb and Rotten Tomatoes differ statistically.
  
**Correlation Results:**
- Correlation between IMDb Ratings and RT Audience Ratings: 0.213
- Correlation between IMDb Meta Scores and RT Tomatometer Ratings: 0.465

  The correlations suggest a moderate positive relationship between Meta_scores and Tomatometer ratings and a weaker positive relationship between IMDb ratings and RT audience ratings.

![alt text][logo7]

[logo7]: plots/correlations.png "Correlation between Ratings"

### Sentiment Analysis
An initial sentiment analysis was performed on three films: "The Lion King (1994)", "Saw (2004)", and "3 Idiots (2009)". This analysis encompassed examining the distribution of sentiment categories, the distribution of sentiment scores, and the correlation between sentiment scores and ratings. Detailed findings for each film are presented below. (For specific details on how these movies were selected, please refer to the following repository: [Scraping IMDB Reviews in R](https://github.com/rishav21r/Scraping-IMDB-Review-in-R)).

**The Lion King (1994)**

**1. Sentiment Distribution:**
- Positive: 96.05%
- Negative: 3.95%
- Neutral: 0.00%

![alt text][logo8]

[logo8]: plots/sentimentlk.png "Distribution of Sentiment for The Lion King (1994)"

**2. Sentiment Score Distribution:**

The majority of reviews expressed a positive sentiment, with sentiment scores predominantly concentrated around positive values.


![alt text][logo9]

[logo9]: plots/sentimentscorelk.png "Distribution of Sentiment Score for The Lion King (1994)"


**3.Correlation between Sentiment Scores and Ratings:**
- Average Sentiment Score: 0.29
- Average Rating: 8.55

![alt text][logo10]

[logo10]: plots/sentimentvsratinglk.png "Correlation between Sentiment Scores and Ratings for The Lion King (1994)"

Sentiment analysis reveals overwhelmingly positive feedback for "The Lion King (1994)", with a strong correlation between positive sentiment and high ratings, affirming the audience's positive reception of this highly-rated film.

**Saw (2004)**

**1. Sentiment Distribution:**
- Positive: 75.88%
- Negative: 24.12%
- Neutral: 0.00%

![alt text][logo11]

[logo11]: plots/sentimentsaw.png "Distribution of Sentiment for Saw (2004)"

**2. Sentiment Score Distribution:**

Although positive sentiment prevails, a notable proportion of reviews express negative sentiment.

![alt text][logo12]

[logo12]: plots/sentimentscoresaw.png "Distribution of Sentiment Score for Saw (2004)"

**3.Correlation between Sentiment Scores and Ratings:**
- Average Sentiment Score: 0.08
- Average Rating: 7.67

![alt text][logo13]

[logo13]: plots/sentimentvsratingsaw.png "Correlation between Sentiment Scores and Ratings for Saw (2004)"

In contrast to the overwhelmingly positive sentiment for "The Lion King (1994)", "Saw (2004)" elicits a more divided response. The lower average sentiment score and the significant presence of negative sentiment suggest a polarized audience reaction to "Saw (2004)".

**3 Idiots (2009)**

**1. Sentiment Distribution:**
- Positive: 94.12%
- Negative: 4.71%
- Neutral: 1.18%

![alt text][logo14]

[logo14]: plots/sentiment3i.png "Distribution of Sentiment for 3 Idiots (2009)"

**2. Sentiment Score Distribution:**

Much like "The Lion King (1994)", the majority of reviews for "3 Idiots (2009)" are positive, with very few falling into the neutral or negative categories.

![alt text][logo15]

[logo15]: plots/sentimentscore3i.png "Distribution of Sentiment Score for 3 Idiots (2009)"

**3.Correlation between Sentiment Scores and Ratings:**
- Average Sentiment Score: 0.08
- Average Rating: 7.67

![alt text][logo16]

[logo16]: plots/sentimentvsrating3i.png "Correlation between Sentiment Scores and Ratings for 3 Idiots (2009)"

Like "The Lion King (1994)", audiences overwhelmingly loved "3 Idiots (2009)".  Its high average rating and positive sentiment score are a testament to its popularity.

### Revenue Analysis
#### Correlation Analysis:
The scatter plots with regression lines for IMDb Rating vs. Gross Revenue and Meta Score vs. Gross Revenue show the distribution and trend of the data points. The visual inspection suggests a weak relationship between the ratings and gross revenue.

![alt text][logo17]

[logo17]: plots/revenue.png "Rating vs Gross Revenue for IMDB"

#### Regression Analysis:

| Feature       | Coefficient   | Intercept       | R-Squared  |
| :-------------|:--------------| :---------------| :----------|
| IMDB Rating   | 5448623.83    | -352611928.67   | 0.0177     |
| Meta Score    | -429086.03    | 112971161.85    | 0.0019     |

    
- For IMDb ratings, each one-point increase is associated with a rise of roughly $5.45 million in gross revenue. However, the R-squared value of 1.77% suggests this relationship is weak and that IMDb ratings alone explain a very small portion of the variance in a movie's financial success.
- Interestingly, Meta scores show an inverse relationship, with each one-point increase linked to a decrease of about $430,000 in gross revenue. Yet again, the R-squared value of 0.2% indicates this is a very weak connection, and Metacritic scores alone are not a strong predictor of a movie's box office performance.

#### Residual Plots:
The residual plots for both IMDb Rating and Meta Score illustrate the distribution of differences between the actual gross revenue and the revenue predicted by our linear models. The non-random patterns in these plots suggest that these models, which assume a straightforward linear relationship, may not fully capture the complex nuances of how ratings and gross revenue interact.

![alt text][logo18]

[logo18]: plots/residual.png "Residual Plots for IMDB"

The analysis reveals that movie ratings, whether from IMDb or Metacritic (Meta score), have only a slight influence on a movie's gross revenue. The low R-squared values demonstrate that factors beyond ratings play a much larger role in a film's box office success. To gain a deeper understanding of these factors, further analysis could explore the impact of marketing budgets, distribution strategies, and genre on a movie's financial performance.

### Content Rating Profitability
The highest-grossing films, averaging $143.3 million, fall within the "86 to 90" rating category, indicating that movies with IMDb scores in this range tend to be the most commercially successful. The "Above 90" category follows closely behind, averaging a still impressive $81.7 million, but suggesting that exceptionally high ratings don't always guarantee the highest earnings.  Films rated "76 to 80" demonstrate moderate commercial success, averaging $60.5 million, while the "81 to 85" category trails with an average gross of $56.4 million, the lowest among the analyzed categories.

![alt text][logo19]

[logo19]: plots/grossrevenue.png "Average Gross Revenue by IMDb Rating Category"
