from flask import Flask, request, render_template
from answer_engine import load_answers, find_answer

app = Flask(__name__)
answers = load_answers()

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        answer = find_answer(question, answers)
        response = answer if answer else "Sorry, I don’t know yet. You can add this to the knowledge base."
    return render_template('index.html', response=response)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        while True:
            question = input("Ask a DVT IDE question (or 'exit'): ")
            if question.lower() in ('exit', 'quit'):
                break
            answer = find_answer(question, answers, debug=True)
            print(answer if answer else "Sorry, I don’t know yet.")
    else:
        app.run(debug=True)
