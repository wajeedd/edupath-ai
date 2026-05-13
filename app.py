import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="EduPath AI", page_icon="📚")

# App title
st.title("📚 EduPath AI — Know Your Gaps")

# Load questions CSV
df = pd.read_csv("questions.csv")

# Instructions
st.subheader("Take the Diagnostic Test")
st.write("Answer each question carefully. This helps identify weak concepts.")

# Store answers
answers = {}

# Display questions
for _, row in df.iterrows():

    options = [
        row['option_a'],
        row['option_b'],
        row['option_c'],
        row['option_d']
    ]

    choice = st.radio(
        f"Q{row['question_id']}: {row['question_text']}",
        options,
        key=f"q{row['question_id']}",
        index=None
    )

    answers[row['question_id']] = choice

# Submit button
if st.button("Submit Test"):

    st.session_state['answers'] = answers
    st.session_state['questions'] = df

    st.success("Test submitted successfully! ✅")

    st.switch_page("pages/results.py")