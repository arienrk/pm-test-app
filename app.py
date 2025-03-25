import streamlit as st

st.set_page_config(page_title="PM Personality Test", layout="wide")

# -------------------- Initialization --------------------
if "page" not in st.session_state:
    st.session_state.page = 1

type_descriptions = {
    "The Gantt Captain": ("You thrive on structure, execution, and getting things done step by step.", "Realistic (R)", "📊"),
    "Spreadsheet Detective": ("You love diving into data, finding patterns, and solving logic puzzles.", "Investigative (I)", "🕵️"),
    "Agile Picasso": ("You’re visual, flexible, and thrive on creative problem-solving.", "Artistic (A)", "🎨"),
    "PM Therapist": ("You care deeply about your team and believe collaboration drives success.", "Social (S)", "💬"),
    "PowerPoint Gladiator": ("You love the spotlight, persuasion, and presenting bold ideas.", "Enterprising (E)", "🎤"),
    "Governance Guardian": ("You keep things structured, organized, and compliant.", "Conventional (C)", "🛡️"),
}

avenger_traits = {
    "Iron Man": "🧠 Strategic, inventive, and always two steps ahead.",
    "Captain America": "🛡️ Loyal, brave, and a natural leader.",
    "Thor": "⚡ Powerful, noble, and sometimes unpredictable.",
    "Black Widow": "🕵️ Strategic, calm under pressure, and always a step ahead.",
    "Hulk": "💪 Strong, passionate, and surprisingly thoughtful.",
    "Doctor Strange": "🔮 Wise, mystical, and a master of complex situations.",
    "Spider-Man": "🕸️ Clever, quick, and full of energy.",
    "Black Panther": "🐾 Noble, resourceful, and grounded in purpose.",
    "Other": "🌟 Unique — just like your hero choice!",
}

# -------------------- PAGE 1 --------------------
if st.session_state.page == 1:
    st.title("👤 Welcome to the PM Personality Test")
    st.subheader("Step 1: Tell us a bit about yourself")

    country = st.text_input("🌍 What country are you from?")
    role_options = ["Project Manager", "PMO", "Product Manager", "Delivery Manager", "Program Manager", "Other"]
    role_selected = st.selectbox("🎯 Choose your role", role_options)
    other_role = st.text_input("Please specify your role:") if role_selected == "Other" else ""
    avenger = st.selectbox("🦸 Who is your favorite Avenger?", list(avenger_traits.keys()))
    email = st.text_input("📧 Your Email Address")
    consent = st.checkbox("I agree to the GDPR terms and data usage policy.")

    if st.button("Start the Test ➡️"):
        if not (country and email and consent):
            st.warning("Please complete all required fields and accept the privacy notice.")
        else:
            st.session_state.country = country
            st.session_state.role = other_role if role_selected == "Other" else role_selected
            st.session_state.avenger = avenger
            st.session_state.email = email
            st.session_state.page = 2

# -------------------- PAGE 2 --------------------
elif st.session_state.page == 2:
    st.title("🧠 PM Personality Quiz")

    questions = [
        # The Gantt Captain
        "Do you believe a project without a plan is like cooking without a recipe?",
        "Do you make a project schedule before planning your weekend?",
        "Do you feel like your soul leaves your body when someone says, 'Let’s just go with the flow'?",
        "Do you believe that 'ASAP' is not a deadline, but a cry for help?",
        "Do last-minute changes in a project feel like someone flipped your game board right before you won?",
        # Spreadsheet Detective
        "Do you check numbers twice before making a decision, and then check them one more time, just in case?",
        "Would you rather spend Friday night with an Excel sheet than at a party?",
        "Do you feel excited when you hear the words 'dashboard' and 'data analysis'?",
        "When someone says 'Trust me,' do you immediately ask for proof and numbers?",
        "Do you believe that gut feelings are cute, but data is king?",
        # Agile Picasso
        "Do you think a project plan should have more colors and sticky notes than a child's art project?",
        "Do you believe that Post-it notes and whiteboards solve all problems?",
        "Have you ever replaced a long report with a simple drawing or diagram?",
        "Do you think 'processes' are optional, but creativity is mandatory?",
        "If someone says, 'This is how we always do it,' do you immediately want to try a different way?",
        # PM Therapist
        "Do your teammates talk to you about their problems more than they talk to HR?",
        "Do you believe that a happy team is more important than a perfect report?",
        "Would you rather have coffee and a chat than write another email?",
        "Do you believe a team’s mood decides project success more than any fancy tool?",
        "Have you ever stopped a meeting just to make sure everyone is still emotionally okay?",
        # PowerPoint Gladiator
        "Do you secretly enjoy presenting your ideas more than working on them?",
        "Can you convince people that your idea is brilliant, even if you just made it up 5 minutes ago?",
        "Do you love big ideas and vision, but details make your brain hurt?",
        "Do you enjoy negotiating deadlines and budgets like you’re in a reality TV show?",
        "Do you believe a great PowerPoint presentation can fix almost anything?",
        # Governance Guardian
        "Does missing documentation make you feel like something terrible will happen?",
        "Do you believe rules and processes keep the world from falling apart?",
        "Do you prefer a project where everyone knows exactly what to do, step by step?",
        "Do you believe checklists are life, and without them, chaos takes over?",
        "Does the idea of a 'flexible' process make you physically uncomfortable?",
    ]

    type_keys = list(type_descriptions.keys())
    scores = {key: 0 for key in type_keys}
    answers = []

    with st.form("quiz_form"):
        for idx, q in enumerate(questions):
            answer = st.radio(f"Q{idx+1}. {q}", ["A. Yes", "B. No"], key=f"q{idx+1}")
            answers.append(answer)
            if answer.startswith("A"):
                type_index = idx // 5  # 5 questions per type
                scores[type_keys[type_index]] += 1

        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.page = 3
        st.session_state.scores = scores
        st.session_state.answers = answers

# -------------------- PAGE 3: RESULTS --------------------
elif st.session_state.page == 3:
    st.title("🎉 Your Results")

    scores = st.session_state.scores
    top_score = max(scores.values())
    top_types = [ptype for ptype, score in scores.items() if score == top_score]

    descriptions = []
    holland_codes = []

    st.subheader("🧠 Your PM Personality Type(s):")
    for ptype in top_types:
        desc, holland, icon = type_descriptions[ptype]
        st.markdown(f"**{icon} {ptype}**\n\n{desc}\n\n🧩 *Holland Code Match: {holland}*\n")
        descriptions.append(desc)
        holland_codes.append(holland)

    # Favorite Avenger
    avenger = st.session_state.avenger
    avenger_desc = avenger_traits.get(avenger, "🌟 Unique — just like your hero choice!")

    st.subheader(f"🦸 Your Favorite Avenger: {avenger}")
    st.markdown(avenger_desc)

    # You can add an email send button or backend next
