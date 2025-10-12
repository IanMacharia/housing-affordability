# Housing Affordability Dashboard

An interactive dashboard exploring housing prices, rents, and incomes for African cities (starting with Nairobi).
Tracks trends over time and highlights neighborhoods with the most affordable options.

## Quick start (local)

1. **Create venv & install**
   \python -m venv .venv && . .\.venv\Scripts\Activate.ps1\
   \pip install -r requirements.txt\

2. **Environment**
   Copy \.env.sample\ → \.env\ and set values (e.g., \APP_PORT=8501\).

3. **Run**
   \streamlit run src\App.py --server.port 8501\

## Project layout

- \src/\ — app code (Streamlit entrypoint at \src\App.py\)
- \local_data/\ — **ignored** local data folder
- \
otebooks/\ — exploration
- \	ests/\ — unit tests
- \.github/workflows/ci.yml\ — CI pipeline

## Collaboration (you & Kate)

- Create feature branches: \eat/<short-description>\
- Open a Pull Request to \main\
- Keep PRs small; add a short summary and link related issues

## Roadmap (initial)
- [ ] Data sourcing (Nairobi): prices, rents, income benchmarks
- [ ] Cleaning & joins
- [ ] City + ward-level visuals
- [ ] Affordability index prototype
- [ ] Deploy preview



CI check: 2025-10-12T15:57:59.5923539-04:00
