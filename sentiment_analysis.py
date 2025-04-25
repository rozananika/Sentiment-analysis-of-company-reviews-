import pandas as pd
from textblob import TextBlob
import re

# Load the CSV file (handles multiline fields)
import matplotlib.pyplot as plt
from collections import defaultdict

skipped_lines = 0
review_data = []  # List of dicts: {'company': name, 'text': review/description, 'sentiment': score}
import csv

with open('company_reviews.csv', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            company = str(row.get('name', 'Unknown'))
            review = str(row.get('reviews', ''))
            description = str(row.get('description', ''))
            # Remove extra whitespace and linebreaks
            review = re.sub(r'\s+', ' ', review).strip()
            description = re.sub(r'\s+', ' ', description).strip()
            text = review if review and review.lower() != 'nan' else description
            if text and text.lower() != 'nan':
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                review_data.append({'company': company, 'text': text, 'sentiment': polarity})
        except Exception:
            skipped_lines += 1

if not review_data:
    print("No review texts found for sentiment analysis.")
    exit()

# Sentiment by company
company_sentiments = defaultdict(list)
for row in review_data:
    company_sentiments[row['company']].append(row['sentiment'])

company_avg_sent = {c: sum(s)/len(s) for c,s in company_sentiments.items() if s}
company_review_count = {c: len(s) for c,s in company_sentiments.items()}

# Top 10 companies by review count
top_companies = sorted(company_review_count.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 companies by review count and their average sentiment:")
for c, count in top_companies:
    avg = company_avg_sent[c]
    print(f"{c}: {count} reviews, avg sentiment {avg:.3f}")

# Most positive, negative, and neutral reviews
most_positive = max(review_data, key=lambda x: x['sentiment'])
most_negative = min(review_data, key=lambda x: x['sentiment'])
most_neutral = min(review_data, key=lambda x: abs(x['sentiment']))

print("\nMost positive review:")
print(f"Company: {most_positive['company']} | Sentiment: {most_positive['sentiment']:.3f}")
print(most_positive['text'][:500], '...')

print("\nMost negative review:")
print(f"Company: {most_negative['company']} | Sentiment: {most_negative['sentiment']:.3f}")
print(most_negative['text'][:500], '...')

print("\nMost neutral review:")
print(f"Company: {most_neutral['company']} | Sentiment: {most_neutral['sentiment']:.3f}")
print(most_neutral['text'][:500], '...')

# Visualization: Bar chart of average sentiment by top companies
plt.figure(figsize=(10,5))
companies = [c for c, _ in top_companies]
avgs = [company_avg_sent[c] for c in companies]
plt.bar(companies, avgs, color='skyblue')
plt.ylabel('Average Sentiment Polarity')
plt.title('Average Sentiment by Company (Top 10 by Review Count)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('company_sentiment_bar.png')
print("\nBar chart saved as 'company_sentiment_bar.png'.")

# Histogram of all sentiment scores
plt.figure(figsize=(8,4))
plt.hist([row['sentiment'] for row in review_data], bins=30, color='orange', edgecolor='black')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Sentiment Polarity (All Reviews)')
plt.tight_layout()
plt.savefig('sentiment_histogram.png')
print("Histogram saved as 'sentiment_histogram.png'.")
