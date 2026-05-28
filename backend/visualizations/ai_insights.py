import streamlit as st


def generate_ai_insights(df, team_name, player_name):

    st.subheader("AI Match Insights")

    # =========================================
    # TEAM DATA
    # =========================================

    team_df = df[
        df['team.name'] == team_name
    ]

    player_df = df[
        df['player.name'] == player_name
    ]

    # =========================================
    # METRICS
    # =========================================

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

    pass_accuracy = 0

    if total_passes > 0:
        pass_accuracy = (
            successful_passes / total_passes
        ) * 100

    shots = len(
        player_df[
            player_df['type.name'] == 'Shot'
        ]
    )

    dribbles = len(
        player_df[
            player_df['type.name'] == 'Dribble'
        ]
    )

    duels = len(
        player_df[
            player_df['type.name'] == 'Duel'
        ]
    )

    # =========================================
    # AI INSIGHTS
    # =========================================

    insights = []

    # PASSING
    if pass_accuracy > 85:
        insights.append(
            f"✅ {team_name} showed elite passing accuracy ({pass_accuracy:.1f}%)."
        )

    elif pass_accuracy > 75:
        insights.append(
            f"⚡ {team_name} maintained solid ball circulation."
        )

    else:
        insights.append(
            f"⚠️ {team_name} struggled with passing consistency."
        )

    # SHOTS
    if shots >= 5:
        insights.append(
            f"🔥 {player_name} was highly aggressive in attack with {shots} shots."
        )

    # DRIBBLES
    if dribbles >= 5:
        insights.append(
            f"🪄 {player_name} constantly challenged defenders through dribbling."
        )

    # DUELS
    if duels >= 5:
        insights.append(
            f"💪 {player_name} was heavily involved in physical battles."
        )

    # =========================================
    # DISPLAY
    # =========================================

    for insight in insights:

        st.markdown(
            f"""
            <div style="
                background-color:#111827;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                border-left:5px solid #22d3ee;
                color:white;
                font-size:16px;
            ">
                {insight}
            </div>
            """,
            unsafe_allow_html=True
        )