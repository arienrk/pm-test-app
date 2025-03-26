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

    sheet = client.open("PM-Personality_Test").sheet1
    sheet.append_row(data_row)

def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("PM-Personality_Test").sheet1
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
