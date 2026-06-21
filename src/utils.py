"""
utils.py

Helper functions for loading the courses history dataset.
"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "courses_history.csv"


def load_courses(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the courses history CSV into a DataFrame."""
    df = pd.read_csv(path)
    return df
