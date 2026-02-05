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
