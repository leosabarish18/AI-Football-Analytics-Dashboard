from mplsoccer import Pitch
import matplotlib.pyplot as plt


def generate_pass_map(df, player_name):

    fig, ax = plt.subplots(figsize=(12, 8))

    pitch = Pitch(
    pitch_type='statsbomb',
    pitch_color='#1B5E20',
    line_color='white',
    linewidth=2
)

    pitch.draw(ax=ax)

    if "player.name" not in df.columns:
        return fig

    player_df = df[
        (df["player.name"] == player_name) &
        (df["type.name"] == "Pass")
    ]

    for _, row in player_df.iterrows():

        start = row.get("location")
        end = row.get("pass.end_location")

        if (
            isinstance(start, list)
            and isinstance(end, list)
            and len(start) >= 2
            and len(end) >= 2
        ):

            pitch.arrows(
                start[0],
                start[1],
                end[0],
                end[1],
                color="#0026ffd4",
                ax=ax
            )
            fig.patch.set_facecolor('#111827')

    ax.set_title(
    f"{player_name} Pass Map",
    fontsize=22,
    color='#22D3EE',
    fontweight='bold'
)

    return fig