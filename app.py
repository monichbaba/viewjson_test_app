from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session

# Load MCQs from JSON file
QUESTIONS_FILE = os.path.join('mcqs', 'questions.json')
with open(QUESTIONS_FILE, encoding='utf-8') as f:
    questions = json.load(f)

@app.route('/')
def home():
    return redirect('/password')

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == 'harharmahadev':  # ✅ Set your own password here
            session['authenticated'] = True
            return redirect('/test')
        else:
            return render_template('password.html', error="❌ Incorrect password")
    return render_template('password.html')

@app.route('/test', methods=['GET'])
def test():
    if not session.get('authenticated'):
        return redirect('/password')
    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    if not session.get('authenticated'):
        return redirect('/password')

    user_answers = {}
    for q in questions:
        qid = str(q["id"])
        selected_options = request.form.getlist(f'q{qid}')
        user_answers[qid] = selected_options

    results = []
    for q in questions:
        qid = str(q["id"])
        correct = q["answer"]
        if isinstance(correct, str):
            correct = [correct]  # Ensure it's a list
        user = user_answers.get(qid, [])

        # Compare sets after stripping
        is_correct = set(map(str.strip, correct)) == set(map(str.strip, user))

        results.append({
            "question": q["question"],
            "correct": correct,
            "user": user,
            "is_correct": is_correct
        })

    return render_template("result.html", results=results)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/password')

if __name__ == '__main__':
    app.run(debug=True)
