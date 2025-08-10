from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 🔒 Required for session

# Load MCQs from JSON file - commission_mcqs हटाकर सीधे लिस्ट लोड करें
QUESTIONS_FILE = os.path.join('mcqs', 'questions.json')
with open(QUESTIONS_FILE, encoding='utf-8') as f:
    questions = json.load(f)  # commission_mcqs हटाया गया

@app.route('/')
def home():
    return redirect('/password')

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == 'mahadev':
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
        correct_keys = q["answer"]
        if isinstance(correct_keys, str):
            correct_keys = [correct_keys]

        user_keys = user_answers.get(qid, [])

        correct_texts = [f"{key} – {q['options'][key]}" for key in correct_keys]
        user_texts = [f"{key} – {q['options'][key]}" for key in user_keys if key in q['options']]

        is_correct = set(map(str.strip, correct_keys)) == set(map(str.strip, user_keys))

        explanation = q.get("explanation", "कोई व्याख्या उपलब्ध नहीं है।")

        results.append({
            "id": qid,
            "question": q["question"],
            "correct": correct_texts,
            "selected": user_texts,
            "is_correct": is_correct,
            "explanation": explanation
        })

    return render_template("result.html", results=results)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/password')

if __name__ == '__main__':
    app.run(debug=True)
