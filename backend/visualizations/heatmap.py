from mplsoccer import Pitch
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


def generate_heatmap(df, player_name):

    # -----------------------------------
    # FILTER PLAYER EVENTS
    # -----------------------------------
    player_df = df[df['player.name'] == player_name]

    # -----------------------------------
    # REMOVE EVENTS WITHOUT LOCATION
    # -----------------------------------
    player_df = player_df[player_df['location'].notna()]

    x = []
    y = []

    # -----------------------------------
    # EXTRACT X Y LOCATIONS
    # -----------------------------------
    for loc in player_df['location']:

        if isinstance(loc, list):

            if len(loc) >= 2:

                x.append(loc[0])
                y.append(loc[1])

    # -----------------------------------
    # CREATE PITCH
    # -----------------------------------
    pitch = Pitch(
    pitch_type='statsbomb',
    pitch_color='#1B5E20',   # premium stadium grass
    line_color='white',
    linewidth=2
)

    fig, ax = pitch.draw(figsize=(14, 8))

    # -----------------------------------
    # DARK BACKGROUND OUTSIDE PITCH
    # -----------------------------------
    fig.patch.set_facecolor('#111827')
    ax.set_facecolor('#1B5E20')

    # -----------------------------------
    # DRAW HEATMAP
    # -----------------------------------
    if len(x) > 1:

        xy = np.vstack([x, y])

        kde = gaussian_kde(xy)

        xi, yi = np.mgrid[
            0:120:300j,
            0:80:300j
        ]

        zi = kde(
            np.vstack([
                xi.flatten(),
                yi.flatten()
            ])
        )

        zi = zi.reshape(xi.shape)

        # REMOVE EMPTY DARK REGIONS
        threshold = np.max(zi) * 0.12

        zi[zi < threshold] = np.nan

        # HEATMAP
        ax.contourf(
            xi,
            yi,
            zi,
            levels=100,
            cmap='inferno',
            alpha=0.9
        )

        # CONTOUR LINES
        ax.contour(
            xi,
            yi,
            zi,
            levels=20,
            colors='white',
            linewidths=0.3,
            alpha=0.15
        )

        # PLAYER TOUCH POINTS
        pitch.scatter(
            x,
            y,
            ax=ax,
            s=10,
            color='white',
            alpha=0.25
        )

    # -----------------------------------
    # TITLE
    # -----------------------------------
    ax.set_title(
        f"{player_name} Tactical Heatmap",
        fontsize=22,
        color='#22D3EE',
        pad=20,
        weight='bold'
    )

    return fig