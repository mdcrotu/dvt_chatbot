import yaml
from rapidfuzz import fuzz, process
from dvt_chatbot.config import CUSTOM_ANSWERS_FILE, DVT_GUIDE_FILE
from dvt_chatbot.search_engine import load_guide_chunks, find_best_semantic_match

def load_answers(filepath=None):
    path = filepath or CUSTOM_ANSWERS_FILE
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def find_answer_with_score(question, answers, threshold=70, debug=False):
    q = question.strip()
    
    # Exact match
    for qa in answers:
        if q.lower() == qa['question'].lower().strip():
            if debug:
                print(f"[DEBUG] Exact match on '{qa['question']}' (score 100)")
            return qa['answer'], qa['question'], 100

    # Fuzzy match using token set ratio
    questions_list = [qa['question'] for qa in answers]
    match = process.extractOne(q, questions_list, scorer=fuzz.token_set_ratio)

    if match:
        best_match, score, _ = match
        if debug:
            print(f"[DEBUG] Fuzzy best match: '{best_match}' with score {score}")
        if score >= threshold:
            for qa in answers:
                if qa['question'] == best_match:
                    return qa['answer'], qa['question'], int(score)
        elif debug:
            return None, best_match, int(score)

    return None

def get_answer_with_fallback(user_question, model=None):
    # Try fuzzy match first
    custom_answers = load_answers()
    fuzzy_result = find_answer_with_score(user_question, custom_answers)
    if fuzzy_result:
        return {
            "answer": fuzzy_result[0],
            "source": "custom",
            "score": fuzzy_result[2],
            "suggested_question": fuzzy_result[1],
        }

    # Fall back to semantic search
    chunks = load_guide_chunks(DVT_GUIDE_FILE)
    match = find_best_semantic_match(user_question, chunks, threshold=0.0, model=model)

    if match:
        return {
            "answer": match["content"],
            "source": "guide",
            "score": match["score"],
            "title": match["title"],
            "url": match["url"],
        }

    # Nothing matched
    return None
