"""
Contains functions for computing tournament and team-level statistics from the FIFA World Cup match dataset.
"""

import pandas as pd


def get_total_matches(df: pd.DataFrame) -> int:
    """
    Return total number of matches played.
    """
    return len(df)


def get_total_goals(df: pd.DataFrame) -> int:
    """
    Return total number of goals scored.
    """
    return (df["score_1"] + df["score_2"]).sum()


def get_average_goals(df: pd.DataFrame) -> float:
    """
    Return average goals scored per match.
    """
    return round(get_total_goals(df) / get_total_matches(df), 2)


def get_matches_by_stage(df: pd.DataFrame) -> pd.Series:
    """
    Return number of matches played in each stage.
    """
    return df["stage"].value_counts()


def get_goals_by_stage(df: pd.DataFrame) -> pd.Series:
    """
    Return total goals scored in each stage.
    """
    goals = df["score_1"] + df["score_2"]
    return goals.groupby(df["stage"]).sum()


def get_highest_scoring_matches(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Return highest scoring matches.
    """
    matches = df.copy()
    matches["total_goals"] = matches["score_1"] + matches["score_2"]

    return matches.sort_values(
        by="total_goals",
        ascending=False
    ).head(top_n)


def get_penalty_matches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return all matches decided by penalties.
    """
    return df[df["decided_by_penalties"] == True]


def get_team_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a complete statistics table for every team.

    Returns a DataFrame with columns:

    Team
    GP : Games Played
    W  : Wins
    D  : Draws
    L  : Losses
    GF : Goals For
    GA : Goals Against
    GD : Goal Difference
    """

    teams = sorted(set(df["team_1"]).union(df["team_2"]))

    stats = pd.DataFrame({
        "Team": teams,
        "GP": 0,
        "W": 0,
        "D": 0,
        "L": 0,
        "GF": 0,
        "GA": 0
    })

    stats = stats.set_index("Team")

    for _, match in df.iterrows():

        team1 = match["team_1"]
        team2 = match["team_2"]

        score1 = match["score_1"]
        score2 = match["score_2"]

        winner = match["winner"]

        # Games Played
        stats.loc[team1, "GP"] += 1
        stats.loc[team2, "GP"] += 1

        # Goals
        stats.loc[team1, "GF"] += score1
        stats.loc[team1, "GA"] += score2

        stats.loc[team2, "GF"] += score2
        stats.loc[team2, "GA"] += score1

        # Result
        if winner == "Draw":
            stats.loc[team1, "D"] += 1
            stats.loc[team2, "D"] += 1

        elif winner == team1:
            stats.loc[team1, "W"] += 1
            stats.loc[team2, "L"] += 1

        elif winner == team2:
            stats.loc[team2, "W"] += 1
            stats.loc[team1, "L"] += 1

    stats["GD"] = stats["GF"] - stats["GA"]

    stats = stats.reset_index()

    stats = stats.sort_values(
        by=["W", "GD", "GF"],
        ascending=False
    ).reset_index(drop=True)

    return stats


if __name__ == "__main__":

    from cleaning import load_data

    df = load_data("data/matches.csv")

    print("\n--- Tournament Summary ---")
    print(f"Matches: {get_total_matches(df)}")
    print(f"Goals: {get_total_goals(df)}")
    print(f"Average Goals: {get_average_goals(df)}")

    print("\n--- Matches by Stage ---")
    print(get_matches_by_stage(df))

    print("\n--- Goals by Stage ---")
    print(get_goals_by_stage(df))

    print("\n--- Highest Scoring Matches ---")
    print(
        get_highest_scoring_matches(df)[
            [
                "team_1",
                "score_1",
                "score_2",
                "team_2",
                "stage",
            ]
        ]
    )

    print("\n--- Team Statistics ---")
    print(get_team_statistics(df))