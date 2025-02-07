from flask import Flask, render_template, request, session, redirect, url_for
import os, json, random

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
app.password = os.getenv('PASSWORD', 'fallback_password')

# Define Survey Questions
questions = [
    "What is your favorite color?",
    "What is your favorite food?",
    "What is your dream travel destination?",
]

# File to store responses
RESPONSES_FILE = "responses.json"

# Load responses from file (if exists)
def load_responses():
    if os.path.exists(RESPONSES_FILE):
        try:
            with open(RESPONSES_FILE, "r") as file:
                return json.load(file)
        except:
            return {q: [] for q in questions}
    return {q: [] for q in questions}  # Default structure

# Save responses to file
def save_responses():
    with open(RESPONSES_FILE, "w") as file:
        json.dump(all_responses, file, indent=4)

# Global dictionary to store responses
all_responses = load_responses()

@app.route('/', methods=['GET', 'POST'])
def survey():
    if session.get('submitted'):
        return redirect(url_for('show_results'))

    if request.method == 'POST':
        responses = {question: request.form.get(question, '') for question in questions}
        
        # Store responses in dictionary and shuffle 
        for question, answer in responses.items():
            if answer:
                all_responses[question].append(answer)
                random.shuffle(all_responses[question])

        save_responses()  # 🔥 Save to file
        
        session['submitted'] = True
        return redirect(url_for('show_results'))

    return render_template('survey.html', questions=questions)

@app.route('/results', methods=['GET', 'POST'])
def show_results():
    auth = False
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == app.password:
            # session['authenticated'] = True  # ✅ Grant access
            auth = True
            return render_template('results.html', response_lists=all_responses)
        else:
            print("❌ Incorrect password. Try again.")
            return render_template('password_prompt.html')

    # if not session.get('authenticated'):
    if not auth: 
        return render_template('password_prompt.html')

    return render_template('results.html', response_lists=all_responses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
