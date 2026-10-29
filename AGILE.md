# Agile Process: Biscayne Bay Water Quality Explorer

This project was managed with a lightweight **Scrum-style** process: user stories in a prioritized backlog, short time-boxed sprints, a visible task board (GitHub Projects), small commits tied to stories, and a retrospective.

> Board: https://github.com/FrLagoSoft/Dr.Reis-Dataset

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

## Retrospective

**What went well:** Splitting the code into modules early made later features (map, insights) quick to add. Testing each story against the Definition of Done caught missing axis units before release.

**What didn't:** Putting the actual data file into the folders and translating that into the actual app data was a struggle. The first time I deployed the app itself, I realized that the data didn't even show at all. It was shocking and I had to trace back what the variables all fetched from my csv file, and try to edit those values. 

**What I'll change for Project 2:** Follow more closely through the class lectures, so that I don't have crises in general data structures like this. 
