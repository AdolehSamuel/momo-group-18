# MoMo Analytics

GROUP 8

Process, analyze, and visualize Mobile Money (MoMo) SMS data end‑to‑end. This project ingests XML exports of SMS, cleans and categorizes transactions, loads them into a relational database (SQLite for now), and powers a lightweight analytics dashboard for insights.


✨ Key Features

ETL Pipeline: Parse XML → Clean & Normalize → Categorize → Load to DB
Relational Storage (SQLite): Durable, queryable transaction history
Analytics-Ready Outputs: Aggregations for charts, KPIs, and tables
Simple Frontend Dashboard: HTML/CSS/JS visualizations
Optional API (FastAPI): Serve transactions and analytics programmatically
Environment-Driven Config: Reproducible runs across machines



🧭 Architecture Diagram


   <img width="190" height="519" alt="image" src="https://github.com/user-attachments/assets/de797767-ae43-41ac-b71a-74cf47d3f76e" />



 🧱 Scrum Board
 



 🧰 Tech Stack

  Language: Python 3.x
  ETL: Standard library + lxml (or ElementTree), Pandas (optional), custom cleaners
  Database: SQLite (dev). Ready to swap to Postgres later
  API (optional): FastAPI + Uvicorn
  Frontend: HTML, CSS, vanilla JS (Chart.js or similar)
  Config: .env with environment variables
  Testing: pytest



📁 Project Structure (Planned)

```
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── db.sqlite3
│   └── logs/
├── etl/
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
│   ├── app.py
│   ├── db.py
│   └── schemas.py
├── scripts/
│   ├── run_etl.sh
│   ├── export_json.sh
│   └── serve_frontend.sh
└── tests/
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py
```

---

⚙️ Installation

 1) Clone

```bash
git clone <your-repo-url>
cd momo-analytics
```

 2) Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Environment variables

Create a `.env` file (use `.env.example` as a guide). Example values:

```
# ETL
RAW_XML_DIR=./data/raw
PROCESSED_DIR=./data/processed
DB_PATH=./data/db.sqlite3
LOG_DIR=./data/logs

# API (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

---

🚚 ETL Pipeline

Entry point: `etl/run.py`

1. Parse XML (`etl/parse_xml.py`)

    Read SMS export(s) in XML
    Extract timestamp, amount, counterparty, reference, message
2. Clean & Normalize (`etl/clean_normalize.py`)

   * Standardize dates, currency, amounts, phone formats
   * Normalize message templates; handle duplicates
3. Categorize (`etl/categorize.py`)

   * Rules/regex to label transactions: *cash-in, cash-out, transfer, merchant, fees, reversal, airtime, bill pay*, etc.
4. Load DB (`etl/load_db.py`)

   * Create/upgrade tables; load normalized rows
   * Generate summary tables / materialized views (daily totals, by category, top counterparties)

Run:

```bash
python -m etl.run
```

Or with helper script:

```bash
bash scripts/run_etl.sh
```

Outputs:

* `data/db.sqlite3` – relational store
* `data/processed/` – cleaned CSV/JSON exports (optional)
* `data/logs/` – run logs

---

 🗄️ Database (SQLite)

Suggested tables (simplified):

transactions

* `id` (PK), `timestamp`, `direction` (in/out), `amount`, `currency`, `category`, `counterparty`, `reference`, `message_hash` (for dedupe), `raw_id`

raw\_messages

* `raw_id` (PK), `received_at`, `sender`, `body`, `source_file`

aggregates\_daily

* `date`, `total_in`, `total_out`, `net`, `txn_count`

---

🧪 Testing

Run unit tests for core stages:

```bash
pytest -q
```

 `test_parse_xml.py`: parsing correctness, sample fixtures
 `test_clean_normalize.py`: amount/date normalization, dedupe
 `test_categorize.py`: rules classification coverage

---

🌐 Optional API (FastAPI)

Serve data to the dashboard or 3rd‑party tools.
Run API:

```bash
uvicorn api.app:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000} --reload
```

**Example endpoints** (planned):

* `GET /health` – service check
* `GET /transactions?limit=...&category=...`
* `GET /analytics/daily` – time series
* `GET /analytics/categories` – distribution by category

`api/schemas.py` documents response models.

---

 🖥️ Frontend Dashboard

A static dashboard reads API JSON (or local JSON files exported from ETL) and visualizes time series, category breakdowns, and top entities.

**Serve locally:**

```bash
bash scripts/serve_frontend.sh
```

Open `index.html` in your browser. Core assets:

* `web/styles.css`
* `web/chart_handler.js`

**Charts & Tables**

* Daily totals (line chart)
* In vs Out vs Fees (stacked bars)
* Category distribution (doughnut/pie)
* Top counterparties (table)

---

 🧵 Usage Workflow

1. Export MoMo SMS as **XML** (e.g., from your device/backup tool), place files in `data/raw/`.
2. Configure `.env` paths if needed.
3. Run ETL to populate `db.sqlite3`.
4. Start **API** (optional).
5. Open the **dashboard** to explore insights.

---

🛡️ Data & Security Notes

* Treat MoMo data as **sensitive**. Do not commit real SMS/XML or DB files.
* `.gitignore` should exclude `data/raw/`, `data/db.sqlite3` and any secrets.
* Consider anonymization (hashing phone numbers) for demos.

---

🔧 Scripts

* `scripts/run_etl.sh` – run the ETL end‑to‑end
* `scripts/export_json.sh` – export selected tables to JSON for the frontend
* `scripts/serve_frontend.sh` – quick local static server

---

 🧾 Requirements

* Python 3.x
* lxml (or ElementTree), fastapi+uvicorn (optional), pandas (optional), pytest
* SQLite (bundled with Python)

See `requirements.txt` for exact versions.

---

 🧑‍💻 Contributors

* **Blessing Ingabire** – `blessiingab`
* **Tabitha Dorcas Akimana** – `tdorcas-akim`
* **Adoleh Samuel** – `AdolehSamuel`



