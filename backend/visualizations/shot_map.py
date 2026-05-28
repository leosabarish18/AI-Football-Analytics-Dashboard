from mplsoccer import Pitch
import matplotlib.pyplot as plt
import pandas as pd


def generate_shot_map(df, team_name):

    print(df.columns.tolist())
    print(df.head())

    # -----------------------------
    # TEAM FILTER
    # -----------------------------
    team_df = df[df['team.name'] == team_name]

    # -----------------------------
    # SHOT EVENTS
    # -----------------------------
    shots = team_df[
        team_df['type.name'] == 'Shot'
    ].copy()

    # -----------------------------
    # CREATE X/Y FROM LOCATION
    # -----------------------------
    shots = shots[
        shots['location'].notna()
    ]

    shots['x'] = shots['location'].apply(
        lambda loc: loc[0] if isinstance(loc, list) else None
    )

    shots['y'] = shots['location'].apply(
        lambda loc: loc[1] if isinstance(loc, list) else None
    )

    # -----------------------------
    # CREATE PITCH
    # -----------------------------
    pitch = Pitch(
        pitch_color='#196f1d',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    fig.set_facecolor('#09142b')
    ax.set_facecolor('#196f1d')

    # -----------------------------
    # GOALS = GREEN
    # -----------------------------
    goals = shots[
        shots['shot.outcome.name'] == 'Goal'
    ]

    pitch.scatter(
        goals['x'],
        goals['y'],
        s=420,
        color='#00ff88',
        edgecolors='white',
        linewidth=2.5,
        ax=ax,
        label='Goal'
    )

    # -----------------------------
    # SAVED = YELLOW
    # -----------------------------
    saved = shots[
        shots['shot.outcome.name'].isin([
            'Saved',
            'Saved To Post'
        ])
    ]

    pitch.scatter(
        saved['x'],
        saved['y'],
        s=380,
        color='#ffd700',
        edgecolors='white',
        linewidth=2,
        ax=ax,
        label='Saved'
    )

    # -----------------------------
    # MISSED = RED
    # -----------------------------
    missed = shots[
        shots['shot.outcome.name'].isin([
            'Off T',
            'Wayward',
            'Blocked',
            'Post'
        ])
    ]

    pitch.scatter(
        missed['x'],
        missed['y'],
        s=350,
        color='#ff4d4d',
        edgecolors='white',
        linewidth=2,
        ax=ax,
        label='Missed'
    )

    # -----------------------------
    # TITLE
    # -----------------------------
    ax.set_title(
        f"{team_name} Shot Map",
        fontsize=28,
        color='#22d3ee',
        fontweight='bold',
        pad=20
    )

    # -----------------------------
    # LEGEND
    # -----------------------------
    legend = ax.legend(
        facecolor='#09142b',
        edgecolor='white',
        fontsize=12,
        loc='upper left'
    )

    for text in legend.get_texts():
        text.set_color("white")

    return fig