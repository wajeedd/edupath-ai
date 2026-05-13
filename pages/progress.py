import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import json


def load_user_history(user_id: int) -> pd.DataFrame:

    conn = sqlite3.connect("edupath.db")

    df = pd.read_sql("""
        SELECT taken_at, scores_json
        FROM sessions
        WHERE user_id = ?
        ORDER BY taken_at
    """, conn, params=(user_id,))

    conn.close()

    rows = []

    for _, row in df.iterrows():

        scores = json.loads(row['scores_json'])

        for concept, score in scores.items():

            rows.append({
                'date': row['taken_at'],
                'concept': concept,
                'score': score
            })

    return pd.DataFrame(rows)


# Page title
st.title("📈 Your Progress")

# Check login
if 'user_id' not in st.session_state:

    st.warning("Please log in first.")

    st.stop()

# Load history
history = load_user_history(
    st.session_state['user_id']
)

# Empty history
if history.empty:

    st.info(
        "Take a few tests to see your progress here."
    )

# Show charts
else:

    st.subheader("📊 Concept Improvement Over Time")

    fig = px.line(
        history,
        x='date',
        y='score',
        color='concept',
        markers=True,
        title="Concept Scores Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Average score
    st.subheader("📌 Performance Summary")

    avg_score = history['score'].mean()

    st.metric(
        "Average Concept Score",
        f"{avg_score:.1f}%"
    )