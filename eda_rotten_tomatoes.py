import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd  # Importing pandas to read the CSV file

# Load the CSV file into a DataFrame
rotten_tomatoes = pd.read_csv('cleaned_rotten_tomatoes_movies_1.csv')

''' __Distribution of Tomatometer and Audience Ratings__ '''

# Setting aesthetic style for plots
sns.set(style="whitegrid")

# Distribution of Tomatometer Ratings
plt.figure(figsize=(10, 6))
sns.histplot(rotten_tomatoes['tomatometer_rating'], bins=20, kde=True, color='blue')
plt.title('Distribution of Tomatometer Ratings')
plt.xlabel('Tomatometer Rating')
plt.ylabel('Frequency')
plt.show()

# Distribution of Audience Ratings
plt.figure(figsize=(10, 6))
sns.histplot(rotten_tomatoes['audience_rating'], bins=20, kde=True, color='green')
plt.title('Distribution of Audience Ratings')
plt.xlabel('Audience Rating')
plt.ylabel('Frequency')
plt.show()

''' __Genre Analysis: Average Ratings by Genre__ '''
# Extract primary genre
rotten_tomatoes['Primary_Genre'] = rotten_tomatoes['genres'].str.split(',').str[0]

# Calculate average ratings for genres by critics and audiences
genre_analysis = rotten_tomatoes.groupby('Primary_Genre').agg({
    'tomatometer_rating': 'mean',
    'audience_rating': 'mean'
}).dropna().sort_values(by='tomatometer_rating', ascending=False)

# Plot average ratings by genre for critics and audiences
plt.figure(figsize=(14, 8))
sns.barplot(x=genre_analysis.index, y=genre_analysis['tomatometer_rating'], color='blue', label='Tomatometer')
sns.barplot(x=genre_analysis.index, y=genre_analysis['audience_rating'], color='red', alpha=0.6, label='Audience')
plt.xticks(rotation=90)
plt.title('Average Ratings by Genre for Critics and Audiences')
plt.xlabel('Genre')
plt.ylabel('Average Rating')
plt.legend()
plt.show()

''' __Agreement Between Critics and Audience Statuses__ '''
# Adjust status to binary for comparison
rotten_tomatoes['critic_positive'] = rotten_tomatoes['tomatometer_status'].isin(['Certified-Fresh', 'Fresh'])
rotten_tomatoes['audience_positive'] = rotten_tomatoes['audience_status'] == 'Upright'

# Calculate new agreement rate based on binary status
rotten_tomatoes['adjusted_status_agreement'] = rotten_tomatoes['critic_positive'] == rotten_tomatoes['audience_positive']
adjusted_agreement_rate = rotten_tomatoes['adjusted_status_agreement'].mean()

# Plot adjusted agreement rate
plt.figure(figsize=(8, 5))
sns.barplot(x=['Adjusted Agreement'], y=[adjusted_agreement_rate], color='grey')  # Changed from palette='muted' to color='grey'
plt.title('Adjusted Proportion of Agreement between Critics and Audience Statuses')
plt.ylabel('Proportion of Agreement')
plt.ylim(0, 1)  # Limiting Y-axis for better visualization of proportions
plt.show()


''' __Top Production Companies Analysis__ '''
# Importing necessary libraries

# Load the dataset
rotten_tomatoes = pd.read_csv('cleaned_rotten_tomatoes_movies_1.csv')

# Check if the necessary columns to compute 'adjusted_status_agreement' exist
if 'tomatometer_status' in rotten_tomatoes.columns and 'audience_status' in rotten_tomatoes.columns:
    # Convert statuses to a uniform binary format for comparison
    rotten_tomatoes['critic_positive'] = rotten_tomatoes['tomatometer_status'].isin(['Certified-Fresh', 'Fresh'])
    rotten_tomatoes['audience_positive'] = rotten_tomatoes['audience_status'] == 'Upright'

    # Calculate the 'adjusted_status_agreement'
    rotten_tomatoes['adjusted_status_agreement'] = (rotten_tomatoes['critic_positive'] == rotten_tomatoes['audience_positive']).astype(int)

else:
    print("Required columns for calculating 'adjusted_status_agreement' are missing.")

# Now proceed with your aggregation
production_companies_ratings = rotten_tomatoes.groupby('production_company').agg({
    'tomatometer_rating': 'mean',
    'audience_rating': 'mean',
    'adjusted_status_agreement': 'mean'  # This should now work as the column exists
}).dropna()

# Continue with the filtering and sorting as previously
top_production_companies = production_companies_ratings[
    (production_companies_ratings['tomatometer_rating'] > 70) &
    (production_companies_ratings['audience_rating'] > 70) &
    (production_companies_ratings['adjusted_status_agreement'] > 0.7)
].sort_values(by='tomatometer_rating', ascending=False).head(10)

# Print the DataFrame to check the output
if not top_production_companies.empty:
    print(top_production_companies)
else:
    print("No production companies meet the criteria.")

# Plot the comparison

# Check if the DataFrame is empty
if not top_production_companies.empty:
    # Reset index to get 'production_company' as a column
    top_production_companies.reset_index(inplace=True)

    # Melt the DataFrame to long format for easier plotting with seaborn
    melted_df = top_production_companies.melt(id_vars='production_company',
                                              value_vars=['tomatometer_rating', 'audience_rating'],
                                              var_name='Rating Type', value_name='Rating')

    # Create a bar plot
    plt.figure(figsize=(12, 8))
    barplot = sns.barplot(x='production_company', y='Rating', hue='Rating Type', data=melted_df)
    plt.xticks(rotation=45, ha='right')
    plt.title('Comparative Ratings of Top Production Companies')
    plt.xlabel('Production Company')
    plt.ylabel('Average Rating')
    plt.legend(title='Rating Type')

    # Improve layout
    plt.tight_layout()

    # Show the plot
    plt.show()
else:
    print("No production companies meet the criteria.")
