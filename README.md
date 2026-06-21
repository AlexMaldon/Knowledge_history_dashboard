# Courses history dashboard

Interactive Streamlit dashboard to explore a career-long history of completed courses and certifications — built to visualize how a learning path evolves over time across platforms, subject areas, and technical skills.

## Why this project

Whilst some people enjoy sunbathing on the beach, what I’m really passionate about is learning something new every day. As my job and hobby involve analysing data, here’s the story of my learning journey !

Tracking decades of professional development (courses, certifications, bootcamps) in a spreadsheet makes it hard to see the bigger picture: which platforms were used most, how subject focus shifted over the years, and when specific skills (R, Python, SQL, Cloud/MLOps, Generative AI...) entered the picture. This dashboard turns that flat spreadsheet into an explorable, filterable view.

## Features

- 📈 **Courses per year** — trend of learning activity over time
- 🏛️ **Top platforms** — which platforms (Coursera, LinkedIn Learning, Google Cloud, Datacamp, etc.) were used most
- 📚 **Courses by subject area** — distribution across business intelligence, modelling, visualization, production implementation, etc.
- 🛠️ **Skill focus** — total courses tagged per skill (R, Python, SQL, Excel, Tableau, Power BI, IA/ML, Cloud/MLOps...)
- 🕒 **Skill evolution over time** — a stacked area chart showing how skill focus shifted across a career, e.g. moving from classic BI tools toward Python, ML, and Cloud/MLOps in recent years
- 🔍 **Interactive filters** — by year range, subject area, platform, and skill tag

## Tech stack

- Python 3.11
- Streamlit (dashboard UI)
- Pandas (data handling)
- Plotly (visualizations)

## Project structure

```
ai-portfolio-dashboard/
├── data/
│   └── courses_history.csv     # Personal courses/certifications history
├── src/
│   ├── app.py                  # Streamlit app entrypoint
│   ├── course_analytics.py     # Data transformation & aggregation logic
│   └── utils.py                # Data loading helpers
├── requirements.txt
└── README.md
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

## Data structure

Each row in `courses_history.csv` represents one completed course, with:

| Column | Description |
|---|---|
| `idcourse` | Unique identifier |
| `PLATAFORMA` | Platform / provider (Coursera, LinkedIn Learning, Google Cloud, etc.) |
| `TITULO` | Course title |
| `AÑO` | Year completed |
| `AREA` | Subject area (Modelling, Visualization, Business intelligence, Production implementation, etc.) |
| `Marketing`, `SPSS`, `EXCEL`, `TABLEAU`, `POWERBI`, `SQL`, `R`, `PYTHON`, `IA ML`, `Cloud MLOps` | Binary skill tags — `1` if the course covered that skill |

## License

MIT
