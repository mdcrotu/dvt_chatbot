import yaml
from rapidfuzz import fuzz, process

def load_answers(path='custom_answers.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def find_answer_with_score(question, answers, threshold=70, debug=False):
    q = question.strip()
    # Exact match
    for qa in answers:
        if q.lower() == qa['question'].lower().strip():
            if debug:
                print(f"[DEBUG] Exact match on '{qa['question']}' (score 100)")
            return qa['answer'], qa['question'], 100

    # Fuzzy match with token set ratio
    questions_list = [qa['question'] for qa in answers]
    best_match, score, _ = process.extractOne(
        q, questions_list,
        scorer=fuzz.token_set_ratio
    )

    if debug:
        print(f"[DEBUG] Fuzzy best match: '{best_match}' with score {score}")

    if score >= threshold:
        for qa in answers:
            if qa['question'] == best_match:
                return qa['answer'], qa['question'], int(score)

    return None if not debug else (None, best_match, int(score))
