import yaml
from rapidfuzz import fuzz, process

def load_answers(path='custom_answers.yaml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def find_answer(question, answers, threshold=80):
    question_clean = question.lower().strip()

    # Exact match first
    for qa in answers:
        if question_clean == qa['question'].lower().strip():
            return qa['answer']

    # Fuzzy match fallback
    questions_list = [qa['question'] for qa in answers]
    best_match = process.extractOne(question, questions_list, scorer=fuzz.ratio)

    if best_match and best_match[1] >= threshold:
        for qa in answers:
            if qa['question'] == best_match[0]:
                return qa['answer']

    return None
