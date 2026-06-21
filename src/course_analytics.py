"""
course_analytics.py

Analytics helpers for the professional courses history dataset.

The source dataset (courses_history.csv) tracks every course/certification
completed across a career, with columns:
- idcourse, LINKEDIN, PLATAFORMA, TITULO, AÑO, AREA
- One binary column per skill tag: Marketing, SPSS, EXCEL, TABLEAU,
  POWERBI, SQL, R, PYTHON, IA ML, Cloud MLOps

This module turns that raw structure into tidy summaries for the dashboard:
counts by year, by platform, by skill, and a simple "learning timeline"
view that shows how the skill focus has evolved over time.
"""

import pandas as pd

SKILL_COLUMNS = [
    "Marketing", "SPSS", "EXCEL", "TABLEAU", "POWERBI",
    "SQL", "R", "PYTHON", "IA ML", "Cloud MLOps",
]


def clean_courses(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize raw column types: skill flags to 0/1 ints, year to numeric."""
    df = df.copy()
    for col in SKILL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["TITULO"] = df["TITULO"].astype(str).str.strip().str.strip("'\u2018\u2019")
    df["PLATAFORMA"] = df["PLATAFORMA"].astype(str).str.strip()
    # Relabel area names that changed naming over time
    AREA_RELABEL = {
        "Data engineering": "Feature engineering",
    }
    df["AREA"] = df["AREA"].replace(AREA_RELABEL)
    return df


def courses_per_year(df: pd.DataFrame) -> pd.DataFrame:
    """Count of courses completed per year."""
    out = (
        df.dropna(subset=["AÑO"])
        .groupby("AÑO")
        .size()
        .reset_index(name="count")
        .sort_values("AÑO")
    )
    out["AÑO"] = out["AÑO"].astype(int)
    return out


def courses_per_platform(df: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    """Top N platforms by number of courses completed."""
    out = (
        df.groupby("PLATAFORMA")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
    )
    return out

AREA_ORDER = [
    "Business intelligence",
    "Code lab",
    "Exploration analysis",
    "Data cleaning",
    "Feature engineering",
    "Visualization",
    "Modelling",
    "Production implementation",
]

def courses_per_area(df: pd.DataFrame) -> pd.DataFrame:
    """Course count by subject area (AREA column)."""
    out = (
        df.groupby("AREA")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    out["AREA"] = pd.Categorical(out["AREA"], categories=AREA_ORDER, ordered=True)
    out = out.sort_values("AREA").dropna(subset=["AREA"])
    out["AREA"] = out["AREA"].astype(str)
    return out


def skill_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Total number of courses tagged with each skill."""
    totals = df[SKILL_COLUMNS].sum().reset_index()
    totals.columns = ["skill", "count"]
    return totals.sort_values("count", ascending=False)


def skill_evolution_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Long-format table: year x skill x count, for a stacked trend chart."""
    melted = df.melt(
        id_vars=["AÑO"],
        value_vars=SKILL_COLUMNS,
        var_name="skill",
        value_name="flag",
    )
    melted = melted[melted["flag"] == 1].dropna(subset=["AÑO"])
    out = (
        melted.groupby(["AÑO", "skill"])
        .size()
        .reset_index(name="count")
    )
    out["AÑO"] = out["AÑO"].astype(int)
    return out


def summary_metrics(df: pd.DataFrame) -> dict:
    """Headline numbers for the dashboard's top metric row."""
    valid_years = df["AÑO"].dropna()
    return {
        "total_courses": len(df),
        "year_range": (
            f"{int(valid_years.min())}–{int(valid_years.max())}"
            if not valid_years.empty else "—"
        ),
        "n_platforms": df["PLATAFORMA"].nunique(),
        "n_areas": df["AREA"].nunique(),
        "top_skill": skill_totals(df).iloc[0]["skill"] if len(df) else "—",
    }


def filter_courses(
    df: pd.DataFrame,
    year_range: tuple = None,
    areas: list = None,
    platforms: list = None,
    skills: list = None,
) -> pd.DataFrame:
    """Apply the sidebar filters used by the dashboard."""
    out = df.copy()

    if year_range:
        out = out[(out["AÑO"] >= year_range[0]) & (out["AÑO"] <= year_range[1])]

    if areas:
        out = out[out["AREA"].isin(areas)]

    if platforms:
        out = out[out["PLATAFORMA"].isin(platforms)]

    if skills:
        mask = out[skills].sum(axis=1) > 0
        out = out[mask]

    return out
