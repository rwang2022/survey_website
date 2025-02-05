from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Define survey questions
questions = [
    "What is your favorite color?",
    "What is your favorite food?",
    "What is your dream travel destination?",
    "What is your favorite hobby?",
    "What is your favorite animal?"
]

# Store all responses globally (in-memory storage, resets on restart)
all_responses = {q: [] for q in questions}

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        responses = {question: request.form.get(question, '') for question in questions}
        
        # Store responses for each question
        for question, answer in responses.items():
            if answer:
                all_responses[question].append(answer)
                    
    return render_template('survey.html', questions=questions)


@app.route('/results', methods=['GET', 'POST'])
def show_results():
    # Shuffle responses within each question
    for question in all_responses:
        random.shuffle(all_responses[question])
    
    return render_template('results.html', response_lists=all_responses)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Define survey questions
questions = [
    "What is your favorite color?",
    "What is your favorite food?",
    "What is your dream travel destination?",
    "What is your favorite hobby?",
    "What is your favorite animal?"
]

# Store all responses globally (in-memory storage, resets on restart)
all_responses = {q: [] for q in questions}

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        if 'save' in request.form:
            session['responses'] = {question: request.form.get(question, '') for question in questions}
            return render_template('survey.html', questions=questions, saved_responses=session['responses'], message="Your responses have been saved.")
        
        responses = {question: request.form.get(question, '') for question in questions}
        
        # Store responses for each question
        for question, answer in responses.items():
            if answer:
                all_responses[question].append(answer)
        
        # Shuffle responses within each question
        for question in all_responses:
            random.shuffle(all_responses[question])
        
        session.pop('responses', None)  # Clear saved responses after submission
        return render_template('results.html', response_lists=all_responses)
    
    saved_responses = session.get('responses', {})
    return render_template('survey.html', questions=questions, saved_responses=saved_responses)

if __name__ == '__main__':
    app.run(debug=True)
