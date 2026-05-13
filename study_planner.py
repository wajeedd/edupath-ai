import pandas as pd
from datetime import date, timedelta


def generate_plan(
    weak_concepts: list,
    scores: dict,
    exam_date: date,
    hours_per_day: float
) -> list:

    """
    Generates a personalized study plan.
    """

    # Load resources
    resources_df = pd.read_csv("resources.csv")

    today = date.today()

    # Days remaining
    days_left = (exam_date - today).days

    # Sort weakest concepts first
    sorted_concepts = sorted(
        weak_concepts,
        key=lambda c: scores.get(c, 100)
    )

    plan = []

    day_counter = 0

    for concept in sorted_concepts:

        concept_resources = resources_df[
            resources_df['concept_tag'] == concept
        ]

        total_mins = concept_resources[
            'duration_mins'
        ].sum()

        # Calculate study days needed
        days_needed = max(
            1,
            round(total_mins / (hours_per_day * 60))
        )

        for d in range(days_needed):

            if day_counter >= days_left:
                break

            study_date = today + timedelta(days=day_counter)

            plan.append({
                'date': study_date.strftime("%d %b %Y"),
                'concept': concept,
                'score': scores.get(concept, 0),
                'resources': concept_resources.to_dict('records')
            })

            day_counter += 1

    return plan