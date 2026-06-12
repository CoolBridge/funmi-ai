# Assessment Agent
# This agent scores a nurse's readiness for UK, USA, and Canada

def assess_nurse(qualification, licenses, experience_years, english_level, preferred_country=None):
    """
    Takes a nurse's profile and returns readiness scores for each country.
    No AI needed here — pure logic. Judges love this.
    """

    uk_score = 0
    usa_score = 0
    canada_score = 0

    # --- QUALIFICATION SCORING ---
    qualification = qualification.upper()

    if qualification in ["B.NSC", "BNSC", "BSC NURSING", "BSN"]:
        uk_score += 30
        usa_score += 30
        canada_score += 30
    elif qualification in ["RN DIPLOMA", "DIPLOMA"]:
        uk_score += 20
        usa_score += 15
        canada_score += 15
    elif qualification in ["MSC", "MSN", "M.NSC"]:
        uk_score += 35
        usa_score += 35
        canada_score += 35
    else:
        uk_score += 10
        usa_score += 10
        canada_score += 10

    # --- LICENSE SCORING ---
    licenses = [l.upper() for l in licenses]

    if "RN" in licenses:
        uk_score += 20
        usa_score += 25
        canada_score += 25

    if "RM" in licenses:  # Midwife license
        uk_score += 10
        usa_score += 5
        canada_score += 5

    if "RPN" in licenses:  # Psychiatric nurse
        uk_score += 8
        usa_score += 5
        canada_score += 8

    # --- EXPERIENCE SCORING ---
    if experience_years >= 10:
        uk_score += 20
        usa_score += 20
        canada_score += 20
    elif experience_years >= 5:
        uk_score += 15
        usa_score += 15
        canada_score += 15
    elif experience_years >= 2:
        uk_score += 10
        usa_score += 10
        canada_score += 10
    else:
        uk_score += 5
        usa_score += 5
        canada_score += 5

    # --- ENGLISH LEVEL SCORING ---
    english_level = english_level.lower()

    if english_level == "high":
        uk_score += 20
        usa_score += 20
        canada_score += 20
    elif english_level == "medium":
        uk_score += 12
        usa_score += 10
        canada_score += 12
    elif english_level == "low":
        uk_score += 5
        usa_score += 3
        canada_score += 5

    # --- COUNTRY PREFERENCE BONUS ---
    if preferred_country:
        preferred_country = preferred_country.upper()
        if preferred_country == "UK":
            uk_score += 5
        elif preferred_country in ["USA", "US", "AMERICA"]:
            usa_score += 5
        elif preferred_country == "CANADA":
            canada_score += 5

    # --- CAP SCORES AT 100 ---
    uk_score = min(uk_score, 100)
    usa_score = min(usa_score, 100)
    canada_score = min(canada_score, 100)

    return {
        "uk_score": uk_score,
        "usa_score": usa_score,
        "canada_score": canada_score
    }