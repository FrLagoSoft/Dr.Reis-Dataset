# Agile Process: Biscayne Bay Water Quality Explorer

This project was managed with a lightweight **Scrum-style** process: user stories in a prioritized backlog, short time-boxed sprints, a visible task board (GitHub Projects), small commits tied to stories, and a retrospective.

> Board: https://github.com/users/YOUR-USERNAME/projects/N  <!-- replace -->

## Product goal

Give a non-technical user (a student, resident, or environmental-agency staffer) a quick, trustworthy way to explore one survey of Biscayne Bay water quality without writing code.

## Personas

- **Maria, environmental science student**: wants to see trends and relationships for a lab report.
- **Prof. Reis, instructor**: wants clean, documented, deployable code.

## Product backlog (user stories)

Priority uses **MoSCoW** (Must / Should / Could). Points are relative effort (Fibonacci).

| ID | User story | Priority | Pts | Sprint |
|---|---|---|---|---|
| US-1 | As a user, I want the app to load the water-quality dataset automatically so I can start exploring immediately. | Must | 2 | 1 |
| US-2 | As a user, I want an overview with headline averages so I understand the data at a glance. | Must | 2 | 1 |
| US-3 | As a user, I want to pick a parameter and see it plotted over time so I can spot trends. | Must | 3 | 1 |
| US-4 | As a developer, I want the app on GitHub with a requirements.txt so it can be deployed. | Must | 1 | 1 |
| US-5 | As a user, I want to filter all views to a time window so I can focus on part of the survey. | Must | 3 | 2 |
| US-6 | As a user, I want to compare two parameters on a scatter plot so I can see relationships. | Must | 3 | 2 |
| US-7 | As a user, I want a map of where readings were taken so I understand the spatial pattern. | Should | 3 | 2 |
| US-8 | As a user, I want to choose which table columns to see so the data isn't overwhelming. | Should | 2 | 2 |
| US-9 | As a user, I want plain-English insights so I don't have to interpret statistics myself. | Should | 3 | 3 |
| US-10 | As a user, I want to be warned about unreliable sensor readings so I don't draw wrong conclusions. | Should | 2 | 3 |
| US-11 | As a user, I want to upload my own CSV so I can reuse the dashboard for other surveys. | Could | 3 | 3 |
| US-12 | As a user, I want to download filtered data so I can use it in my own analysis. | Could | 1 | 3 |
| US-13 | As a user, I want a public URL so I can open the app without installing anything. | Must | 2 | 3 |

## Definition of Done

A story is done when:

1. The feature works locally with `streamlit run app.py` and shows no errors or warnings.
2. Every chart has a title, labeled axes with units, and a legend or color bar.
3. New functions have a docstring; non-obvious lines have comments.
4. The change is committed with a message referencing the story (e.g. `US-6: add scatter plot`).
5. The card is moved to **Done** on the board.

## Sprints

| Sprint | Goal | Stories |
|---|---|---|
| 1 | Minimum viable dashboard: data loads and one chart works | US-1 – US-4 |
| 2 | Interactivity: filtering, comparison, and spatial view | US-5 – US-8 |
| 3 | Polish, trust, and release | US-9 – US-13 |

### Sprint review notes

- **Sprint 1:** Discovered the `Time` column only stores minutes:seconds, and `Date m/d/y` has trailing spaces in its name. Built a proper `Timestamp` column in `data_utils.load_data()` before charting.
- **Sprint 2:** Refactored the single script into `app.py`, `data_utils.py`, and `charts.py` so UI, data logic, and visuals are separated. A single `PARAMETERS` dictionary now drives every dropdown and axis label.
- **Sprint 3:** The temperature-vs-oxygen correlation came out *positive* in this survey, the opposite of what physics predicts. Changed the Insights text to adapt to the actual result instead of hardcoding a conclusion. Added data-quality warnings for negative turbidity and chlorophyll readings.

## Retrospective

**What went well:** Splitting the code into modules early made later features (map, insights) quick to add. Testing each story against the Definition of Done caught missing axis units before release.

**What didn't:** I initially wrote an insight before checking the data, and it contradicted the actual numbers. Assumptions need to be verified against the dataset.

**What I'll change for Project 2:** Write the acceptance criteria for each story *before* coding, and keep the board updated daily rather than at the end of each sprint.
