# MoMo Analytics – Group 18

Process, analyze, and visualize **Mobile Money (MoMo) SMS data** end-to-end. This project ingests XML exports of SMS, cleans and categorizes transactions, stores them in a relational database (SQLite), and powers a lightweight analytics dashboard for insights.

---

## Contributors

- **Blessing Ingabire** – [blessiingab](https://github.com/blessiingab)
- **Tabitha Dorcas Akimana** – [tdorcas-akim](https://github.com/tdorcas-akim)
- **Adoleh Samuel** – [AdolehSamuel](https://github.com/AdolehSamuel)
- **Chibueze Onugha** -[Chibueze Onugha](https://github.com/Nnamdi004)

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

[High-Level System Architecture](https://drive.google.com/file/d/1pSbZjMMmSFaWmH_uyw1qczj8WgIJIc_J/view?usp=sharing)

**Scrum Board** -

[GitHub Projects](https://github.com/users/AdolehSamuel/projects/1/views/1?layout=board)

---

## Tech Stack

| Component      | Technology                                               |
| -------------- | -------------------------------------------------------- |
| Language       | Python 3.x                                               |
| ETL            | Standard library + lxml / ElementTree, Pandas (optional) |
| Database       | SQLite (dev) → Postgres (future)                         |
| API (Optional) | FastAPI + Uvicorn                                        |
| Frontend       | HTML, CSS, JS (Chart.js or similar)                      |
| Config         | `.env` for environment variables                         |
| Testing        | pytest                                                   |

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

## Quick Start (Local)

1. Requirements

- Python 3.11+ recommended
- macOS/Linux or Windows

2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the API server (auto-initializes the SQLite DB from XML)

```bash
python api/app.py
# or with reload
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

5. Authenticate (Basic Auth)

```bash
BASIC=$(printf 'admin:secret' | base64)
curl -H "Authorization: Basic $BASIC" http://localhost:8000/transactions
```

Notes:

- On startup, the server deletes `data/db.sqlite3` and repopulates it from `data/raw/momo.xml`.
- If you see `ModuleNotFoundError: dsa`, run the server from the repo root or use `uvicorn api.app:app`.

---

## Database Design

The database stores normalized Mobile Money transaction data with proper constraints, indexes, and foreign keys for referential integrity.

### Schema Overview

| Table                      | Purpose                     | Key Columns / Constraints                                     |
| -------------------------- | --------------------------- | ------------------------------------------------------------- |
| `users`                    | Mobile money users          | `user_id` (PK), `phone_number`, `name`                        |
| `transaction_categories`   | Categories for transactions | `category_id` (PK), `category_name`, `description`            |
| `transactions`             | Core transactions           | `transaction_id` (PK), FK → `users`, `transaction_categories` |
| `transaction_participants` | Sender/Receiver mapping     | `participant_id` (PK), FK → `transactions`, `users`           |
| `system_logs`              | Logs for transactions       | `log_id` (PK), FK → `transactions`                            |

### ER Diagram (Simplified)

```
users (1) ──< transactions >── (1) transaction_categories
      \                       /
       \                     /
        └─< transaction_participants >── system_logs
```

### Sample Data Inserts

```sql
INSERT INTO users (phone_number, name) VALUES
('1234567890', 'Alice'),
('2345678901', 'Bob'),
('3456789012', 'Charlie'),
('4567890123', 'David'),
('5678901234', 'Eva');

INSERT INTO transaction_categories (category_name, description) VALUES
('Transfer', 'Money transfers'),
('Bill', 'Bill payments'),
('Purchase', 'Goods and services'),
('Refund', 'Refunds'),
('Donation', 'Charity donations');
```

Full insert scripts available in `database_setup.sql`.

### JSON Mapping

Example of a transaction with nested relationships:

```json
{
  "transaction_id": 1,
  "amount": 100.5,
  "currency": "USD",
  "transaction_date": "2025-09-19T12:00:00Z",
  "fee": 1.5,
  "category": {
    "category_id": 1,
    "category_name": "Transfer"
  },
  "sender": {
    "user_id": 2,
    "name": "Bob"
  },
  "receiver": {
    "user_id": 1,
    "name": "Alice"
  },
  "logs": [{ "log_id": 1, "log_type": "INFO", "message": "Transaction ok" }]
}
```

### Testing the Database

```bash
mysql -u root -p
CREATE DATABASE momo_analytics_group_18;
USE momo_analytics_group_18;
SOURCE database_setup.sql;
```

Run CRUD tests:

```sql
SELECT * FROM transactions;
INSERT INTO transactions (...) VALUES (...);
UPDATE transactions SET amount = 200 WHERE transaction_id = 1;
DELETE FROM transactions WHERE transaction_id = 1;
```

### Indexes & Constraints

- **PRIMARY KEYS** on all main tables
- **FOREIGN KEYS** for relationships
- **CHECK constraints** for valid ENUM-like values
- **Indexes** on `transaction_date` and `category_id` for analytics queries

---

## ETL Pipeline

**Entry point**: `etl/run.py`

Stages:

1. **Parse XML** → Extract timestamp, amount, counterparty, reference, message
2. **Clean & Normalize** → Standardize dates, currency, amounts, phone formats
3. **Categorize** → Apply rules/regex for _cash-in, cash-out, transfer, merchant, fees,_ etc.
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

Docs:

- See `docs/api_docs.md` for endpoint usage and examples.

Implemented endpoints:

- `GET /transactions` → List all
- `GET /transactions/{id}` → Get one
- `POST /transactions` → Create
- `PUT /transactions/{id}` → Update
- `DELETE /transactions/{id}` → Delete

Auth:

- All endpoints require Basic Auth: `Authorization: Basic <base64(admin:secret)>`

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

Further reading:

- `pdf_report.md` includes an intro to API security, endpoint docs, DSA results, and Basic Auth limitations.

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

---

## DSA Benchmark (Optional)

Compare linear search vs dictionary lookup for finding transactions by id:

```bash
python dsa/search_benchmark.py
```

The script prints average timings and the estimated speedup. Ensure at least 20 records are present (the server’s startup population provides this).
