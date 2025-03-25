import streamlit as st

st.set_page_config(page_title="PM Personality Test", layout="wide")
st.title("🧠 Project Management Personality Test")
st.write("Answer 'A' for Yes or 'B' for No")

questions = [
    "Do you believe a project without a plan is like cooking without a recipe?",
    "Do you make a project schedule before planning your weekend?",
    "Do you feel like your soul leaves your body when someone says, 'Let’s just go with the flow'?",
    "Do you believe that 'ASAP' is not a deadline, but a cry for help?",
    "Do last-minute changes in a project feel like someone flipped your game board right before you won?",
    "Do you check numbers twice before making a decision, and then check them one more time, just in case?",
    "Would you rather spend Friday night with an Excel sheet than at a party?",
    "Do you feel excited when you hear the words 'dashboard' and 'data analysis'?",
    "When someone says 'Trust me,' do you immediately ask for proof and numbers?",
    "Do you believe that gut feelings are cute, but data is king?",
    "Do you think a project plan should have more colors and sticky notes than a child's art project?",
    "Do you believe that Post-it notes and whiteboards solve all problems?",
    "Have you ever replaced a long report with a simple drawing or diagram?",
    "Do you think 'processes' are optional, but creativity is mandatory?",
    "If someone says, 'This is how we always do it,' do you immediately want to try a different way?",
    "Do your teammates talk to you about their problems more than they talk to HR?",
    "Do you believe that a happy team is more important than a perfect report?",
    "Would you rather have coffee and a chat than write another email?",
    "Do you believe a team’s mood decides project success more than any fancy tool?",
    "Have you ever stopped a meeting just to make sure everyone is still emotionally okay?",
    "Do you secretly enjoy presenting your ideas more than working on them?",
    "Can you convince people that your idea is brilliant, even if you just made it up 5 minutes ago?",
    "Do you love big ideas and vision, but details make your brain hurt?",
    "Do you enjoy negotiating deadlines and budgets like you’re in a reality TV show?",
    "Do you believe a great PowerPoint presentation can fix almost anything?",
    "Does missing documentation make you feel like something terrible will happen?",
    "Do you believe rules and processes keep the world from falling apart?",
    "Do you prefer a project where everyone knows exactly what to do, step by step?",
    "Do you believe checklists are life, and without them, chaos takes over?",
    "Does the idea of a 'flexible' process make you physically uncomfortable?",
]

answers = []

with st.form("quiz_form"):
    for idx, q in enumerate(questions, 1):
        response = st.radio(f"{idx}. {q}", ["A. Yes", "B. No"], key=idx)
        answers.append(response)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("✅ Your answers have been submitted!")
    st.write("Here are your responses:")
    for i, ans in enumerate(answers, 1):
        st.write(f"Q{i}: {ans}")
