# Housing Affordability Dashboard, master checklist

## Global setup
* [ ] Create repo and enable branch protection on main
* [ ] Add collaborators with write access
* [ ] Create Project board and link to this repo
* [ ] Add labels: phase: planning, phase: data, phase: prep, phase: analysis, phase: viz, phase: deploy, type: task, type: bug, priority: high, priority: normal
* [ ] Add issue template and PR template
* [ ] Create docs folder and paste PROJECT_PLAN.md and this checklist
* [ ] Add CODEOWNERS with Ian and Kate on the whole repo

## Sprint 0, Planning
* [ ] One page brief with problem, users, city choice
* [ ] Metric definitions with formulas and acceptance criteria
* [ ] Wireframes for map, trends, compare
* [ ] Project views saved in GitHub Projects: Backlog, This sprint, Ian pass, Kate pass, In review

## Sprint 1, Data sourcing
* [ ] Data catalog with source URL, license, refresh cadence
* [ ] Raw snapshots saved under data/raw/YYYYMMDD
* [ ] Ingestion notebook or script runs locally
* [ ] Issue: confirm boundary shapefile and neighborhood names

## Sprint 2, Preprocessing
* [ ] Join listings to neighborhoods, verify spatial coverage
* [ ] Currency and inflation adjustments documented
* [ ] Tidy tables saved under data/processed
* [ ] Data profile report saved under reports/

## Sprint 3, Analysis
* [ ] Affordability metrics computed: price to income, rent burden, percentile ranks
* [ ] Sanity checks: medians by year, outlier review
* [ ] Tests for metric functions passing
* [ ] Curated datasets saved under data/curated

## Sprint 4, Visualization
* [ ] Prototype dashboard with map, trends, compare
* [ ] Filters: time, neighborhood, dwelling type
* [ ] Titles, footnotes, and tooltips drafted
* [ ] Screenshots saved for README

## Sprint 5, Deployment
* [ ] Hosted app URL working
* [ ] Refresh process documented or scheduled
* [ ] README with step by step reproduce guide
* [ ] Final slides and short demo video linked

