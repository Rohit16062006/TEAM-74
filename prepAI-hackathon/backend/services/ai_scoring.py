def score_answer(user_answer, expected_answer):
    if not expected_answer:
        # Fallback if no expected answer is provided
        return {
            "technical": 0,
            "behavioral": 70,
            "comm": 68,
            "readiness": 30
        }

    similarity = len(set(user_answer.split()) & set(expected_answer.split())) / len(expected_answer.split())
    technical = int(similarity * 100)
    behavioral = 70
    comm = 68
    readiness = int(0.5 * technical + 0.3 * behavioral + 0.2 * comm)
    return {
        "technical": technical,
        "behavioral": behavioral,
        "comm": comm,
        "readiness": readiness
    }
