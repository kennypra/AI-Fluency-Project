import streamlit as st

from analytics.cleaning import load_data

from analytics.metrics import (
    get_total_matches,
    get_total_goals,
    get_average_goals
)

from analytics.visualizations import (
    plot_team_goals,
    plot_team_wins,
    plot_goal_difference,
    plot_goals_by_stage,
    plot_matches_by_stage,
    plot_score_distribution
)

st.set_page_config(
    page_title="2026 FIFA World Cup Dashboard",
    layout="wide"
)

st.title("🏆 2026 FIFA World Cup Analytics Dashboard")

df = load_data("data/matches.csv")


"""
Display key metrics in a three-column layout regardless of the selected visualization.
"""
col1, col2, col3 = st.columns(3)

col1.metric(
    "Matches",
    get_total_matches(df)
)

col2.metric(
    "Goals",
    get_total_goals(df)
)

col3.metric(
    "Avg Goals",
    get_average_goals(df)
)



"""
create sidebar with a selectbox for different visualizations
"""
chart = st.sidebar.selectbox(

    "Choose Visualization",

    [

        "Goals by Team",

        "Wins by Team",

        "Goal Difference",

        "Goals by Stage",

        "Matches by Stage",

        "Score Distribution"

    ]
)


"""
conditional statements to display the selected visualization
"""
if chart == "Goals by Team":

    fig = plot_team_goals(df)

elif chart == "Wins by Team":

    fig = plot_team_wins(df)

elif chart == "Goal Difference":

    fig = plot_goal_difference(df)

elif chart == "Goals by Stage":

    fig = plot_goals_by_stage(df)

elif chart == "Matches by Stage":

    fig = plot_matches_by_stage(df)

else:

    fig = plot_score_distribution(df)

st.plotly_chart(
    fig,
    use_container_width=True
)