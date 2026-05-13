from nlp_engine import find_similar_wrong_answers
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from gap_detector import calculate_concept_scores, get_weak_concepts

st.title("📊 Your Results")

answers = st.session_state.get('answers', {})
questions_df = st.session_state.get('questions')

if not answers or questions_df is None:
    st.error("No test data found. Please take the test first.")
    st.stop()

# Calculate scores
scores = calculate_concept_scores(answers, questions_df)
weak = get_weak_concepts(scores)

# Radar chart
concepts = list(scores.keys())
values = list(scores.values())

fig = go.Figure(go.Scatterpolar(
    r=values + [values[0]],
    theta=concepts + [concepts[0]],
    fill='toself'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Concept breakdown
st.subheader("📚 Concept Breakdown")

for concept, score in sorted(scores.items(), key=lambda x: x[1]):

    status = "⚠ Needs Work" if score < 60 else "✅ Good"

    st.metric(
        label=concept,
        value=f"{score:.0f}%",
        delta=status
    )

# Weak concepts
st.subheader("🚨 Weak Concepts")

if weak:
    for concept in weak:
        st.write(f"❌ {concept}")
else:
    st.success("Excellent! No weak concepts detected.")
# Collect wrong answers
wrong_answers = []

for _, row in questions_df.iterrows():

    qid = row['question_id']

    if answers.get(qid) != row['correct_answer']:

        wrong_answers.append({
            'question': row['question_text'],
            'chosen': answers.get(qid, ""),
            'correct': row['correct_answer'],
            'concept_tag': row['concept_tag']
        })

# NLP similarity analysis
clusters = find_similar_wrong_answers(wrong_answers)

st.subheader("🧠 AI Misconception Analysis")

if clusters:

    for concept, items in clusters.items():

        st.write(f"### {concept}")

        for item in items:

            st.write(
                f"- {item['question']} "
                f"(Similarity: {item['similarity_score']})"
            )

else:
    st.success("No significant misconception patterns detected.")
# Load resources
resources_df = pd.read_csv("resources.csv")

st.subheader("📚 Recommended Learning Resources")

for concept in weak:

    st.write(f"## 🔹 {concept}")

    concept_resources = resources_df[
        resources_df['concept_tag'] == concept
    ]

    if len(concept_resources) == 0:
        st.write("No resources found.")
        continue

    for _, resource in concept_resources.iterrows():

        if resource['resource_type'] == 'youtube':

            st.markdown(
                f"🎥 [{resource['title']}]({resource['url']}) "
                f"({resource['duration_mins']} mins)"
            )

        elif resource['resource_type'] == 'ncert':

            st.markdown(
                f"📘 {resource['title']}"
            )