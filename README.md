# Agentic Network Logger 🐯

## Project Overview
This project is a **Proof of Concept (PoC)** built to demonstrate high-velocity time-series data ingestion and database performance tuning using **TimescaleDB** and **Python**.

The application simulates a "Network Monitoring Agent" that pushes real-time traffic logs (Device ID, Bytes Transferred, Risk Score) to a cloud PostgreSQL instance. The primary goal was to explore **Database Internals (MVCC)** and **Query Optimization** in a production-like environment.

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Database:** PostgreSQL 16 (Timescale Cloud)
* **Libraries:** `psycopg2-binary`
* **Concepts:** Hypertables, B-Tree Indexing, MVCC, VACUUM, EXPLAIN ANALYZE

## 🚀 Key Features Implemented

### 1. Time-Series Partitioning (Hypertables)
Instead of a standard PostgreSQL table, I utilized **TimescaleDB Hypertables** to automatically partition data by time. This ensures efficient ingestion rates for continuous network logs.
```sql
SELECT create_hypertable('network_logs', 'time');
```

### 2. Database Internals & Storage Management
I simulated a "storage bloat" scenario to analyze PostgreSQL's **Multi-Version Concurrency Control (MVCC)**.
* **Experiment:** Performed bulk `UPDATE` operations to generate "Dead Tuples."
* **Observation:** Queried `_hyper%` chunks to locate dead tuples hidden behind the parent hypertable (which initially reported 0 rows).
* **Resolution:** Executed `VACUUM (VERBOSE, ANALYZE)` to reclaim storage space and optimize the relation.

### 3. Query Performance Tuning
I benchmarked query latency using `EXPLAIN ANALYZE` to compare execution plans.
* **Before Optimization:** A query for a specific device triggered a full **Sequential Scan** (reading all chunks).
* **After Optimization:** Implemented a B-Tree Index on `device_id`, converting the operation to a **Bitmap Heap Scan / Index Scan**, significantly reducing I/O cost.

## 📦 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aryashubh001/agentic-network-logger.git
    cd agentic-network-logger
    ```

2.  **Install dependencies:**
    ```bash
    pip install psycopg2-binary
    ```

3.  **Configure Database:**
    * Create a service on [Timescale Cloud](https://console.cloud.timescale.com/).
    * Update the `DB_PASS`, `DB_HOST`, and `DB_PORT` in `agent.py`.

4.  **Run the Agent:**
    ```bash
    python agent.py
    ```

## 📊 Performance Results

| Metric | Before Indexing | After Indexing |
| :--- | :--- | :--- |
| **Scan Type** | Sequential Scan | Index Scan |
| **Execution Strategy** | Full Table Read | B-Tree Lookup |
| **Cost** | High (Linear O(n)) | Low (Logarithmic O(log n)) |

## 📝 License
This project was created as a technical demonstration for a Database Support Engineer role.
