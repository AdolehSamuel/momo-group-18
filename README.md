# MoMo Analytics – Group 18  

Process, analyze, and visualize **Mobile Money (MoMo) SMS data** end-to-end. This project ingests XML exports of SMS, cleans and categorizes transactions, stores them in a relational database (SQLite), and powers a lightweight analytics dashboard for insights.  

---

##  Contributors  

- **Blessing Ingabire** – [blessiingab](https://github.com/blessiingab)  
- **Tabitha Dorcas Akimana** – [tdorcas-akim](https://github.com/tdorcas-akim)  
- **Adoleh Samuel** – [AdolehSamuel](https://github.com/AdolehSamuel)

---

## Key Features  

- **ETL Pipeline**: Parse XML → Clean & Normalize → Categorize → Load to DB  
- **Relational Storage**: SQLite for durable, queryable transaction history  
- **Analytics-Ready Outputs**: Aggregations for charts, KPIs, and tables  
- **Frontend Dashboard**: HTML/CSS/JS visualizations for insights  
- **Optional API (FastAPI)**: Serve transactions and analytics programmatically  
- **Environment-Driven Config**: Reproducible runs across machines  

---

## Architecture  

**System Diagram** - 

[High-Level System Architecture](https://drive.google.com/file/d/11vWZI0adX_xhK5yFidRbc_ZlMbNj6740/view?usp=sharing)  

**Scrum Board** - 

[GitHub Projects](https://github.com/users/tdorcas-akim/projects/1)  

---

## Tech Stack  

| Component     | Technology                           |
|---------------|--------------------------------------|
| Language       | Python 3.x                            |
| ETL            | Standard library + lxml / ElementTree, Pandas (optional) |
| Database       | SQLite (dev) → Postgres (future)      |
| API (Optional) | FastAPI + Uvicorn                    |
| Frontend        | HTML, CSS, JS (Chart.js or similar)  |
| Config          | `.env` for environment variables     |
| Testing         | pytest                               |

---

## Planned Project Structure  

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

## Installation  

```bash
# 1. Clone repository
git clone https://github.com/AdolehSamuel/momo-group-18.git
cd momo-group-18

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
```

Example `.env` values:
```
DATABASE_URL=********
```

---

## ETL Pipeline  

**Entry point**: `etl/run.py`  

Stages:  
1. **Parse XML** → Extract timestamp, amount, counterparty, reference, message  
2. **Clean & Normalize** → Standardize dates, currency, amounts, phone formats  
3. **Categorize** → Apply rules/regex for *cash-in, cash-out, transfer, merchant, fees,* etc.  
4. **Load DB** → Create tables, insert transactions, generate summary tables  

Run:
```bash
python -m etl.run
# or
bash scripts/run_etl.sh
```

Outputs:  
- `data/db.sqlite3` – database  
- `data/processed/` – cleaned CSV/JSON exports  
- `data/logs/` – ETL logs & errors  

---

## Database Schema (Simplified)  

**transactions**  
`id | timestamp | direction | amount | currency | category | counterparty | reference | message_hash | raw_id`  

**raw_messages**  
`raw_id | received_at | sender | body | source_file`  

**aggregates_daily**  
`date | total_in | total_out | net | txn_count`  

---

## Testing  

```bash
pytest -q
```

Covers:  
- `test_parse_xml.py` → XML parsing correctness  
- `test_clean_normalize.py` → data normalization, dedupe logic  
- `test_categorize.py` → category classification rules  

---

## API (FastAPI)  

Run:  
```bash
uvicorn api.app:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000} --reload
```

Planned endpoints:  
- `GET /health` → Health check  
- `GET /transactions` → Query transactions  
- `GET /analytics/daily` → Daily time series  
- `GET /analytics/categories` → Category breakdown  

---

## Frontend Dashboard  

Static HTML/JS dashboard for visualizing analytics.  

Serve locally:  
```bash
bash scripts/serve_frontend.sh
```
Open `index.html` in browser.  

Charts:  
- Daily totals (line chart)  
- In vs Out vs Fees (stacked bar)  
- Category distribution (doughnut/pie)  
- Top counterparties (table)  

---

## Data & Security  

- Treat MoMo data as **sensitive**: never commit raw XML or DB files  
- Use `.gitignore` for `data/raw/`, `data/db.sqlite3`, and secrets  
- Consider anonymization for demos  

---

## Scripts  

- `run_etl.sh` → Full ETL pipeline  
- `export_json.sh` → Export DB tables to JSON  
- `serve_frontend.sh` → Local static server  

---

## Requirements  

- Python 3.x  
- lxml / ElementTree  
- fastapi + uvicorn (optional)  
- pandas (optional)  
- pytest  
- SQLite (built-in)
