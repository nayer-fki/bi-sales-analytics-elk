# 📊 BI Sales Analytics – ELK Stack

## 🧩 Overview
This project provides a **Sales BI Analytics** solution using the **ELK Stack**.
It ingests sales-related data into **MongoDB**, syncs it into **Elasticsearch**, and visualizes insights using **Kibana dashboards**.

---

## 🏗️ How It Works (Architecture)
1. **Data Source**: Sales/customer/product/event data (JSON or inserted into MongoDB).
2. **MongoDB**: Stores the dataset in database `bi_db`.
3. **Monstache**: Syncs MongoDB collections → Elasticsearch indices (real-time / direct read).
4. **Elasticsearch**: Stores indexed data for fast search + aggregation.
5. **Kibana**: Dashboards for KPIs (Revenue, Orders, Items sold, etc).

---

## 📂 Project Structure
```txt
bi-sales-analytics-elk/
│
├── data/                # JSON files / dataset
├── dashboards/          # Kibana exported dashboards
├── logstash/
│   └── pipeline/        # Logstash pipeline config
├── monstache/           # Monstache config (Mongo → ES sync)
├── scripts/             # Data generation / import scripts
├── docker-compose.yml   # Full stack (Mongo + ES + Kibana + Logstash + Monstache)
└── README.md
▶️ Run the Project

Start services:

docker compose up -d


Check running containers:

docker ps

🌐 Services URLs

Kibana: http://localhost:5602

Elasticsearch: http://localhost:9202

MongoDB: mongodb://localhost:27018

List Elasticsearch indices:

Invoke-RestMethod http://localhost:9202/_cat/indices?v

