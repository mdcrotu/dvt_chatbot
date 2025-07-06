import yaml
from rapidfuzz import fuzz, process

def load_answers(path='custom_answers.yaml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def find_answer(question, answers, threshold=50, debug=False):
    question_clean = question.lower().strip()

    # Exact match first
    for qa in answers:
        if question_clean == qa['question'].lower().strip():
            return qa['answer']

    # Fuzzy match with token set ratio
    questions_list = [qa['question'] for qa in answers]
    best_match, score, _ = process.extractOne(
        question, questions_list, scorer=fuzz.token_set_ratio
    )

    if debug:
        print(f"[DEBUG] Best fuzzy match: '{best_match}' with score {score}")

    if score >= threshold:
        for qa in answers:
            if qa['question'] == best_match:
                return qa['answer']

    return None
