import streamlit as st


def generate_match_stats(df, team_name):

    # =====================================================
    # TEAM FILTER
    # =====================================================
    team_df = df[
        df['team.name'] == team_name
    ]

    # =====================================================
    # PASSES
    # =====================================================
    total_passes = len(
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

    if total_passes > 0:
        pass_accuracy = (
            successful_passes / total_passes
        ) * 100
    else:
        pass_accuracy = 0

    # =====================================================
    # SHOTS
    # =====================================================
    total_shots = len(
        team_df[
            team_df['type.name'] == 'Shot'
        ]
    )

    goals = len(
        team_df[
            team_df['shot.outcome.name'] == 'Goal'
        ]
    )

    shots_on_target = len(
        team_df[
            team_df['shot.outcome.name'].isin([
                'Goal',
                'Saved',
                'Saved To Post'
            ])
        ]
    )

    # =====================================================
    # xG
    # =====================================================
    if 'shot.statsbomb_xg' in team_df.columns:

        xg = team_df[
            'shot.statsbomb_xg'
        ].fillna(0).sum()

    else:
        xg = 0

    # =====================================================
    # DUELS
    # =====================================================
    duels = len(
        team_df[
            team_df['type.name'] == 'Duel'
        ]
    )

    # =====================================================
    # RECOVERIES
    # =====================================================
    recoveries = len(
        team_df[
            team_df['type.name'] == 'Ball Recovery'
        ]
    )

    # =====================================================
    # INTERCEPTIONS
    # =====================================================
    interceptions = len(
        team_df[
            team_df['type.name'] == 'Interception'
        ]
    )

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown(
        f"## {team_name} Match Statistics"
)
    st.markdown("---")

    # =====================================================
    # ROW 1
    # =====================================================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Pass Accuracy",
        f"{pass_accuracy:.1f}%"
    )

    col2.metric(
        "xG",
        f"{xg:.2f}"
    )

    col3.metric(
        "Goals",
        goals
    )

    col4.metric(
        "Shots",
        total_shots
    )

    # =====================================================
    # ROW 2
    # =====================================================
    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Shots On Target",
        shots_on_target
    )

    col6.metric(
        "Successful Passes",
        successful_passes
    )

    col7.metric(
        "Recoveries",
        recoveries
    )

    col8.metric(
        "Interceptions",
        interceptions
    )

    # =====================================================
    # ROW 3
    # =====================================================
    col9, col10 = st.columns(2)

    col9.metric(
        "Total Passes",
        total_passes
    )

    col10.metric(
        "Duels",
        duels
    )