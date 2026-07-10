import pandas as pd

REQUIRED_COLUMNS = [
    "match_id",
    "date",
    "stage",
    "group",
    "team_1",
    "team_2",
    "score_1",
    "score_2",
    "winner",
    "decided_by_penalties",
    "notes",
]

def validate_columns(df: pd.DataFrame):
    """
    Ensure all expected columns exist.
    
    Else, raise a ValueError with the missing columns.
    """

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply simple preprocessing steps to 'date' and 'notes' columns.
    """

    df["date"] = pd.to_datetime(df["date"])
    df["notes"] = df["notes"].fillna("")

    df["decided_by_penalties"] = (
    df["decided_by_penalties"]
        .map({"Yes": True, "No": False})
        )
    return df


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load and prepare the dataset.
    """

    df = pd.read_csv(filepath)

    validate_columns(df)

    df = preprocess(df)

    return df


if __name__ == "__main__":
    df = load_data("data/matches.csv")

    print(df["decided_by_penalties"].unique())