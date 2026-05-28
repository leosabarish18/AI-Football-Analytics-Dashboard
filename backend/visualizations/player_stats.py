import streamlit as st


def generate_player_stats(df, player_name):

    # =====================================================
    # PLAYER FILTER
    # =====================================================
    player_df = df[
        df['player.name'] == player_name
    ]

    # =====================================================
    # PASSES
    # =====================================================
    total_passes = len(
        player_df[
            player_df['type.name'] == 'Pass'
        ]
    )

    successful_passes = len(
        player_df[
            (player_df['type.name'] == 'Pass') &
            (player_df['pass.outcome.name'].isna())
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
        player_df[
            player_df['type.name'] == 'Shot'
        ]
    )

    goals = len(
        player_df[
            player_df['shot.outcome.name'] == 'Goal'
        ]
    )

    # =====================================================
    # KEY PASSES
    # =====================================================
    key_passes = len(
        player_df[
            player_df['pass.shot_assist'] == True
        ]
    )

    # =====================================================
    # DRIBBLES
    # =====================================================
    dribbles = len(
        player_df[
            player_df['type.name'] == 'Dribble'
        ]
    )

    # =====================================================
    # TACKLES
    # =====================================================
    tackles = len(
        player_df[
            player_df['type.name'] == 'Duel'
        ]
    )

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown(
        f"## {player_name} Statistics"
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
        "Goals",
        goals
    )

    col3.metric(
        "Shots",
        total_shots
    )

    col4.metric(
        "Key Passes",
        key_passes
    )

    # =====================================================
    # ROW 2
    # =====================================================
    col5, col6, col7 = st.columns(3)

    col5.metric(
        "Successful Passes",
        successful_passes
    )

    col6.metric(
        "Dribbles",
        dribbles
    )

    col7.metric(
        "Duels",
        tackles
    )