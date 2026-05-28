import streamlit as st
import pandas as pd


def generate_team_comparison(df):

    st.subheader("Team Comparison")

    teams = df['team.name'].dropna().unique()

    if len(teams) < 2:
        st.warning("Not enough teams found.")
        return

    team1 = teams[0]
    team2 = teams[1]

    team1_df = df[df['team.name'] == team1]
    team2_df = df[df['team.name'] == team2]

    def get_stats(team_df):

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
            pass_accuracy = round(
                (successful_passes / total_passes) * 100,
                1
            )

        shots = len(
            team_df[
                team_df['type.name'] == 'Shot'
            ]
        )

        goals = len(
            team_df[
                (team_df['type.name'] == 'Shot') &
                (team_df['shot.outcome.name'] == 'Goal')
            ]
        )

        duels = len(
            team_df[
                team_df['type.name'] == 'Duel'
            ]
        )

        recoveries = len(
            team_df[
                team_df['type.name'] == 'Ball Recovery'
            ]
        )

        return {
            "Pass Accuracy %": pass_accuracy,
            "Shots": shots,
            "Goals": goals,
            "Duels": duels,
            "Recoveries": recoveries
        }

    team1_stats = get_stats(team1_df)
    team2_stats = get_stats(team2_df)

    comparison_df = pd.DataFrame({
        team1: team1_stats,
        team2: team2_stats
    })

    st.dataframe(
        comparison_df,
        use_container_width=True
    )