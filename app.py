import streamlit as st
import smtplib
from email.mime.text import MIMEText
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# -------------------- EMAIL FUNCTION --------------------
def send_email(recipient, subject, body):
    sender = st.secrets["email"]["address"]
    app_password = st.secrets["email"]["app_password"]

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = f"PM Personality Team <{sender}>"
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        return f"Email sending failed: {str(e)}"

# -------------------- GOOGLE SHEET FUNCTION --------------------
def save_to_google_sheet(data_row):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    sheet = client.open("PM-Personality_Test").sheet1
    sheet.append_row(data_row)

# -------------------- APP CONFIG --------------------
st.set_page_config(page_title="PM Personality Test", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = 1

# -------------------- TYPE + AVENGER DEFINITIONS --------------------
type_descriptions = {
    "The Gantt Captain": ("You thrive on structure, execution, and getting things done step by step.", "Realistic (R)", "📈"),
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

# -------------------- PAGE 1: USER INFO --------------------
if st.session_state.page == 1:
    st.title("👤 Welcome to the PM Personality Test")
    st.subheader("Step 1: Tell us a bit about yourself")

    country = st.text_input("🌍 What country are you from?")
    role_options = ["Project Manager", "PMO", "Product Manager", "Delivery Manager", "Program Manager", "Other"]
    role_selected = st.selectbox("🎯 Choose your role", role_options)
    other_role = st.text_input("Please specify your role:") if role_selected == "Other" else ""
    avenger = st.selectbox("🤸 Who is your favorite Avenger?", list(avenger_traits.keys()))
    email = st.text_input("📧 Your Email Address")
    consent = st.checkbox("I agree to the GDPR terms and data usage policy.")

    if st.button("Start the Test ➔"):
        if not (country and email and consent):
            st.warning("Please complete all required fields and accept the privacy notice.")
        else:
            st.session_state.country = country
            st.session_state.role = other_role if role_selected == "Other" else role_selected
            st.session_state.avenger = avenger
            st.session_state.email = email
            st.session_state.page = 2

# -------------------- PAGE 2: QUIZ --------------------
elif st.session_state.page == 2:
    st.title("🧠 PM Personality Quiz")

    questions = [ ... ]  # Your questions here (omitted for space)

    type_keys = list(type_descriptions.keys())
    scores = {key: 0 for key in type_keys}
    answers = []

    with st.form("quiz_form"):
        for idx, q in enumerate(questions):
            answer = st.radio(f"Q{idx+1}. {q}", ["A. Yes", "B. No"], key=f"q{idx+1}")
            answers.append(answer)
            if answer.startswith("A"):
                type_index = idx // 5
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
    answers = st.session_state.answers
    top_score = max(scores.values())
    top_types = [ptype for ptype, score in scores.items() if score == top_score]

    descriptions = []
    holland_codes = []

    st.subheader("🧠 Your PM Personality Type(s):")
    for ptype in top_types:
        desc, holland, icon = type_descriptions[ptype]
        st.markdown(f"**{icon} {ptype}**\n\n{desc}\n\n🧉 *Holland Code Match: {holland}*\n")
        descriptions.append(desc)
        holland_codes.append(holland)

    avenger = st.session_state.avenger
    avenger_desc = avenger_traits.get(avenger, "🌟 Unique — just like your hero choice!")

    st.subheader(f"🤸 Your Favorite Avenger: {avenger}")
    st.markdown(avenger_desc)

    # Build and send the email
    email_lines = [
        "Hi there!",
        "",
        "Thanks for completing the PM Personality Test 🎯",
        "",
        "🧠 **Your PM Personality Type(s):**"
    ]
    for ptype in top_types:
        desc, holland, icon = type_descriptions[ptype]
        email_lines.append(f"{icon} {ptype}")
        email_lines.append(desc)
        email_lines.append(f"🧉 Holland Code Match: {holland}")
        email_lines.append("")

    email_lines.append(f"🤸 Favorite Avenger: {avenger}")
    email_lines.append(avenger_desc)
    email_lines.append("")
    email_lines.append(f"🌍 Country: {st.session_state.country}")
    email_lines.append(f"💼 Role: {st.session_state.role}")
    email_lines.append("")
    email_lines.append("Thank you for participating — may your projects be as epic as your personality!")
    email_lines.append("-- PM Personality Team")

    email_body = "\n".join(email_lines)

    email_sent = send_email(
        recipient=st.session_state.email,
        subject="🧠 Your PM Personality Test Results",
        body=email_body
    )

    if email_sent is True:
        st.success("📧 Your result has been emailed to you!")
    else:
        st.error(f"❌ Failed to send email: {email_sent}")

    # Save to Google Sheet
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pm_types = ", ".join(top_types)
    holland = ", ".join(holland_codes)
    answers_raw = ", ".join(answers)

    data_row = [
        now,
        st.session_state.email,
        st.session_state.country,
        st.session_state.role,
        pm_types,
        holland,
        st.session_state.avenger,
        answers_raw,
        str(top_score)
    ]

    save_to_google_sheet(data_row)

    # Share and Restart
    st.markdown("---")
    st.markdown("### 📨 Want your friends to try the test too?")
    share_url = "https://pm-o-test-app.streamlit.app/"  # Your app URL here

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔁 Start Over"):
            st.session_state.clear()
            st.rerun()

    with col2:
        st.markdown(f"[🌐 Share This Test]({share_url})", unsafe_allow_html=True)
