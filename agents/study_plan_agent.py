import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def get_azure_client():
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_API_KEY"),
        api_version="2024-08-01-preview",
        azure_endpoint="https://funmi-ai-resource.openai.azure.com/"
    )
    return client

def generate_study_plan(country, qualification, experience_years, english_level, exam):
    client = get_azure_client()
    prompt = f"""
    You are an expert nurse migration consultant.
    Generate a detailed 8-week study plan for a nurse with this profile:
    - Qualification: {qualification}
    - Experience: {experience_years} years
    - English Level: {english_level}
    - Destination Country: {country}
    - Key Exam to Pass: {exam}

    Format EXACTLY like this:

    WEEK 1: [Topic Name]
    [2-3 sentences describing what to study and how]

    WEEK 2: [Topic Name]
    [2-3 sentences]

    WEEK 3: [Topic Name]
    [2-3 sentences]

    WEEK 4: [Topic Name]
    [2-3 sentences]

    WEEK 5: [Topic Name]
    [2-3 sentences]

    WEEK 6: [Topic Name]
    [2-3 sentences]

    WEEK 7: [Topic Name]
    [2-3 sentences]

    WEEK 8: [Topic Name]
    [2-3 sentences]

    TIPS:
    [3 specific tips for this nurse's profile]
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert nurse migration consultant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content

def generate_mock_questions(exam, country):
    client = get_azure_client()
    prompt = f"""
    You are an expert {exam} exam coach for nurses migrating to {country}.
    Generate exactly 5 multiple choice questions for the {exam} exam.

    Format EXACTLY like this:

    Q1: [Question text]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    ANSWER: [Correct letter]
    EXPLANATION: [One sentence why]

    Q2: [Question text]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    ANSWER: [Correct letter]
    EXPLANATION: [One sentence why]

    Q3: [Question text]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    ANSWER: [Correct letter]
    EXPLANATION: [One sentence why]

    Q4: [Question text]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    ANSWER: [Correct letter]
    EXPLANATION: [One sentence why]

    Q5: [Question text]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    ANSWER: [Correct letter]
    EXPLANATION: [One sentence why]
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are an expert {exam} exam coach."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content

def parse_questions(raw_text):
    questions = []
    current_q = None
    lines = raw_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Q") and ":" in line and len(line) < 200:
            if current_q:
                questions.append(current_q)
            current_q = {
                "question": line.split(":", 1)[1].strip(),
                "options": [],
                "answer": "",
                "explanation": ""
            }
        elif line.startswith(("A)", "B)", "C)", "D)")) and current_q:
            current_q["options"].append(line)
        elif line.startswith("ANSWER:") and current_q:
            current_q["answer"] = line.replace("ANSWER:", "").strip()
        elif line.startswith("EXPLANATION:") and current_q:
            current_q["explanation"] = line.replace("EXPLANATION:", "").strip()
    if current_q:
        questions.append(current_q)
    return questions
