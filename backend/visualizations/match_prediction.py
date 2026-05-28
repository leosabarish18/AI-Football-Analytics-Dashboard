import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def generate_match_prediction(df):

    # =========================================
    # TITLE
    # =========================================

    st.subheader("Post-Match AI Analysis")

    st.info(
        "This AI analyzes both teams' match statistics "
        "to determine the likely dominant team."
    )

    # =========================================
    # GET TEAMS
    # =========================================

    teams = df['team.name'].dropna().unique()

    if len(teams) < 2:
        st.warning("Not enough teams found.")
        return

    # =========================================
    # COLLECT TEAM STATS
    # =========================================

    stats = []

    for team in teams:

        team_df = df[
            df['team.name'] == team
        ]

        # PASSES
        passes = len(
            team_df[
                team_df['type.name'] == 'Pass'
            ]
        )

        successful_passes = len(
            team_df[
                (team_df['type.name'] == 'Pass') &
                (team_df['pass.outcome.name'].isna())
            ]
        )

        # PASS ACCURACY
        pass_accuracy = 0

        if passes > 0:
            pass_accuracy = (
                successful_passes / passes
            ) * 100

        # SHOTS
        shots = len(
            team_df[
                team_df['type.name'] == 'Shot'
            ]
        )

        # GOALS
        goals = len(
            team_df[
                (team_df['type.name'] == 'Shot') &
                (team_df['shot.outcome.name'] == 'Goal')
            ]
        )

        # RECOVERIES
        recoveries = len(
            team_df[
                team_df['type.name'] == 'Ball Recovery'
            ]
        )

        # STORE
        stats.append({
            "team": team,
            "passes": passes,
            "pass_accuracy": round(pass_accuracy, 1),
            "shots": shots,
            "recoveries": recoveries,
            "goals": goals
        })

    # =========================================
    # DATAFRAME
    # =========================================

    stats_df = pd.DataFrame(stats)

    # =========================================
    # WINNER LABEL
    # =========================================

    max_goals = stats_df['goals'].max()

    stats_df['winner'] = (
        stats_df['goals'] == max_goals
    ).astype(int)

    # =========================================
    # FEATURES
    # =========================================

    X = stats_df[
        [
            'passes',
            'pass_accuracy',
            'shots',
            'recoveries'
        ]
    ]

    y = stats_df['winner']

    # =========================================
    # MODEL
    # =========================================

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    # =========================================
    # CONFIDENCE
    # =========================================

    probabilities = model.predict_proba(X)

    stats_df['confidence'] = (
        probabilities[:, 1] * 100
    ).round(1)

    # =========================================
    # BEST TEAM
    # =========================================

    predicted_team = stats_df.sort_values(
        by='confidence',
        ascending=False
    ).iloc[0]

    # =========================================
    # DISPLAY RESULT
    # =========================================

    st.success(
        f"🏆 AI Detected Winning Team: "
        f"{predicted_team['team']}"
    )

    st.info(
        f"Confidence Score: "
        f"{predicted_team['confidence']:.1f}%"
    )

    # =========================================
    # TABLE
    # =========================================

    st.dataframe(
        stats_df[
            [
                'team',
                'passes',
                'pass_accuracy',
                'shots',
                'recoveries',
                'goals',
                'confidence'
            ]
        ],
        use_container_width=True
    )