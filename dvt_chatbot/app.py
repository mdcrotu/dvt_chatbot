from flask import Flask, request, render_template
from .answer_engine import load_answers, find_answer_with_score

app = Flask(__name__)
answers = load_answers()

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    match_question = None
    match_score = None
    suggestion = None
    if request.method == 'POST':
        result = find_answer_with_score(request.form['question'], answers, threshold=70, debug=False)
        if result and result[0]:
            response, match_question, match_score = result
        else:
            response = "Sorry, I don’t know yet. You can add this to the knowledge base."
            if result:
                _, mq, ms = result
                suggestion = f"Did you mean '{mq}'? (score: {ms})"
    return render_template('index.html', response=response, match_question=match_question,
                           match_score=match_score, suggestion=suggestion)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        while True:
            q = input("Ask a DVT IDE question (or 'exit'): ")
            if q.lower() in ('exit', 'quit'):
                break
            result = find_answer_with_score(q, answers, threshold=70, debug=True)
            if result and result[0]:
                ans, mq, ms = result
                print(f"{ans}  (matched: '{mq}' with score {ms})")
            else:
                if result:
                    _, mq, ms = result
                    print(f"Sorry, I don’t know yet. (suggested: '{mq}' score {ms})")
                else:
                    print("Sorry, I don’t know yet.")
    else:
        app.run(debug=True)
