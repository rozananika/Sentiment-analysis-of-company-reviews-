# Company Reviews Sentiment Analysis App

This project provides a complete pipeline for analyzing and visualizing company reviews using sentiment analysis. It includes data processing, sentiment scoring, and a modern Flask web app for exploring results.

## Features
- **Automated Data Download**: Downloads company reviews dataset from Kaggle (requires Kaggle API credentials).
- **Data Cleaning & Preprocessing**: Cleans review and description text for analysis.
- **Sentiment Analysis**: Uses both VADER and TextBlob to analyze sentiment of each review.
- **Interactive Visualizations**:
  - Sentiment distribution across companies
  - Word clouds for positive and negative reviews
  - Sentiment trends over time
  - Ratings vs sentiment analysis
  - Top companies by review volume and sentiment
  - Distribution of review ratings
  - Sentiment by review length
- **Interactive Dashboard**: Modern web interface with tabs for different visualizations
- **Responsive Design**: Works on desktop and mobile devices
- **Company Explorer**: Browse companies and view detailed sentiment analysis for each

## Demo

Explore company reviews and sentiment analysis through an interactive dashboard:
- Browse companies and view their sentiment scores
- Filter and sort companies by various metrics
- View detailed sentiment analysis for each company
- Explore visualizations of review data

## Setup Instructions

### 1. Clone the repository and install dependencies
```bash
git clone https://github.com/yourusername/company-reviews-sentiment-analysis.git
cd company-reviews-sentiment-analysis
pip install -r requirements.txt
```

Or install dependencies manually:
```bash
pip install pandas nltk textblob matplotlib seaborn flask kaggle plotly wordcloud
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
- The interactive dashboard is accessible at [http://127.0.0.1:8080/dashboard](http://127.0.0.1:8080/dashboard)

## Usage

### Web Interface
- **Home Page**: View a list of companies with their sentiment scores and key metrics
- **Company Details**: Click on any company to see detailed analysis including:
  - Sentiment distribution
  - Review statistics
  - Word clouds for positive/negative reviews
  - Sentiment trends over time
- **Interactive Dashboard**: Access the main dashboard for comprehensive visualizations
  - Filter companies by name, rating, or sentiment score
  - Toggle between different chart types
  - Hover over data points for detailed information

### Navigation
- Use the navigation bar to switch between different sections
- Use the search functionality to find specific companies
- Adjust date ranges and filters to customize your analysis

## File Structure
- `app.py` — Main analysis and chart generation script.
- `flask_app.py` — Flask web server for interactive exploration.
- `templates/` — HTML templates for the web interface
  - `base.html` — Base template with navigation and styling
  - `index.html` — Home page with company listings
  - `company.html` — Company details page
  - `dashboard.html` — Interactive dashboard
- `static/` — Static files (CSS, JS, images)
  - `css/` — Custom styles
  - `js/` — JavaScript for interactive features
  - `images/` — Generated charts and visualizations
- `data/` — Data files
  - `company_reviews.csv` — Raw dataset (downloaded from Kaggle)
  - `processed_company_reviews.csv` — Cleaned and analyzed dataset
- `requirements.txt` — Python dependencies

## Customization

### Adding New Visualizations
1. Create a new function in `app.py` that generates your visualization
2. Add a new route in `flask_app.py` to serve the visualization
3. Update the dashboard template to include your new visualization

### Styling
- Modify the CSS files in `static/css/` to change the look and feel
- Update the base template in `templates/base.html` for major layout changes

### Data Sources
- The app currently uses a Kaggle dataset, but you can modify the data loading code to use your own data
- Update the data processing pipeline in `app.py` if your data has a different format

## License
This project is for educational and demonstration purposes. Dataset copyright belongs to the original Kaggle authors.
