# Comprehensive Data Strategy & Operational Guidebook for the Housing Affordability Dashboard

*File:* `docs/data_strategy_and_guidebook.md` • *Repo:* `housing-affordability-dashboard`

---

## Table of Contents

1. [Data Strategy](#section-1—data-strategy)
2. [Operational Guidebook (Ingest → KPI → Viz)](#section-2—operational-guidebook-ingest--kpi--viz)
3. [KPI / Metric Dictionary](#section-3—kpi--metric-dictionary)
4. [References](#section-4—references-apa)
5. [Appendix — Command Snippets](#appendix—command-snippets)

---

## Section 1 — Data Strategy

### 1.1 Project Overview

* **Goal:** Deliver a robust, reproducible Housing Affordability Dashboard for *Nairobi* that quantifies affordability across time and space and supports policy and market insights.
* **Scope:** Analyze *prices & rents*, *income & expenditure*, and *inflation* to compute affordability ratios and related KPIs. Spatial focus at *ward* and *sub-county*, with county-level rollups.
* **Primary stakeholders:** Analysts, internal audit & finance partners, urban planners, civic-tech collaborators.
* **Intended insights:**

  * Affordability trends (real terms) and price inflation/deflation.
  * Market segmentation by property type and geography.
  * Income-to-price and income-to-rent ratios; rent burden shares.

### 1.2 Data Architecture

#### Sources in scope

* **KNBS Real Estate Survey** — periodic cross-sectional survey (urban market aggregates).
* **KBA Housing Price Index (HPI)** — quarterly index derived from financed transactions.
* **Kaggle Nairobi House Prices** — listing-level sample (transaction/list price + attributes).
* **Census & Boundaries (2019, WRI/IGISMAP)** — spatial backbone for joins.
* **CPI (KNBS/NSO)** — monthly deflator to produce real values.

#### Logical flow

1. **Ingestion:** Fetch KNBS (PDF/XLS), KBA (web table/CSV), Kaggle (CSV). Persist raw snapshots with date stamps.
2. **Cleaning:** Normalize column names, datatypes, and units; geocode/align to *ward/sub-county*.
3. **Transformation:** Create standardized tables for *prices*, *rents*, *index series*, and *income proxies*. Apply CPI deflation.
4. **Metrics:** Compute KPIs (affordability ratio, income-to-rent ratio, price-per-sqm, price index trend, etc.).
5. **Visualization:** Publish to Streamlit or Power BI; spatial heatmaps and trend charts.

#### Repository alignment

```text
/data/
  /raw/
    /knbs/         <-- PDFs/XLS from KNBS Real Estate Survey (dated folders)
    /kba/          <-- KBA HPI extracts (CSV / HTML snapshot)
    /kaggle/       <-- Kaggle CSV (original files)
  /interim/        <-- cleaned-but-not-final parquet/csv
  /processed/      <-- model-ready tables (parquet/csv)

/pipelines/
  ingest_raw.py
  etl_preprocess.py
  metrics_compute.py

/src/
  /utils/    io.py, geo.py
  /validation/ dq_checks.py
  /metrics/  affordability.py

/dashboards/    (streamlit app or PBIX)
/docs/          (this guide)
```

### 1.3 Governance & Quality

#### FAIR Principles

* **Findable:** Every dataset receives a README and `dataset.yml` (name, owner, source URL, license, refresh cadence).
* **Accessible:** Raw snapshots kept under `/data/raw/<source>/YYYY-MM-DD/`; access controlled via Git and repository permissions.
* **Interoperable:** Standard column naming (`snake_case`), units (KES, sqm), and shared keys (`year`, `quarter`, `county_code`, `subcounty_code`, `ward_code`).
* **Reusable:** Clear licenses, provenance logs, and schema contracts; include transform notebooks or tests.

#### DAMA-DMBoK Domains

* **Data Quality:** Define constraints (e.g., non-negative prices, plausible rent/price ranges; ward codes must exist in reference table).
* **Metadata:** Use `dataset.yml` (owner, description, schema, source link, license, update frequency, QA checks).
* **Governance:** Change control via PRs; mandatory data-quality checks (CI) before merging to `main`.
* **Auditability:** Keep immutable raw snapshots; log ETL run metadata (source hash, row counts) to `/data/_summaries/etl_runs.csv`.

### 1.4 Security & Compliance

* **Privacy:** Kaggle listing geocodes must be aggregated to ward/sub-county for public sharing. Do not expose exact household addresses.
* **Access Control:** Use GitHub branch protection and repository roles. Store secrets (if any) via environment variables; avoid committing secrets.
* **Licensing:** Respect KNBS/KBA terms; retain attribution; note that Kaggle datasets may be user-contributed—verify license before redistribution.

### 1.5 Maintenance & Scalability

* **Versioning:** Branch per feature (`feat/etl-knbs`), squash-merge PRs, tag releases (`vYYYY.MM`) when dashboards update.
* **Refresh Cadence:** KBA (quarterly), CPI (monthly), listings (weekly snapshot optional), KNBS Real Estate Survey (periodic). Automate cron/GitHub Actions as needed.
* **Scalability:** Store model-ready tables in columnar format (Parquet). Partition by `year`, `county`. Abstract joins and KPI logic in `/src/metrics/affordability.py`.

### 1.6 Citations (Frameworks)

* DAMA International (2017). *DAMA-DMBoK 2.*
* Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles. *Scientific Data.*
* McKinsey & Company (2020). *The Data-Driven Enterprise of 2025.*

---

## Section 2 — Operational Guidebook (Ingest → KPI → Viz)

### 2.1 Phase 1 — Ingest

* **KNBS Real Estate Survey** → `/data/raw/knbs/` (PDF/XLS). Save original files with date folders.
* **KBA HPI** → `/data/raw/kba/` (CSV/HTML). If scraping, export normalized CSV and include a readme with the URL and retrieval date.
* **Kaggle Nairobi House Prices** → `/data/raw/kaggle/` (CSV). Keep original file name and a checksum.

**Tools:** Python, `pandas`, `requests`, `openpyxl`

```bash
python -m pipelines.ingest_raw
```

### 2.2 Phase 2 — Clean & Transform

* **Standardize schema:** `price_kes`, `rent_kes`, `bedrooms`, `property_type`, `size_sqm`, `year`, `quarter`, `county_code`, `subcounty_code`, `ward_code`.
* **Handle missing values:** Impute only where safe (e.g., infer quarter from month); otherwise flag rows.
* **Geocoding / Region matching:** Map listings to wards/sub-counties using centroid-in-polygon; persist join table for reproducibility.
* **Inflation adjustment:** Join CPI (KNBS/NSO) by month/quarter; compute `price_kes_real`, `rent_kes_real` in the chosen base year (e.g., 2023).

```bash
python -m pipelines.etl_preprocess
```

### 2.3 Phase 3 — Merge & Compute Metrics

* **Join strategy:**

  * *Spatial:* Use `ward_code` → `subcounty_code` → `county_code` hierarchy.
  * *Temporal:* Aggregate quarterly series (KBA) to annual where necessary to match survey years (KNBS snapshots); CPI aligns everything to real terms.
* **Feature engineering:** price per sqm, rent burden (% income), annualized change, deciles/percentiles by ward.

```bash
python -m pipelines.metrics_compute
```

### 2.4 Phase 4 — Validation & QA

* Run `/src/validation/dq_checks.py` to validate:

  * Schema adherence (required columns present, correct dtypes).
  * Range checks (e.g., `0 <= rent_kes_real <= 2e6`).
  * Outlier detection (IQR or z-score), duplicates, and spatial mismatches.
* Emit logs and summaries to `/data/_summaries/` (CSV + HTML).

### 2.5 Phase 5 — Visualization

* **Streamlit / Power BI:** consume `/data/processed/` parquet/CSV.
* **Visual mappings:**

  * Affordability trendlines (county and metro views; real terms).
  * Spatial heatmaps (ward/sub-county affordability ratio, rent burden).
  * Comparative bars (price per sqm by property type; income-to-rent ratio).

---

## Section 3 — KPI / Metric Dictionary

*All monetary values should be presented in **real KES** using CPI with a declared base year (e.g., 2023=100). Include a Data Notes tooltip on the dashboard to clarify sources and adjustments.*

| KPI                                  | Formula / Composition                                                       | Data Source(s)                                                 | Description                                                                      | Dashboard Use                                                  |
| ------------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Affordability Ratio**              | `median_house_price_real / median_annual_household_income_real`             | KNBS Real Estate Survey (prices) + KIHBS/KeNADA (income) + CPI | Core ratio comparing purchase prices to incomes; lower is more affordable.       | **Core Metric** — headline card + county/ward comparison chart |
| **Price Index Trend**                | `(HPI_t - HPI_base) / HPI_base`                                             | KBA HPI                                                        | Quarterly price evolution; choose a base quarter.                                | Trendline widget with YoY/QtQ toggles                          |
| **Income to Rent Ratio**             | `median_monthly_income_real / median_monthly_rent_real`                     | KIHBS/KeNADA (income) + KNBS/Kaggle (rent) + CPI               | How many months of income are required per month of rent; proxy for rent burden. | Rent vs Income section: bar/violin by ward/sub-county          |
| **Rent Burden %**                    | `(median_monthly_rent_real / median_monthly_income_real) * 100`             | KNBS/Kaggle + KIHBS + CPI                                      | Share of income spent on rent (30%+ often flagged as burdensome).                | Choropleth heatmap by ward; distribution plot                  |
| **Price per Sq Meter**               | `sale_price_real / size_sqm`                                                | Kaggle (listings) + CPI                                        | Size-normalized price; enables cross-type comparison.                            | Comparative chart (box/strip) by property type and area        |
| **Average Mortgage to Income Ratio** | `avg_monthly_mortgage_payment_real / avg_monthly_income_real`               | KNBS (finance items) + KIHBS + CPI                             | Indicates repayment strain for financed buyers.                                  | Financial Stress panel                                         |
| **Annual Real Price Change**         | `(median_price_real_t - median_price_real_{t-1}) / median_price_real_{t-1}` | KNBS/KBA + CPI                                                 | Year-over-year real price appreciation/depreciation.                             | Sparkline + small-multiple charts by sub-county                |
| **Supply Context (Units)**           | `sum(units_by_project)`                                                     | CAHF Developments (optional)                                   | New supply proxy by county/sub-county.                                           | Context band / tooltip in price charts                         |

### 3.1 Metric Dependencies

* **All “_real” values** depend on the CPI join and selected base year.
* **Spatial metrics** depend on successful mapping of listings to *ward/sub-county*.
* **Income-based KPIs** depend on availability of KIHBS (or proxy microdata) for the relevant geography and time; if not available for 2023, interpolate from the last wave using CPI and KBA trend as a sensitivity check.

---

## Section 4 — References (APA)

* DAMA International. (2017). *DAMA-DMBoK 2: Data Management Body of Knowledge.*
* Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data, 3.*
* McKinsey & Company. (2020). *The Data-Driven Enterprise of 2025.*
* Kenya Bankers Association. (2023). *KBA Housing Price Index Q4 Report.*
* Kenya National Bureau of Statistics. (2022). *Real Estate Survey Report.*

---

## Appendix — Command Snippets

```bash
# 1) Ingest
python -m pipelines.ingest_raw

# 2) Clean & transform
python -m pipelines.etl_preprocess

# 3) Merge & compute metrics
python -m pipelines.metrics_compute

# 4) Run data-quality checks
python -m src.validation.dq_checks
```
