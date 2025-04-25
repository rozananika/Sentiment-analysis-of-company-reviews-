from flask import Flask, render_template_string, request
import pandas as pd
import os

app = Flask(__name__)

# Load processed data or process if not present
df_path = 'processed_company_reviews.csv'
if not os.path.exists(df_path):
    # Fallback: Try to use raw CSV if processed not found
    df_path = 'company_reviews.csv'
    if not os.path.exists(df_path):
        raise FileNotFoundError('No processed or raw dataset found. Please run app.py first.')
    df = pd.read_csv(df_path, encoding='utf-8', engine='python')
else:
    df = pd.read_csv(df_path, encoding='utf-8', engine='python')

# Home page: list companies
@app.route('/')
def home():
    companies = sorted(df['name'].dropna().unique())
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
      <title>Company Reviews Sentiment Analysis</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Company Reviews</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="/">All Companies</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/dashboard">Dashboards</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <h2 class="mb-4">Select a company:</h2>
      <ul class="list-group">
      {% for company in companies %}
        <li class="list-group-item"><a href="/company?name={{ company }}">{{ company }}</a></li>
      {% endfor %}
      </ul>
    </div>
    </body>
    </html>
    ''', companies=companies)

# Company detail page
@app.route('/company')
def company_detail():
    company = request.args.get('name')
    if not company:
        return 'No company specified.'
    company_df = df[df['name'] == company]
    if company_df.empty:
        return f'No data for company: {company}'
    # Prepare data for display
    reviews = company_df['reviews'].fillna('').tolist()
    descriptions = company_df['description'].fillna('').tolist()
    vader_scores = company_df['vader_sentiment_score'].fillna('').tolist() if 'vader_sentiment_score' in company_df else []
    textblob_scores = company_df['textblob_sentiment_score'].fillna('').tolist() if 'textblob_sentiment_score' in company_df else []
    vader_sentiments = company_df['vader_sentiment'].fillna('').tolist() if 'vader_sentiment' in company_df else []
    textblob_sentiments = company_df['textblob_sentiment'].fillna('').tolist() if 'textblob_sentiment' in company_df else []
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
      <title>{{ company }} - Company Reviews Sentiment Analysis</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Company Reviews</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="/">All Companies</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <h1 class="mb-3">{{ company }}</h1>
      <h2 class="mb-4">Reviews and Analysis</h2>
      <table class="table table-striped table-bordered">
        <thead class="table-primary">
          <tr>
            <th>#</th>
            <th>Review</th>
            <th>Description</th>
            <th>VADER Score</th>
            <th>VADER Sentiment</th>
            <th>TextBlob Score</th>
            <th>TextBlob Sentiment</th>
          </tr>
        </thead>
        <tbody>
          {% for i in range(reviews|length) %}
          <tr>
            <td>{{ i+1 }}</td>
            <td>{{ reviews[i][:300] }}</td>
            <td>{{ descriptions[i][:300] }}</td>
            <td>{{ vader_scores[i] if vader_scores else '' }}</td>
            <td>{{ vader_sentiments[i] if vader_sentiments else '' }}</td>
            <td>{{ textblob_scores[i] if textblob_scores else '' }}</td>
            <td>{{ textblob_sentiments[i] if textblob_sentiments else '' }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    </body>
    </html>
        <th>TextBlob Score</th>
        <th>TextBlob Sentiment</th>
      </tr>
      {% for i in range(reviews|length) %}
      <tr>
        <td>{{ i+1 }}</td>
        <td>{{ reviews[i][:300] }}</td>
        <td>{{ descriptions[i][:300] }}</td>
        <td>{{ vader_scores[i] if vader_scores else '' }}</td>
        <td>{{ vader_sentiments[i] if vader_sentiments else '' }}</td>
        <td>{{ textblob_scores[i] if textblob_scores else '' }}</td>
        <td>{{ textblob_sentiments[i] if textblob_sentiments else '' }}</td>
      </tr>
      {% endfor %}
    </table>
    ''', company=company, reviews=reviews, descriptions=descriptions, vader_scores=vader_scores, vader_sentiments=vader_sentiments, textblob_scores=textblob_scores, textblob_sentiments=textblob_sentiments)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # List of expected PNGs from analysis
    chart_files = [
        'sentiment_distribution_vader.png',
        'sentiment_score_distribution_vader.png',
        'top_10_company_sentiment_vader.png',
        'locations_sentiment.png',
        'ratings_vs_sentiment.png',
        'revenue_vs_sentiment.png',
    ]
    # Only include charts that exist
    charts = [f for f in chart_files if os.path.exists(f)]
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
      <title>Dashboards - Company Reviews Sentiment Analysis</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Company Reviews</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="/">All Companies</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="/dashboard">Dashboards</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <h1 class="mb-4">Dashboards</h1>
      <div class="row">
      {% for chart in charts %}
        <div class="col-md-6 mb-4">
          <div class="card">
            <img src="/{{ chart }}" class="card-img-top" alt="{{ chart }}">
            <div class="card-body">
              <h5 class="card-title">{{ chart.replace('_', ' ').replace('.png', '').title() }}</h5>
            </div>
          </div>
        </div>
      {% endfor %}
      </div>
      {% if not charts %}
        <div class="alert alert-warning">No dashboard charts found. Please run the analysis script to generate them.</div>
      {% endif %}
    </div>
    </body>
    </html>
    ''', charts=charts)

# Serve static images from root
from flask import send_from_directory
@app.route('/<path:filename>')
def serve_static(filename):
    if filename.endswith('.png'):
        return send_from_directory('.', filename)
    return '', 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)
