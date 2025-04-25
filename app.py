import os
import pandas as pd
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

# Download Kaggle dataset if not present
def download_kaggle_dataset():
    kaggle_path = 'company-reviews.zip'
    csv_path = 'company_reviews.csv'
    if not os.path.exists(csv_path):
        print('Downloading dataset from Kaggle...')
        os.system('kaggle datasets download -d vaghefi/company-reviews -f company_reviews.csv')
        os.system('unzip -o company_reviews.csv.zip')
        print('Dataset downloaded and extracted.')
    else:
        print('Dataset already exists.')

# Data preprocessing function
def preprocess_text(text):
    if pd.isna(text) or not text:
        return ''
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Extract revenue as numeric (in millions)
def extract_revenue(revenue_str):
    if pd.isna(revenue_str):
        return float('nan')
    match = re.search(r'\$([\d.]+)([MB]?)', revenue_str)
    if match:
        value = float(match.group(1))
        if match.group(2) == 'M':
            return value
        elif match.group(2) == 'B':
            return value * 1000
    return float('nan')

def main():
    download_kaggle_dataset()
    df = pd.read_csv('company_reviews.csv', encoding='utf-8', engine='python')
    print("Dataset Preview:")
    print(df.head())

    # Clean description
    df['cleaned_description'] = df['description'].apply(preprocess_text)

    # Initialize VADER
    sia = SentimentIntensityAnalyzer()

    # VADER sentiment
    def get_vader_sentiment(text):
        if not text:
            return 0.0
        scores = sia.polarity_scores(text)
        return scores['compound']

    # TextBlob sentiment
    def get_textblob_sentiment(text):
        if not text:
            return 0.0
        return TextBlob(text).sentiment.polarity

    df['vader_sentiment_score'] = df['cleaned_description'].apply(get_vader_sentiment)
    df['textblob_sentiment_score'] = df['cleaned_description'].apply(get_textblob_sentiment)

    def classify_sentiment(score):
        if score >= 0.02:
            return 'Positive'
        elif score <= -0.02:
            return 'Negative'
        else:
            return 'Neutral'

    df['vader_sentiment'] = df['vader_sentiment_score'].apply(classify_sentiment)
    df['textblob_sentiment'] = df['textblob_sentiment_score'].apply(classify_sentiment)

    # Display sentiment distributions
    print("\nVADER Sentiment Distribution (%):")
    print(df['vader_sentiment'].value_counts(normalize=True) * 100)
    print("\nTextBlob Sentiment Distribution (%):")
    print(df['textblob_sentiment'].value_counts(normalize=True) * 100)

    # Correlation analysis
    numeric_cols = ['rating', 'vader_sentiment_score', 'textblob_sentiment_score']
    if 'revenue' in df.columns and pd.api.types.is_numeric_dtype(df['revenue']):
        numeric_cols.append('revenue')
    if 'salaries' in df.columns and pd.api.types.is_numeric_dtype(df['salaries']):
        numeric_cols.append('salaries')
    print("\nCorrelation Matrix:")
    print(df[numeric_cols].corr())

    # Visualization 1: Sentiment distribution (VADER)
    plt.figure(figsize=(8, 6))
    sns.countplot(x='vader_sentiment', data=df, palette='viridis')
    plt.title('Sentiment Distribution of Company Reviews (VADER)')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.savefig('sentiment_distribution_vader.png')
    plt.close()

    # Visualization 2: Sentiment score distribution (VADER)
    plt.figure(figsize=(8, 6))
    sns.histplot(df['vader_sentiment_score'], bins=30, kde=True, color='blue')
    plt.title('Distribution of VADER Sentiment Scores')
    plt.xlabel('VADER Sentiment Score')
    plt.ylabel('Frequency')
    plt.savefig('sentiment_score_distribution_vader.png')
    plt.close()

    # Visualization 3: Average sentiment by company (Top 10)
    company_sentiment = df.groupby('name')['vader_sentiment_score'].mean().sort_values(ascending=False)
    top_10_companies = company_sentiment.head(10)
    plt.figure(figsize=(12, 6))
    top_10_companies.plot(kind='bar', color='purple')
    plt.title('Average Sentiment Score by Company (VADER - Top 10)')
    plt.xlabel('Company')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('top_10_company_sentiment_vader.png')
    plt.close()

    # Visualization 4: Sentiment by Location (top 10)
    if 'locations' in df.columns:
        location_sentiment = df.groupby('locations')['vader_sentiment_score'].mean().sort_values(ascending=False)[:10]
        location_sentiment.index = location_sentiment.index.str.slice(0, 15)
        plt.figure(figsize=(10, 6))
        location_sentiment.plot(kind='bar', color='pink')
        plt.title('Average Sentiment Score by Location (Top 10)')
        plt.xlabel('locations')
        plt.ylabel('Average Sentiment Score')
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        plt.savefig('locations_sentiment.png')
        plt.close()

    # Visualization 5: Rating vs Sentiment Score
    if 'ratings' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='ratings', y='vader_sentiment_score', data=df, alpha=0.5)
        plt.title('ratings vs Sentiment Score')
        plt.xlabel('ratings')
        plt.ylabel('Sentiment Score')
        plt.savefig('ratings_vs_sentiment.png')
        plt.close()

    # Revenue extraction and plot
    if 'revenue' in df.columns:
        df['revenue_numeric'] = df['revenue'].apply(extract_revenue)
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='revenue_numeric', y='vader_sentiment_score', data=df, alpha=0.5)
        plt.title('Revenue vs VADER Sentiment Score')
        plt.xlabel('Revenue (Millions USD)')
        plt.ylabel('VADER Sentiment Score')
        plt.savefig('revenue_vs_sentiment.png')
        plt.close()

    # Save processed dataset
    df.to_csv('processed_company_reviews.csv', index=False)
    print("Processed dataset saved as 'processed_company_reviews.csv'")

if __name__ == '__main__':
    main()
