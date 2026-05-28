import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Football Dashboard",
    page_icon="⚽",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #09142b;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #1e1e2f;
}

/* TITLES */
h1, h2, h3, h4 {
    color: white;
}

/* TEXT */
p, label, div {
    color: white;
}

/* METRIC CARDS */
div[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #22d3ee;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(34, 211, 238, 0.3);
}

/* SELECTBOX */
div[data-baseweb="select"] {
    background-color: #111827;
    border-radius: 10px;
}

/* TABS */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: bold;
}

/* REMOVE STREAMLIT HEADER */
header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown("""
# ⚽ AI Football Analytics Dashboard
### Advanced Match Intelligence & Tactical Analysis
""")

st.divider()
import streamlit as st
import pandas as pd

from utils.load_competitions import load_competitions
from utils.load_matches import load_matches
from utils.load_events import load_events

from visualizations.heatmap import generate_heatmap
from visualizations.pass_map import generate_pass_map
from visualizations.passing_network import generate_passing_network
from visualizations.formation import generate_formation
from visualizations.shot_map import generate_shot_map
from visualizations.match_stats import generate_match_stats
from visualizations.player_stats import generate_player_stats
from visualizations.radar_chart import generate_radar_chart
from visualizations.ai_insights import generate_ai_insights
from visualizations.team_comparison import generate_team_comparison
from visualizations.match_prediction import generate_match_prediction

# ---------------------------------------------------
# LOAD COMPETITIONS
# ---------------------------------------------------

competitions = load_competitions()

competition_options = {}

for comp in competitions:

    label = f"{comp.get('competition_name')} ({comp.get('season_name')})"

    competition_options[label] = (
        comp.get("competition_id"),
        comp.get("season_id")
    )

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Football Analytics")

selected_competition = st.sidebar.selectbox(
    "Select Tournament",
    list(competition_options.keys())
)

competition_id, season_id = competition_options[selected_competition]

# ---------------------------------------------------
# LOAD MATCHES
# ---------------------------------------------------

matches = load_matches(competition_id, season_id)

match_options = {}

for match in matches:

    home_team = match["home_team"]["home_team_name"]
    away_team = match["away_team"]["away_team_name"]

    label = f"{home_team} vs {away_team}"

    match_options[label] = match["match_id"]

selected_match = st.sidebar.selectbox(
    "Select Match",
    list(match_options.keys())
)

if not match_options:
    st.warning("No matches available for selected tournament.")
    st.stop()

selected_match = st.sidebar.selectbox(
    "Select Match",
    list(match_options.keys())
)

match_id = match_options[selected_match]

# ---------------------------------------------------
# LOAD EVENTS
# ---------------------------------------------------

events = load_events(match_id)

if len(events) == 0:
    st.error("No event data found.")
    st.stop()

clean_events = [
    event for event in events
    if isinstance(event, dict)
]

df = pd.json_normalize(clean_events)

# ---------------------------------------------------
# TEAM COLUMN
# ---------------------------------------------------

team_column = None

possible_team_columns = [
    "team.name",
    "possession_team.name"
]

for col in possible_team_columns:
    if col in df.columns:
        team_column = col
        break

if team_column is None:
    st.error("Team column not found.")
    st.stop()

teams = sorted(df[team_column].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams
)

team_df = df[df[team_column] == selected_team]

# ---------------------------------------------------
# PLAYER COLUMN
# ---------------------------------------------------

player_column = None

possible_player_columns = [
    "player.name"
]

for col in possible_player_columns:
    if col in df.columns:
        player_column = col
        break

if player_column is None:
    st.error("Player column not found.")
    st.stop()

players = sorted(team_df[player_column].dropna().unique())

selected_player = st.sidebar.selectbox(
    "Select Player",
    players
)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tabs = st.tabs([
    "Heatmap",
    "Pass Map",
    "Passing Network",
    "Formation",
    "Shot Map",
    "Match Stats",
    "Player Stats",
    "Radar Chart",
    "AI Insights",
    "Team Comparison",
    "Post-Match AI Analysis"
])

# ---------------------------------------------------
# HEATMAP
# ---------------------------------------------------

with tabs[0]:

    st.subheader("Player Heatmap")

    try:
        fig = generate_heatmap(
            team_df,
            selected_player
        )

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Heatmap Error: {e}")

# ---------------------------------------------------
# PASS MAP
# ---------------------------------------------------

with tabs[1]:

    st.subheader("Pass Map")

    try:
        fig = generate_pass_map(
            team_df,
            selected_player
        )

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Pass Map Error: {e}")

# ---------------------------------------------------
# PASSING NETWORK
# ---------------------------------------------------

with tabs[2]:

    st.subheader("Passing Network")

    try:
        fig = generate_passing_network(
            team_df,
            selected_team
        )

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Passing Network Error: {e}")

# ---------------------------------------------------
# FORMATION
# ---------------------------------------------------

with tabs[3]:

    st.subheader("Formation")

    try:
        fig = generate_formation(
            team_df,
            selected_team
        )

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Formation Error: {e}")

# ---------------------------------------------------
# SHOT MAP
# ---------------------------------------------------

with tabs[4]:

    st.subheader("Shot Map")

    try:
        fig = generate_shot_map(
            team_df,
            selected_team
        )

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Shot Map Error: {e}")

# ---------------------------------------------------
# MATCH STATS
# ---------------------------------------------------

with tabs[5]:

    st.subheader("Match Statistics")

    try:

        generate_match_stats(
            df,
            selected_team
        )

    except Exception as e:
        st.error(f"Match Stats Error: {e}")

# ---------------------------------------------------
# PLAYER STATS
# ---------------------------------------------------

with tabs[6]:

    st.subheader("Player Statistics")

    try:

        generate_player_stats(
            team_df,
            selected_player
        )

    except Exception as e:
        st.error(f"Player Stats Error: {e}")
# ---------------------------------------------------
# RADAR CHART
# ---------------------------------------------------

with tabs[7]:

    st.subheader("Player Radar Chart")

    try:

        generate_radar_chart(
            team_df,
            selected_player
        )

    except Exception as e:
        st.error(f"Radar Chart Error: {e}")
# ---------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------

with tabs[8]:

    try:

        generate_ai_insights(
            team_df,
            selected_team,
            selected_player
        )

    except Exception as e:
        st.error(f"AI Insights Error: {e}")
# ---------------------------------------------------
# TEAM COMPARISON
# ---------------------------------------------------

with tabs[9]:

    try:

        generate_team_comparison(
            df
        )

    except Exception as e:
        st.error(f"Team Comparison Error: {e}")
# ---------------------------------------------------
# ML MATCH PREDICTION
# ---------------------------------------------------

with tabs[10]:

    try:

        generate_match_prediction(df)

    except Exception as e:
        st.error(f"Prediction Error: {e}")