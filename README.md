# Company Reviews Sentiment Analysis App

This project provides a complete pipeline for analyzing and visualizing company reviews using sentiment analysis. It includes data processing, sentiment scoring, and a modern Flask web app for exploring results.

## Features
- **Automated Data Download**: Downloads company reviews dataset from Kaggle (requires Kaggle API credentials).
- **Data Cleaning & Preprocessing**: Cleans review and description text for analysis.
- **Sentiment Analysis**: Uses both VADER and TextBlob to analyze sentiment of each review.
- **Visualizations**: Generates charts for sentiment distributions, top companies, ratings vs sentiment, and more.
- **Flask Web App**: Browse companies, see their reviews/descriptions and sentiment analysis, and view dashboards with all generated charts.
- **Modern UI**: Responsive Bootstrap-based navigation and tables.

## Setup Instructions

### 1. Clone the repository and install dependencies
```bash
pip install pandas nltk textblob matplotlib seaborn flask kaggle
```

### 2. Kaggle API Credentials
- Download `kaggle.json` from your [Kaggle account settings](https://www.kaggle.com/settings).
- Place it in `C:\Users\<YourUsername>\.kaggle\kaggle.json` (Windows) or `~/.kaggle/kaggle.json` (Linux/Mac).

### 3. Run the Analysis Script
This will download the dataset, process it, and generate all necessary charts.
```bash
python app.py
```

### 4. Start the Flask Web Server
```bash
python flask_app.py
```

- The app will be available at [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Usage
- **Home:** Browse a list of companies and select one to view its reviews and sentiment analysis.
- **Company Page:** See all reviews, descriptions, and sentiment scores for the selected company.
- **Dashboards:** Click "Dashboards" in the toolbar to view all generated charts.

## File Structure
- `app.py` — Main analysis and chart generation script.
- `flask_app.py` — Flask web server for interactive exploration.
- `company_reviews.csv` — Company reviews dataset (downloaded from Kaggle).
- `processed_company_reviews.csv` — Cleaned and analyzed dataset.
- `*.png` — Generated charts for dashboards.

## Customization
- You can add more columns, charts, or features by editing `app.py` and `flask_app.py`.
- For interactive dashboards, consider integrating Plotly Dash or Streamlit.

## License
This project is for educational and demonstration purposes. Dataset copyright belongs to the original Kaggle authors.
