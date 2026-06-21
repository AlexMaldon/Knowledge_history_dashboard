"""
app.py

Professional Courses History Dashboard
Interactive Streamlit app to explore a career-long history of completed
courses and certifications: trends over time, platforms used, subject
areas, and skill focus evolution.

Run with: streamlit run src/app.py
"""

import streamlit as st
import plotly.express as px

from utils import load_courses
from course_analytics import (
    clean_courses,
    courses_per_year,
    courses_per_platform,
    courses_per_area,
    skill_totals,
    skill_evolution_by_year,
    summary_metrics,
    filter_courses,
    AREA_ORDER,
    SKILL_COLUMNS,
)

st.set_page_config(
    page_title="Courses History Dashboard",
    page_icon="🎓",
    layout="wide",
)

# ── Header ────────────────────────────────────────────────────────────────
st.title("🎓 Professional Courses History Dashboard")
st.markdown(
    "<p style='font-size:18px; color:gray;'>An interactive view of a "
    "career-long learning path: courses and certifications completed "
    "across platforms, subject areas, and skills.</p>",
    unsafe_allow_html=True,
)

# ── Load and clean data ──────────────────────────────────────────────────
raw_df = load_courses()
df = clean_courses(raw_df)

# ── Sidebar filters ───────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

min_year = int(df["AÑO"].dropna().min())
max_year = int(df["AÑO"].dropna().max())
year_range = st.sidebar.slider(
    "Year range", min_value=min_year, max_value=max_year,
    value=(min_year, max_year),
)

area_options = sorted(df["AREA"].dropna().unique())
area_filter = st.sidebar.multiselect("Subject area", area_options, default=[])

platform_options = sorted(df["PLATAFORMA"].dropna().unique())
platform_filter = st.sidebar.multiselect("Platform", platform_options, default=[])

skill_filter = st.sidebar.multiselect("Skill tag", SKILL_COLUMNS, default=[])

filtered = filter_courses(
    df,
    year_range=year_range,
    areas=area_filter or None,
    platforms=platform_filter or None,
    skills=skill_filter or None,
)

# ── Summary metrics ───────────────────────────────────────────────────────
metrics = summary_metrics(filtered)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total courses", metrics["total_courses"])
c2.metric("Year range", metrics["year_range"])
c3.metric("Platforms used", metrics["n_platforms"])
c4.metric("Subject areas", metrics["n_areas"])
c5.metric("Top skill", metrics["top_skill"])

st.divider()

# ── Skill evolution over time ─────────────────────────────────────────────
st.subheader("🕒 How skill focus has evolved over time")
evolution = skill_evolution_by_year(filtered)
if len(evolution) > 0:
    fig_evo = px.area(
        evolution, x="AÑO", y="count", color="skill",
        labels={"AÑO": "Year", "count": "Courses"},
    )
    st.plotly_chart(fig_evo, use_container_width=True)
else:
    st.info("No skill-tagged courses match the current filters.")
    
# ── Skill totals ──────────────────────────────────────────────────────────
st.subheader("🛠️ Skill focus — total courses per skill tag")
totals = skill_totals(filtered)
fig_skills = px.bar(
    totals, x="skill", y="count",
    labels={"skill": "Skill", "count": "Courses"},
)
st.plotly_chart(fig_skills, use_container_width=True)    
    

# ── Two-column charts: platform + area ───────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📚 Courses by subject area")
    per_area = courses_per_area(filtered)
    fig_area = px.pie(
        per_area, names="AREA", values="count", hole=0.4,
        category_orders={"AREA": AREA_ORDER},
    )
    st.plotly_chart(fig_area, use_container_width=True)
    
with col2:
    st.subheader("🏛️ Top platforms")
    per_platform = courses_per_platform(filtered)
    fig_platform = px.bar(
        per_platform, x="count", y="PLATAFORMA", orientation="h",
        labels={"PLATAFORMA": "Platform", "count": "Courses"},
    )
    fig_platform.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_platform, use_container_width=True)


# ── Detailed table ────────────────────────────────────────────────────────
st.subheader("📋 Course details")
display_cols = ["AÑO", "PLATAFORMA", "TITULO", "AREA"]
st.dataframe(
    filtered[display_cols].sort_values("AÑO", ascending=False),
    use_container_width=True,
    height=400,
)

st.divider()
st.caption(
    "Data source: personal courses history. Built as a portfolio project "
    "to demonstrate data analysis and dashboard design with Streamlit."
)

# ── Courses per year (trend) ─────────────────────────────────────────────
st.subheader("📈 Courses completed per year")
per_year = courses_per_year(filtered)
fig_year = px.bar(
    per_year, x="AÑO", y="count",
    labels={"AÑO": "Year", "count": "Courses completed"},
)
fig_year.update_layout(showlegend=False)
st.plotly_chart(fig_year, use_container_width=True)