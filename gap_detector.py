def calculate_concept_scores(answers, questions_df):

    concept_data = {}

    for _, row in questions_df.iterrows():

        concept = row['concept_tag']

        if concept not in concept_data:
            concept_data[concept] = {
                'correct': 0,
                'total': 0
            }

        concept_data[concept]['total'] += 1

        qid = row['question_id']

        if answers.get(qid) == row['correct_answer']:
            concept_data[concept]['correct'] += 1

    scores = {}

    for concept, data in concept_data.items():

        score = (data['correct'] / data['total']) * 100

        scores[concept] = score

    return scores


def get_weak_concepts(scores):

    weak = []

    for concept, score in scores.items():

        if score < 60:
            weak.append(concept)

    return weak