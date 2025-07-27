from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/test')
def test():
    with open('questions.json', encoding='utf-8') as f:
        questions = json.load(f)
    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    with open('questions.json', encoding='utf-8') as f:
        questions = json.load(f)

    submitted = {}
    for q in questions:
        qid = str(q['id'])
        submitted[qid] = request.form.getlist(f"q{qid}")

    results = []
    for q in questions:
        qid = str(q['id'])
        correct = set(q['answer'])
        selected = set(submitted.get(qid, []))
        results.append({
            "question": q["question"],
            "options": q["options"],
            "correct": correct,
            "selected": selected,
            "is_correct": correct == selected
        })

    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
