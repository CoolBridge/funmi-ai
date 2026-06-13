import streamlit as st
from agents.assessment_agent import assess_nurse
from agents.decision_agent import recommend_pathway
from agents.study_plan_agent import generate_study_plan, generate_mock_questions, parse_questions

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Funmi AI",
    page_icon="🏥",
    layout="centered"
)

# --- SESSION STATE INIT ---
if 'scores' not in st.session_state:
    st.session_state.scores = None
if 'recommendation' not in st.session_state:
    st.session_state.recommendation = None
if 'study_plan' not in st.session_state:
    st.session_state.study_plan = None
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'qualification' not in st.session_state:
    st.session_state.qualification = None
if 'experience' not in st.session_state:
    st.session_state.experience = None
if 'english_level' not in st.session_state:
    st.session_state.english_level = None
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

# --- HEADER ---
st.title("🏥 Funmi AI")
st.subheader("Global Nursing Career & Migration Assistant")
st.markdown("*An AI-powered nursing career coach that helps nurses assess eligibility, prepare for licensing exams, and build personalized migration pathways for countries such as the UK, USA, and Canada.*")
st.divider()

# --- SIDEBAR PROGRESS ---
st.sidebar.title("Your Progress")
st.sidebar.markdown("✅ Step 1: Fill your profile")
st.sidebar.markdown("✅ Step 2: Get assessment" if st.session_state.scores else "⬜ Step 2: Get assessment")
st.sidebar.markdown("✅ Step 3: See recommendation" if st.session_state.recommendation else "⬜ Step 3: See recommendation")
st.sidebar.markdown("✅ Step 4: Get study plan" if st.session_state.study_plan else "⬜ Step 4: Get study plan")
st.sidebar.markdown("✅ Step 5: Mock exam" if st.session_state.quiz_submitted else "⬜ Step 5: Mock exam")

# --- SECTION 1: NURSE PROFILE ---
st.header("📋 Step 1: Your Nurse Profile")
st.markdown("Tell us about yourself so we can assess your readiness.")

col1, col2 = st.columns(2)

with col1:
    qualification = st.selectbox(
        "Highest Qualification",
        ["B.NSc", "Diploma", "MSc", "BSN", "Other"]
    )
    experience = st.slider(
        "Years of Experience",
        min_value=0,
        max_value=30,
        value=3
    )

with col2:
    english_level = st.selectbox(
        "English Proficiency",
        ["High", "Medium", "Low"]
    )
    preferred_country = st.selectbox(
        "Preferred Destination (optional)",
        ["No Preference", "UK", "USA", "Canada"]
    )

st.markdown("#### Your Licenses")
licenses = st.multiselect(
    "Select all licenses you currently hold",
    ["RN", "RM", "RPN"],
    default=["RN"]
)

st.divider()

# --- ASSESS BUTTON ---
if st.button("🔍 Assess My Readiness", use_container_width=True):
    if not licenses:
        st.error("⚠️ Please select at least one license.")
    else:
        country_pref = None if preferred_country == "No Preference" else preferred_country
        st.session_state.scores = assess_nurse(
            qualification=qualification,
            licenses=licenses,
            experience_years=experience,
            english_level=english_level,
            preferred_country=country_pref
        )
        st.session_state.recommendation = recommend_pathway(st.session_state.scores)
        st.session_state.qualification = qualification
        st.session_state.experience = experience
        st.session_state.english_level = english_level
        st.session_state.study_plan = None
        st.session_state.questions = None
        st.session_state.quiz_questions = None
        st.session_state.user_answers = {}
        st.session_state.quiz_submitted = False

# --- SHOW RESULTS IF ASSESSED ---
if st.session_state.scores:
    scores = st.session_state.scores
    recommendation = st.session_state.recommendation

    # --- SECTION 2: SCORES ---
    st.header("📊 Step 2: Your Readiness Scores")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🇬🇧 United Kingdom", f"{scores['uk_score']}%")
        st.progress(scores['uk_score'] / 100)
    with col2:
        st.metric("🇺🇸 United States", f"{scores['usa_score']}%")
        st.progress(scores['usa_score'] / 100)
    with col3:
        st.metric("🇨🇦 Canada", f"{scores['canada_score']}%")
        st.progress(scores['canada_score'] / 100)

    st.divider()

    # --- SECTION 3: RECOMMENDATION ---
    st.header("🎯 Step 3: Recommended Pathway")
    st.success(f"### {recommendation['flag']} {recommendation['recommended']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Timeline**\n\n{recommendation['timeline']}")
    with col2:
        st.info(f"**Key Exam**\n\n{recommendation['exam']}")
    with col3:
        st.info(f"**Confidence**\n\n{recommendation['confidence']}")

    st.markdown("#### Why this recommendation?")
    st.write(recommendation['reason'])

    st.divider()

    # --- SECTION 4: REQUIREMENTS ---
    st.header("📋 Step 4: What You Need")
    country_key = recommendation['recommended']

    if "Kingdom" in country_key:
        st.markdown("""
        ### Your UK Checklist
        - ✅ Valid RN License from your home country
        - 📝 Register with NMC (Nursing & Midwifery Council)
        - 📚 Pass the **CBT** (Computer Based Test)
        - 🗣️ Pass **IELTS 7.0+** or **OET Grade B**
        - ✈️ Travel to UK for **OSCE** exam
        - 📄 Good Standing Certificate from home country
        """)
    elif "United States" in country_key:
        st.markdown("""
        ### Your USA Checklist
        - ✅ Valid RN License from your home country
        - 📝 CGFNS Credential Evaluation
        - 📚 Pass the **NCLEX-RN** exam
        - 🗣️ Pass **TOEFL** or **IELTS**
        - 📄 VisaScreen Certificate
        - 🏛️ Apply to your chosen State Board
        """)
    else:
        st.markdown("""
        ### Your Canada Checklist
        - ✅ Valid RN License from your home country
        - 📝 NNAS Credential Assessment
        - 📚 Pass the **NCLEX-RN** exam
        - 🗣️ Pass **IELTS** or **CELBAN**
        - 🏛️ Apply to Provincial Nursing College
        - 🍁 Explore Express Entry PR pathway
        """)

    st.divider()

    # --- SECTION 5: STUDY PLAN ---
    st.header("📚 Step 5: Your AI Study Plan")
    st.markdown("Click below to generate a personalized 8-week study plan.")

    if st.button("🧠 Generate My Study Plan", use_container_width=True):
        try:
            with st.spinner("Funmi AI is building your personalized study plan..."):
                st.session_state.study_plan = generate_study_plan(
                    country=recommendation['recommended'],
                    qualification=st.session_state.qualification,
                    experience_years=st.session_state.experience,
                    english_level=st.session_state.english_level,
                    exam=recommendation['exam']
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")

    if st.session_state.study_plan:
        st.success("Your study plan is ready!")
        weeks = st.session_state.study_plan.split("WEEK ")
        for week in weeks:
            if week.strip():
                lines = week.strip().split("\n")
                week_title = "WEEK " + lines[0]
                week_content = "\n".join(lines[1:]).strip()
                with st.expander(week_title):
                    st.write(week_content)

        st.divider()

        # --- SECTION 6: MOCK EXAM ---
        st.header("📝 Step 6: Mock Exam Practice")
        st.markdown("Test your knowledge with Funmi-AI generated questions.")

        if st.button("🎯 Generate Mock Questions", use_container_width=True):
            try:
                with st.spinner("Generating exam questions..."):
                    raw = generate_mock_questions(
                        exam=recommendation['exam'],
                        country=recommendation['recommended']
                    )
                    st.session_state.quiz_questions = parse_questions(raw)
                    st.session_state.user_answers = {}
                    st.session_state.quiz_submitted = False
            except Exception as e:
                st.error(f"Error: {str(e)}")

        if st.session_state.quiz_questions:
            questions = st.session_state.quiz_questions

            st.markdown("### Answer all questions then click Submit")
            st.markdown("---")

            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")

                options = q['options']

                selected = st.radio(
                    f"Q{i+1}",
                    options=options,
                    key=f"q_{i}",
                    index=None,
                    label_visibility="collapsed"
                )

                if selected:
                    st.session_state.user_answers[i] = selected[0]

                st.markdown("---")

            all_answered = len(st.session_state.user_answers) == len(questions)

            if not all_answered:
                remaining = len(questions) - len(st.session_state.user_answers)
                st.warning(f"Please answer all questions. ({remaining} remaining)")

            if st.button("✅ Submit Answers", use_container_width=True, disabled=not all_answered):
                st.session_state.quiz_submitted = True

        # --- RESULTS ---
        if st.session_state.quiz_submitted and st.session_state.quiz_questions:
            questions = st.session_state.quiz_questions
            answers = st.session_state.user_answers

            score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q['answer'])
            total = len(questions)
            percent = int((score / total) * 100)

            st.divider()
            st.header("🏆 Your Results")

            if percent >= 80:
                st.success(f"## {percent}% — Excellent! ({score}/{total} correct)")
                advice = "You're well prepared! Keep up this momentum and you'll ace the real exam."
                recommendation_text = "Move on to the next section of your study plan — you're ready."
            elif percent >= 60:
                st.warning(f"## {percent}% — Good Progress ({score}/{total} correct)")
                advice = "You're on the right track but need more practice. Focus on the questions you got wrong."
                recommendation_text = "Review the explanations below, then attempt the quiz again before moving on."
            else:
                st.error(f"## {percent}% — Needs Improvement ({score}/{total} correct)")
                advice = "Don't be discouraged! Review the explanations carefully and revisit your study plan."
                recommendation_text = "Go back to Weeks 1-2 of your study plan before retaking this quiz."

            st.markdown(f"**💡 Advice:** {advice}")
            st.markdown(f"**📋 Next Step:** {recommendation_text}")

            st.divider()
            st.markdown("### 📖 Answer Review")

            for i, q in enumerate(questions):
                user_ans = answers.get(i, "Not answered")
                correct_ans = q['answer']
                is_correct = user_ans == correct_ans

                if is_correct:
                    st.success(f"**Q{i+1}: {q['question']}**")
                    st.markdown(f"✅ Your answer: **{user_ans}** — Correct!")
                else:
                    st.error(f"**Q{i+1}: {q['question']}**")
                    st.markdown(f"❌ Your answer: **{user_ans}** | ✅ Correct: **{correct_ans}**")

                st.markdown(f"📝 *{q['explanation']}*")
                st.markdown("---")

            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state.quiz_questions = None
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
