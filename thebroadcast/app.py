from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sample news data (In real implementation, this would come from a database)
news_data = []

# Log file path
log_file = "log.txt"

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# News Page
@app.route('/news')
def news():
    return render_template('news.html', news_data=news_data)

# Contact Us Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Add News Page
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == 'POST':
        headlines = request.form['headlines']
        description = request.form['description']
        author_name = request.form['author_name']
        category = request.form['category']
        
        news_item = {
            'headlines': headlines,
            'description': description,
            'author_name': author_name,
            'category': category
        }
        
        # Add news to the news_data list
        news_data.append(news_item)
        
        log_action(f"News added: {headlines} by {author_name}")
        
        return redirect(url_for('news'))
    
    return render_template('add_news.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if credentials are valid (In real implementation, this would check from a database)
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['role'] = 'admin'
            log_action(f"Admin logged in: {username}")
            return redirect(url_for('home'))
        elif username == 'user' and password == 'user':
            session['logged_in'] = True
            session['role'] = 'user'
            log_action(f"User logged in: {username}")
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, try again."
    
    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # In real implementation, save the user details to a database
        log_action(f"User registered: {username}")
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Log Action (Track user login or actions like adding/updating news)
def log_action(action):
    with open(log_file, 'a') as file:
        file.write(f"{datetime.now()} - {action}\n")

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
