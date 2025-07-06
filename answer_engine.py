import yaml

def load_answers(path='custom_answers.yaml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def find_answer(question, answers):
    question = question.lower().strip()
    for qa in answers:
        if question == qa['question'].lower().strip():
            return qa['answer']
    return None
