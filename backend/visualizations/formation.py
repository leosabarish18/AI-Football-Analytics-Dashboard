from mplsoccer import Pitch
import matplotlib.pyplot as plt
import pandas as pd


def generate_formation(df, team_name):

    print(df.columns.tolist())
    print(df.head())

    # -----------------------------
    # FILTER TEAM
    # -----------------------------
    team_df = df[
        (df['team.name'].notna()) &
        (df['team.name'].astype(str).str.strip() == str(team_name).strip())
    ].copy()

    print("TEAM DF SHAPE:", team_df.shape)

    # -----------------------------
    # FILTER VALID LOCATIONS
    # -----------------------------
    formation_df = team_df[
        (team_df['location'].notna()) &
        (team_df['player.name'].notna())
    ].copy()

    formation_df = formation_df[
        formation_df['location'].apply(lambda x: isinstance(x, list))
    ]

    # -----------------------------
    # EXTRACT X/Y
    # -----------------------------
    formation_df['x'] = formation_df['location'].apply(lambda loc: loc[0])
    formation_df['y'] = formation_df['location'].apply(lambda loc: loc[1])

    # -----------------------------
    # PLAYER POSITIONS
    # -----------------------------
    players = formation_df.groupby('player.name')[['x', 'y']].mean()

    # -----------------------------
    # PITCH
    # -----------------------------
    pitch = Pitch(
        pitch_color='#196f1d',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    fig.set_facecolor('#09142b')
    ax.set_facecolor('#196f1d')

    colors = ['#00d4ff', '#ff4d4d', '#ffd700']

    # -----------------------------
    # DRAW PLAYERS
    # -----------------------------
    for i, (player, row) in enumerate(players.iterrows()):

        pitch.scatter(
            row['x'],
            row['y'],
            s=1400,
            color=colors[i % len(colors)],
            edgecolors='black',
            linewidth=3,
            ax=ax
        )

        ax.text(
            row['x'],
            row['y'],
            player.split()[-1],
            color='black',
            ha='center',
            va='center',
            fontsize=10,
            fontweight='bold'
        )

    # -----------------------------
    # TITLE
    # -----------------------------
    ax.set_title(
        f"{team_name} Formation",
        fontsize=22,
        color='#22d3ee',
        fontweight='bold',
        pad=20
    )

    return fig