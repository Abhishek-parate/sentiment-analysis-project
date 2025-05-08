# SentimentAI - Text Sentiment Analysis

A Flask web application for sentiment analysis using Groq API. This final year project provides a platform to analyze the sentiment of text and categorize it as positive, negative, or neutral.

## Features

- Text sentiment analysis using Groq's advanced language models
- User registration and authentication
- Saving analysis history for registered users
- Responsive design with TailwindCSS
- API endpoint for programmatic access

## Technologies Used

- **Frontend**: HTML, TailwindCSS, JavaScript
- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **AI Integration**: Groq API
- **Authentication**: Flask-Login

## Project Structure

```
sentiment-analysis-project/
│
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API keys, etc.)
├── .gitignore              # Git ignore file
│
├── static/                 # Static files
│   ├── css/
│   │   └── output.css      # Compiled TailwindCSS
│   ├── js/
│   │   └── main.js         # JavaScript functionality
│   └── images/
│       └── hero.jpg        # Sample image
│
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── home.html           # Homepage
│   ├── about.html          # About page
│   ├── test.html           # Sentiment analysis test page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── contact.html        # Contact page
│
├── models/                 # Database models
│   └── user.py             # User model
│
├── services/               # Service layer
│   └── sentiment.py        # Sentiment analysis service using Groq
│
├── utils/                  # Utility functions
│   └── helpers.py          # Helper functions
│
└── db/                     # Database
    └── db.sqlite3          # SQLite database
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sentiment-analysis-project.git
   cd sentiment-analysis-project
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```
   SECRET_KEY=your_secret_key_here
   FLASK_ENV=development
   DATABASE_URI=sqlite:///db/db.sqlite3
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000/`

## API Usage

The application provides a simple API endpoint for sentiment analysis:

```
POST /api/analyze
Content-Type: application/json

{
  "text": "Your text to analyze"
}
```

Example response:

```json
{
  "sentiment": "positive",
  "score": 0.85,
  "explanation": "The text expresses enthusiasm and satisfaction."
}
```

## Obtaining a Groq API Key

To use this application, you need to obtain a Groq API key:

1. Sign up for an account at [groq.com](https://groq.com)
2. Navigate to API settings
3. Generate a new API key
4. Add the key to your `.env` file

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project was developed as a final year project in Computer Science
- Thanks to Groq for providing the language model API
- Thanks to Flask and TailwindCSS communities for the excellent documentation


# Sentiment Analysis Project Summary

This project is a complete Flask web application for sentiment analysis using Groq's API. It's designed to serve as a final year project, offering a sophisticated yet user-friendly interface for analyzing text sentiment.

## Key Components

### Backend (Flask)

- **Flask Application**: The core application with routes for all pages and API endpoints
- **Authentication System**: Complete login/registration system using Flask-Login
- **Database**: SQLAlchemy ORM with SQLite for storing users and analysis history
- **Groq API Integration**: Python service for analyzing text sentiment using Groq's language models

### Frontend

- **TailwindCSS**: Modern, responsive UI with custom styling
- **Interactive UI**: JavaScript-enhanced user experience
- **Form Validation**: Client and server-side validation for all forms
- **Responsive Design**: Mobile-friendly interface that works on all devices

### Pages

1. **Home**: Landing page with feature overview and project introduction
2. **About**: Detailed information about the project and technology
3. **Test**: Main page for sentiment analysis with results display
4. **Login/Register**: User authentication pages
5. **Contact**: Contact form and information
6. **Error Pages**: Custom 404 and 500 error pages

### Features

- **Sentiment Analysis**: Analyze any text for positive, negative, or neutral sentiment
- **Confidence Scores**: Get numerical scores indicating sentiment strength
- **Explanations**: AI-generated explanations for sentiment classification
- **History Saving**: Save analysis history for registered users
- **API Access**: RESTful API endpoint for programmatic access

## Implementation Details

### Groq API Integration

The project uses Groq's language models to perform sentiment analysis. The integration is handled by a dedicated service class that:

1. Formats the text for analysis
2. Sends a well-structured prompt to Groq's API
3. Processes the response to extract sentiment, score, and explanation
4. Handles error cases gracefully

### Database Schema

The database includes two main tables:
- **Users**: Stores user information and authentication data
- **SentimentAnalyses**: Records analysis history linked to users

### Security Considerations

- Passwords are securely hashed using Werkzeug's password hashing
- CSRF protection on all forms
- Environment variables for sensitive configuration
- Input validation to prevent injection attacks

## Deployment Requirements

- Python 3.8+
- Groq API Key
- Flask and dependencies listed in requirements.txt
- SQLite database (can be easily switched to PostgreSQL for production)

## Future Improvements

- Batch analysis for multiple texts
- Advanced visualization of sentiment patterns
- Multi-language support
- Emotion detection beyond simple sentiment
- User dashboard with analysis statistics