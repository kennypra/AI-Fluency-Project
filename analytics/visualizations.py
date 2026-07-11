"""
This file contains the functions necessary for generating interactive Plotly visualizations for the FIFA World Cup Analytics Dashboard.
"""

import plotly.express as px

from analytics.metrics import (
    get_team_statistics,
    get_matches_by_stage,
    get_goals_by_stage,
)


def plot_team_goals(df):
    """
    Create a bar chart showing goals scored by each team.
    """

    stats = get_team_statistics(df)

    fig = px.bar(
        stats,
        x="Team",
        y="GF",
        title="Goals Scored by Team",
        labels={
            "GF": "Goals Scored",
            "Team": "Team"
        }
    )

    return fig


def plot_team_wins(df):
    """
    Create a bar chart showing wins by team.
    """

    stats = get_team_statistics(df)

    fig = px.bar(
        stats,
        x="Team",
        y="W",
        title="Wins by Team",
        labels={
            "W": "Wins",
            "Team": "Team"
        }
    )

    return fig


def plot_goal_difference(df):
    """
    Create a bar chart of goal differential.
    """

    stats = get_team_statistics(df)

    fig = px.bar(
        stats,
        x="Team",
        y="GD",
        title="Goal Differential",
        labels={
            "GD": "Goal Difference"
        }
    )

    return fig



def plot_goals_by_stage(df):
    """
    Total goals scored in each tournament stage.
    """

    goals = get_goals_by_stage(df)

    fig = px.bar(
        x=goals.index,
        y=goals.values,
        labels={
            "x": "Stage",
            "y": "Goals"
        },
        title="Goals by Tournament Stage"
    )

    return fig



def plot_matches_by_stage(df):
    """
    Number of matches played in each stage.
    """

    matches = get_matches_by_stage(df)

    fig = px.bar(
        x=matches.index,
        y=matches.values,
        labels={
            "x": "Stage",
            "y": "Matches"
        },
        title="Matches by Tournament Stage"
    )

    return fig



def plot_score_distribution(df):
    """
    Histogram showing total goals per match.
    """

    scores = df.copy()

    scores["total_goals"] = (
        scores["score_1"] +
        scores["score_2"]
    )

    fig = px.histogram(
        scores,
        x="total_goals",
        nbins=8,
        title="Distribution of Total Goals per Match",
        labels={
            "total_goals": "Goals"
        }
    )

    return fig



if __name__ == "__main__":

    from analytics.cleaning import load_data

    df = load_data("data/matches.csv")

    fig = plot_score_distribution(df)

    fig.show()
    