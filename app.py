import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.urls import url_parse
from models.user import db, User, SentimentAnalysis
from services.sentiment import SentimentAnalyzer
from utils.helpers import flash_errors, get_sentiment_color, get_sentiment_emoji
from config import Config
from datetime import datetime

# Create Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Create the database directory if it doesn't exist
db_path = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(db_path, 'db', 'db.sqlite3')
os.makedirs(os.path.dirname(db_file), exist_ok=True)

# Set the absolute path for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
sentiment_analyzer = SentimentAnalyzer()

# Create database tables
with app.app_context():
    db.create_all()

# Context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.now}

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Form classes
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class SentimentForm(FlaskForm):
    text = TextAreaField('Text for Sentiment Analysis', validators=[DataRequired()])
    submit = SubmitField('Analyze')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 120)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# Route definitions
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = SentimentForm()
    result = None
    
    if form.validate_on_submit():
        text = form.text.data
        
        # Analyze the sentiment
        result = sentiment_analyzer.analyze(text)
        
        # Save the analysis if user is logged in
        if current_user.is_authenticated:
            analysis = SentimentAnalysis(
                text=text,
                sentiment=result['sentiment'],
                score=result['score'],
                user_id=current_user.id
            )
            db.session.add(analysis)
            db.session.commit()
            
            flash('Sentiment analysis has been saved to your history!', 'success')
        
        # Add UI helper attributes to the result
        result['color'] = get_sentiment_color(result['sentiment'], result['score'])
        result['emoji'] = get_sentiment_emoji(result['sentiment'])
    
    return render_template('test.html', form=form, result=result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
        
        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        
        return redirect(next_page)
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.password = form.password.data
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    if form.errors:
        flash_errors(form)
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would send an email or save the contact message
        # For this demo, we'll just show a success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for sentiment analysis"""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    result = sentiment_analyzer.analyze(data['text'])
    return jsonify(result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)