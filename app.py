from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random, os, uuid

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
app.password = os.getenv('PASSWORD', 'fallback_password')

# Database Setup (SQLite)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'responses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Survey Questions
questions = [
    "What is your favorite color?",
    "What is your favorite food?",
    "What is your dream travel destination?",
    "What is your favorite hobby?",
    "What is your favorite animal?"
]

# Database Model for Storing Responses
class Response(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

# Create tables when app starts
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def survey():
    # Check if the user already submitted
    if session.get('submitted'):
        return redirect(url_for('show_results'))

    if request.method == 'POST':
        try:
            responses = [(question, request.form.get(question, '')) for question in questions]
            random.shuffle(responses)
            
            for question, answer in responses:
                if answer:
                    new_response = Response(question=question, answer=answer)
                    db.session.add(new_response)
            db.session.commit()
            session['submitted'] = True
            return redirect(url_for('show_results'))
        except Exception as e:
            db.session.rollback()  # 🔄 Rollback in case of failure
            print(f"🔥 Database Commit Failed: {str(e)}")  # Print error in terminal

    return render_template('survey.html', questions=questions)

@app.route('/results', methods=['GET','POST'])
def show_results():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == app.password:
            session['authenticated'] = True  # ✅ Allow access
            return redirect(url_for('show_results'))
        else:
            return render_template('password_prompt.html', error="Incorrect password")

    # 🔒 Check if the user is authenticated
    if not session.get('authenticated'):
        return render_template('password_prompt.html')

    # Fetch and display results if authenticated
    all_responses = {q: [] for q in questions}
    responses = Response.query.order_by(db.func.random()).all()
    
    for response in responses:
        all_responses[response.question].append(response.answer)

    return render_template('results.html', response_lists=all_responses)


if __name__ == '__main__':
    app.run(debug=True)