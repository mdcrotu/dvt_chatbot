from flask import Flask, request, render_template
from .answer_engine import get_answer_with_fallback

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    match_question = None
    match_score = None
    suggestion = None
    source = None

    if request.method == 'POST':
        user_question = request.form['question']
        result = get_answer_with_fallback(user_question)

        if result:
            response = result['answer']
            match_score = result.get('score')
            source = result.get('source')
            if source == 'custom':
                match_question = result.get('suggested_question')
                if match_question and match_question.lower() != user_question.strip().lower():
                    suggestion = f"Did you mean '{match_question}'? (score: {match_score})"
        else:
            response = "Sorry, I don’t know yet. You can add this to the knowledge base."

    return render_template('index.html', response=response, match_question=match_question,
                           match_score=match_score, suggestion=suggestion, source=source)

def main_cli():
    while True:
        q = input("Ask a DVT IDE question (or 'exit'): ")
        if q.lower() in ('exit', 'quit'):
            break
        else:
            from dvt_chatbot.answer_engine import get_answer_with_fallback
            fallback = get_answer_with_fallback(q)
            if fallback:
                print("\n---")
                if fallback["source"] == "guide":
                    print(f"**📘 Guide Match: {fallback['title']}**\n")
                    print(f"{fallback['answer'].strip()}\n")
                    print(f"[🔗 View in DVT Guide]({fallback['url']})")
                elif fallback["source"] == "custom":
                    print(f"**🧠 Custom Answer**\n")
                    print(f"{fallback['answer'].strip()}")
                    if fallback.get("suggested_question") and fallback["suggested_question"] != q:
                        print(f"\n_(Matched: '{fallback['suggested_question']}' with score {fallback['score']})_")
                else:
                    print(fallback["answer"].strip())
                print("---\n")
            else:
                print("Sorry, I don’t know yet.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        main_cli()
    else:
        app.run(debug=True)
