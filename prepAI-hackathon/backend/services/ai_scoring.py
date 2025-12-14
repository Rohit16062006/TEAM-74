def score_answer(user_answer: str, expected_answer: str) -> dict:
    if not expected_answer or len(expected_answer.split()) == 0:
        return {
            "technical_score": 0,
            "behavioral_score": 70,
            "comm_score": 68,
            "readiness_score": 30
        }

    user_words = set(user_answer.lower().split())
    expected_words = set(expected_answer.lower().split())
    
    if not expected_words:
        similarity = 0
    else:
        similarity = len(user_words & expected_words) / len(expected_words)
    
    # Cap similarity at 1.0
    if similarity > 1: similarity = 1
    
    # Better logic: if similarity is low but length is good, give some points for effort
    if len(user_answer) > 20 and similarity < 0.2:
        similarity += 0.2

    technical = int(similarity * 100)
    behavioral = 85 # Mocked
    comm = 90      # Mocked
    readiness = int(0.5 * technical + 0.3 * behavioral + 0.2 * comm)
    
    return {
        "technical_score": technical,
        "behavioral_score": behavioral,
        "comm_score": comm,
        "readiness_score": readiness
    }
