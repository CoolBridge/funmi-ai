# Decision Agent
# Looks at scores + requirements and recommends the best country

def recommend_pathway(scores):
    """
    Takes the scores from assessment_agent and picks the best country.
    Simple but effective logic.
    """

    uk = scores["uk_score"]
    usa = scores["usa_score"]
    canada = scores["canada_score"]

    # Find the highest score
    best_score = max(uk, usa, canada)

    if best_score == uk:
        recommended = "United Kingdom"
        flag = "🇬🇧"
        reason = (
            f"Your profile scores highest for the UK ({uk}%). "
            "The UK has a faster pathway (6-12 months), high nurse demand, "
            "and the NMC process suits your background well."
        )
        timeline = "6–12 months"
        exam = "CBT + OSCE"

    elif best_score == usa:
        recommended = "United States"
        flag = "🇺🇸"
        reason = (
            f"Your profile scores highest for the USA ({usa}%). "
            "The US offers the highest salaries and strong career growth, "
            "though the pathway takes longer (12-24 months)."
        )
        timeline = "12–24 months"
        exam = "NCLEX-RN"

    else:
        recommended = "Canada"
        flag = "🇨🇦"
        reason = (
            f"Your profile scores highest for Canada ({canada}%). "
            "Canada offers a clear PR pathway and strong work-life balance "
            "for internationally educated nurses."
        )
        timeline = "12–18 months"
        exam = "NCLEX-RN"

    # Calculate confidence based on how far ahead the top score is
    scores_list = [uk, usa, canada]
    scores_list.remove(best_score)
    gap = best_score - max(scores_list)

    if gap >= 15:
        confidence = "High"
    elif gap >= 8:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "recommended": recommended,
        "flag": flag,
        "reason": reason,
        "timeline": timeline,
        "exam": exam,
        "confidence": confidence,
        "score": best_score
    }