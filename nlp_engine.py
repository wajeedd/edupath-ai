from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')


def find_similar_wrong_answers(wrong_answers: list) -> dict:
    """
    Finds semantic similarity between wrong answers.
    Helps detect repeated misconception patterns.
    """

    if len(wrong_answers) < 2:
        return {}

    # Create comparison texts
    texts = [
        item['chosen'] + " vs " + item['correct']
        for item in wrong_answers
    ]

    # Convert text into embeddings
    embeddings = model.encode(texts)

    # Similarity matrix
    sim_matrix = cosine_similarity(embeddings)

    clusters = {}

    for i, item in enumerate(wrong_answers):

        tag = item['concept_tag']

        if tag not in clusters:
            clusters[tag] = []

        clusters[tag].append({
            'question': item['question'],
            'similarity_score': round(float(np.mean(sim_matrix[i])), 2)
        })

    return clusters