from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for session management

# ✅ Path to questions.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_PATH = os.path.join(BASE_DIR, 'mcqs', 'questions.json')

# 🔐 Password login route
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == "ias123":  # 🔑 Password here
            session['authenticated'] = True
            return redirect(url_for("test"))
        else:
            error = "❌ Incorrect password"
    return render_template("password.html", error=error)

# 📋 Test page
@app.route("/test", methods=["GET"])
def test():
    if not session.get('authenticated'):
        return redirect('/')
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return render_template("test.html", questions=questions)

# ✅ Submit + Result page
@app.route("/submit", methods=["POST"])
def submit():
    if not session.get('authenticated'):
        return redirect('/')
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    score = 0
    results = []
    for q in questions:
        qid = str(q["id"])
        correct_ans = q["answer"]
        selected_ans = request.form.get(qid)

        is_correct = (selected_ans == correct_ans)
        if is_correct:
            score += 1

        results.append({
            "question": q["question"],
            "correct": correct_ans,
            "selected": selected_ans,
            "status": "✅" if is_correct else "❌"
        })

    return render_template("result.html", results=results, score=score, total=len(questions))

# 🚀 Run server
if __name__ == '__main__':
    app.run(debug=True)
