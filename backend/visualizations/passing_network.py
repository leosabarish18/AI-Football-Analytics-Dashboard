from mplsoccer import Pitch
import matplotlib.pyplot as plt
import pandas as pd


def generate_passing_network(df, team_name):

    # =========================================================
    # TEAM FILTER
    # =========================================================
    team_df = df[
        df['team.name'] == team_name
    ].copy()

    # =========================================================
    # ONLY PASSES
    # =========================================================
    passes = team_df[
        team_df['type.name'] == 'Pass'
    ].copy()

    # =========================================================
    # REMOVE EMPTY LOCATIONS
    # =========================================================
    passes = passes[
        passes['location'].notna()
    ]

    passes = passes[
        passes['pass.end_location'].notna()
    ]

    # =========================================================
    # CREATE START X/Y
    # =========================================================
    passes['x'] = passes['location'].apply(
        lambda loc: loc[0] if isinstance(loc, list) else None
    )

    passes['y'] = passes['location'].apply(
        lambda loc: loc[1] if isinstance(loc, list) else None
    )

    # =========================================================
    # CREATE END X/Y
    # =========================================================
    passes['end_x'] = passes['pass.end_location'].apply(
        lambda loc: loc[0] if isinstance(loc, list) else None
    )

    passes['end_y'] = passes['pass.end_location'].apply(
        lambda loc: loc[1] if isinstance(loc, list) else None
    )

    # =========================================================
    # PLAYER TOUCH COUNTS
    # =========================================================
    player_pass_count = passes.groupby(
        'player.name'
    ).size()

    # =========================================================
    # PLAYER POSITIONS
    # =========================================================
    avg_pos = passes.groupby(
        'player.name'
    )[['x', 'y']].mean()

    # =========================================================
    # PASS CONNECTIONS
    # =========================================================
    pass_between = passes.groupby(
        ['player.name', 'pass.recipient.name']
    ).size().reset_index(name='count')

    # =========================================================
    # CREATE PITCH
    # =========================================================
    pitch = Pitch(
        pitch_color='#196f1d',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(figsize=(14, 10))

    fig.set_facecolor('#09142b')
    ax.set_facecolor('#196f1d')

    # =========================================================
    # SUCCESSFUL PASSES (GREEN)
    # =========================================================
    successful_passes = passes[
        passes['pass.outcome.name'].isna()
    ]

    for _, row in successful_passes.iterrows():

        distance = (
            (row['end_x'] - row['x']) ** 2 +
            (row['end_y'] - row['y']) ** 2
        ) ** 0.5

        # REMOVE SHORT PASSES
        if distance < 30:
            continue

        pitch.lines(
            row['x'],
            row['y'],
            row['end_x'],
            row['end_y'],
            lw=2,
            color='#00ff88',
            alpha=0.003,
            ax=ax,
            zorder=1
        )

    # =========================================================
    # FAILED PASSES (RED)
    # =========================================================
    failed_passes = passes[
        passes['pass.outcome.name'].notna()
    ]

    for _, row in failed_passes.iterrows():

        distance = (
            (row['end_x'] - row['x']) ** 2 +
            (row['end_y'] - row['y']) ** 2
        ) ** 0.5

        if distance < 35:
            continue

        pitch.lines(
            row['x'],
            row['y'],
            row['end_x'],
            row['end_y'],
            lw=2,
            color='#ff4d4d',
            alpha=0.05,
            linestyle='dashed',
            ax=ax,
            zorder=1
        )

    # =========================================================
    # PROGRESSIVE PASSES (PURPLE)
    # =========================================================
    progressive_passes = passes[
        (passes['end_x'] - passes['x']) > 30
    ]

    for _, row in progressive_passes.iterrows():

        pitch.lines(
            row['x'],
            row['y'],
            row['end_x'],
            row['end_y'],
            lw=2,
            color='#c084fc',
            alpha=0.08,
            comet=True,
            ax=ax,
            zorder=2
        )

    # =========================================================
    # PASS COMBINATIONS
    # =========================================================
    for _, row in pass_between.iterrows():

        # SHOW ONLY STRONG CONNECTIONS
        if row['count'] < 6:
            continue

        player1 = row['player.name']
        player2 = row['pass.recipient.name']
        count = row['count']

        if (
            player1 in avg_pos.index and
            player2 in avg_pos.index
        ):

            x1 = avg_pos.loc[player1, 'x']
            y1 = avg_pos.loc[player1, 'y']

            x2 = avg_pos.loc[player2, 'x']
            y2 = avg_pos.loc[player2, 'y']

            pitch.lines(
                x1,
                y1,
                x2,
                y2,
                lw=count * 0.5,
                color='#00d4ff',
                alpha=0.55,
                ax=ax,
                zorder=3
            )

    # =========================================================
    # PLAYER NODES
    # =========================================================
    for player, row in avg_pos.iterrows():

        touches = player_pass_count.get(player, 1)

        node_size = touches * 18

        pitch.scatter(
            row['x'],
            row['y'],
            s=node_size,
            color='#22d3ee',
            edgecolors='white',
            linewidth=3,
            ax=ax,
            zorder=5
        )

        ax.text(
            row['x'],
            row['y'],
            f"{player.split()[-1]}\n{touches}",
            color='black',
            ha='center',
            va='center',
            fontsize=8,
            fontweight='bold',
            zorder=6
        )

    # =========================================================
    # LEGEND
    # =========================================================
    ax.text(
        2,
        5,
        "GREEN = Successful Pass\n"
        "RED = Failed Pass\n"
        "PURPLE = Progressive Pass\n"
        "Node Size = Touches",
        color='white',
        fontsize=11,
        bbox=dict(
            facecolor='#09142b',
            alpha=0.7
        )
    )

    # =========================================================
    # TITLE
    # =========================================================
    ax.set_title(
        f"{team_name} Passing Network",
        fontsize=28,
        color='#22d3ee',
        fontweight='bold',
        pad=20
    )

    return fig