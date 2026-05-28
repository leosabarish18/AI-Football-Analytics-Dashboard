import streamlit as st
import plotly.graph_objects as go


def generate_radar_chart(df, player_name):

    # =====================================================
    # PLAYER FILTER
    # =====================================================
    player_df = df[
        df['player.name'] == player_name
    ]

    # =====================================================
    # METRICS
    # =====================================================

    passes = len(
        player_df[
            player_df['type.name'] == 'Pass'
        ]
    )

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

    recoveries = len(
        player_df[
            player_df['type.name'] == 'Ball Recovery'
        ]
    )

    key_passes = len(
        player_df[
            player_df['pass.shot_assist'] == True
        ]
    )

    categories = [
        'Passes',
        'Shots',
        'Dribbles',
        'Duels',
        'Recoveries',
        'Key Passes'
    ]

    values = [
        passes,
        shots,
        dribbles,
        duels,
        recoveries,
        key_passes
    ]

    # CLOSE RADAR
    categories.append(categories[0])
    values.append(values[0])

    # =====================================================
    # CREATE FIGURE
    # =====================================================

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player_name,
        line=dict(
            color='#22d3ee',
            width=3
        )
    ))

    fig.update_layout(

        polar=dict(
            bgcolor='#09142b',
            radialaxis=dict(
                visible=True,
                color='white'
            ),
            angularaxis=dict(
                color='white'
            )
        ),

        paper_bgcolor='#09142b',

        font=dict(
            color='white'
        ),

        title=dict(
            text=f"{player_name} Radar Chart",
            font=dict(size=24)
        ),

        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )