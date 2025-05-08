from flask import flash, url_for, redirect
from functools import wraps
from flask_login import current_user

def flash_errors(form):
    """
    Flash errors from a Flask-WTF form
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", "error")

def login_required(f):
    """
    Custom login_required decorator that flashes a message
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def get_sentiment_color(sentiment, score=None):
    """
    Returns a TailwindCSS color class based on sentiment
    """
    if sentiment.lower() == 'positive':
        if score and score > 0.7:
            return 'bg-green-600'
        return 'bg-green-500'
    elif sentiment.lower() == 'negative':
        if score and score < -0.7:
            return 'bg-red-600'
        return 'bg-red-500'
    else:  # neutral
        return 'bg-gray-500'

def get_sentiment_emoji(sentiment):
    """
    Returns an emoji based on sentiment
    """
    if sentiment.lower() == 'positive':
        return '😊'
    elif sentiment.lower() == 'negative':
        return '😔'
    else:  # neutral
        return '😐'