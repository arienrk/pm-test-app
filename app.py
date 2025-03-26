import streamlit as st
import smtplib
from email.mime.text import MIMEText
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

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
    
        sheet = client.open("PM-Personality_Test").sheet1  # Make sure this matches your sheet name
        sheet.append_row(data_row)
def load_data():
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
    
        sheet = client.open("PM-Personality_Test").sheet1  # Make sure the name matches your sheet
        data = sheet.get_all_records()
        return pd.DataFrame(data)


# -------------------- APP CONFIG --------------------
st.set_page_config(page_title="PM Personality Test", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = 1


# -------------------- ADMIN PAGE --------------------
if st.sidebar.text_input("Admin password") == "admin123":
    st.sidebar.success("Access granted")
    st.title("📊 Admin Dashboard")

    df = load_data()

    st.subheader("🔢 Raw Data")
    st.dataframe(df)

    st.subheader("📊 PM Type Distribution (Pie Chart)")
    if "PM Type(s)" in df.columns:
        chart_data = df["PM Type(s)"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(chart_data.values, labels=chart_data.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

    st.stop()

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

avenger_images = {
    "Iron Man": "https://i.ibb.co/7y0m1nV/ironman.jpg",
    "Captain America": "https://i.ibb.co/7n1fcTg/captainamerica.jpg",
    "Thor": "https://i.ibb.co/XDX85Kt/thor.jpg",
    "Black Widow": "https://i.ibb.co/5Gr1Ly9/blackwidow.jpg",
    "Hulk": "https://i.ibb.co/5kWJKmB/hulk.jpg",
    "Doctor Strange": "https://i.ibb.co/xYb2N1H/doctorstrange.jpg",
    "Spider-Man": "https://i.ibb.co/5Rph3PZ/spiderman.jpg",
    "Black Panther": "https://i.ibb.co/DQXT5S7/blackpanther.jpg"
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
        answer = st.radio(f"Q{idx+1}. {q}", ["A. Yes", "B. No"], key=f"q{idx+1}", index=None)
        answers.append(answer)
        if answer is not None and answer.startswith("A"):
            type_index = idx // 5
            scores[type_keys[type_index]] += 1

    submitted = st.form_submit_button("Submit")

    if submitted:
        if None in answers:
            st.warning("⚠️ Please answer all the questions before submitting.")
        else:
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

    avenger = st.session_state.avenger
    avenger_desc = avenger_traits.get(avenger, "🌟 Unique — just like your hero choice!")

    st.subheader(f"🦸 Your Favorite Avenger: {avenger}")
    st.markdown(avenger_desc)

    #-------------------Google Sheet---------------------
    # Prepare row for Google Sheet
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email = st.session_state.email
    country = st.session_state.country
    role = st.session_state.role
    avenger = st.session_state.avenger
    answers_raw = ", ".join(st.session_state.answers)
    pm_types = ", ".join(top_types)
    holland = ", ".join(holland_codes)
    
    data_row = [now, email, country, role, pm_types, holland, avenger, answers_raw]
    
    # Save to Google Sheet
    save_to_google_sheet(data_row)

    # ---------------- EMAIL & Share Button ----------------
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
        email_lines.append(f"{desc}")
        email_lines.append(f"🧩 Holland Code Match: {holland}")
        email_lines.append("")

    email_lines.append(f"🦸 **Your Favorite Avenger:** {avenger}")
    email_lines.append(avenger_traits.get(avenger, "🌟 Unique — just like your hero choice!"))
    email_lines.append("")
    email_lines.append(f"🌍 Country: {st.session_state.country}")
    email_lines.append(f"💼 Role: {st.session_state.role}")
    email_lines.append("")
    email_lines.append("Thank you for participating — may your projects be as epic as your personality!")
    email_lines.append("-- PM Personality Team")

    email_body = "\n".join(email_lines)

    if st.button("📧 Send my results by email"):
        result = send_email(st.session_state.email, "Your PM Personality Test Results", email_body)
        if result is True:
            st.success("✅ Your result has been emailed!")
        else:
            st.error(f"❌ Failed to send email: {result}")
    st.markdown("---")
    st.markdown("### 💌 Want your friends to try the test too?")
    share_url = "https://pm-o-test-app.streamlit.app/"

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔁 Start Over"):
            st.session_state.clear()
            st.rerun()
    with col2:
        st.markdown(f"[🌐 Open Test Page]({share_url})", unsafe_allow_html=True)

    st.markdown("#### 📢 Share this test on:")

    linkedin_text = "Take the PM Personality Test and discover your project management style! 💼🧠"
    twitter_text = "Discover your PM personality type in this fun test! 💼🧠 #ProjectManagement"

    linkedin_share = f"https://www.linkedin.com/sharing/share-offsite/?url={share_url}"
    twitter_share = f"https://twitter.com/intent/tweet?text={twitter_text}&url={share_url}"
    facebook_share = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    email_share = f"mailto:?subject=PM Personality Test&body=Check out this fun PM personality test! {share_url}"

    col3, col4, col5, col6 = st.columns(4)
    with col3:
        st.markdown(f"[🔗 LinkedIn]({linkedin_share})", unsafe_allow_html=True)
    with col4:
        st.markdown(f"[🐦 Twitter/X]({twitter_share})", unsafe_allow_html=True)
    with col5:
        st.markdown(f"[📘 Facebook]({facebook_share})", unsafe_allow_html=True)
    with col6:
        st.markdown(f"[✉️ Email]({email_share})", unsafe_allow_html=True)
