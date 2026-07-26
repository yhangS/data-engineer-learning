# Data Engineering Learning

> My hands-on learning journey to become a Data Engineer.

---

# 🎯 Goal

Become a Data Engineer / Data Warehouse Developer with a modern data stack.

This repository records my hands-on learning process from basic environment setup to building an end-to-end data engineering project.

The focus is on:

- Hands-on practice
- Real development workflow
- Data warehouse thinking
- Batch data processing
- Workflow orchestration
- Cloud data platform basics
- Portfolio project preparation

---

# 🧭 Target Role

Target role:

```text
Data Engineer
Data Warehouse Developer
Junior / Mid-level Data Engineer
```

Target technical direction:

```text
Linux
Docker
Git
Spark / PySpark
Airflow
AWS
dbt
Data Warehouse
ETL / ELT
Batch Processing
```

---

# 💻 Environment

| Item | Version |
|------|---------|
| OS | Windows 10 |
| Virtual Machine | VMware Workstation 17 |
| Guest OS | Ubuntu Server 26.04 |
| Hostname | data-lab |
| IDE | VS Code |
| Remote Development | VS Code Remote SSH |
| Version Control | Git / GitHub |
| Programming Language | Python 3 |
| Container Runtime | Docker |
| Spark Runtime | Docker + apache/spark-py |

---

# 📁 Repository Structure

```text
data-engineer-learning/
├── README.md
├── 01-linux/
├── 02-docker/
├── 03-git/
├── 04-spark/
├── 05-airflow/
├── 06-aws/
├── 07-dbt/
└── project/
```

---

# 📚 Learning Roadmap

## Phase 1 - Linux ✅

Goal:

Learn how to work in a Linux server environment.

Completed:

- [x] Ubuntu Server Installation
- [x] SSH Remote Connection
- [x] Basic Linux Commands
- [x] Directory Operations
- [x] File Operations
- [x] File Viewing
- [x] Permissions
- [x] Process Basics
- [x] Disk Usage
- [x] Network Basics

Key takeaway:

```text
Linux is the basic working environment for data engineers.
```

---

## Phase 2 - Docker ✅

Goal:

Learn how to use containers to build reproducible development environments.

Completed:

- [x] Docker Installation
- [x] Registry Mirror
- [x] Image
- [x] Container
- [x] Container Lifecycle
- [x] Volume
- [x] Bind Mount
- [x] Docker Network
- [x] Dockerfile
- [x] Docker Compose

Key takeaway:

```text
Docker helps package and run applications in isolated environments.
```

Most useful commands:

---

## Phase 3 - Git ✅

Goal:

Learn version control and push learning projects to GitHub.

Completed:

- [x] Git Installation
- [x] Git Config
- [x] Git Init
- [x] Git Status
- [x] Git Diff
- [x] Git Add
- [x] Git Commit
- [x] Git Log
- [x] .gitignore
- [x] GitHub Remote Repository
- [x] Git Push

Key takeaway:

```text
Git records code changes.
GitHub is used to store and showcase projects.
```

Basic workflow:

```text
Working Directory
    ↓ git add
Staging Area
    ↓ git commit
Local Repository
    ↓ git push
GitHub Repository
```

---

## Phase 4 - Spark ✅

Goal:

Learn how to use Spark / PySpark for batch data processing and ETL.

Completed:

- [x] Spark 是什么
- [x] Spark vs MapReduce
- [x] Spark Architecture
- [x] PySpark Environment
- [x] First PySpark Script
- [x] DataFrame
- [x] DataFrame API vs Spark SQL
- [x] Transformations and Actions
- [x] Lazy Evaluation
- [x] explain()
- [x] DataFrame Common APIs
- [x] Join
- [x] Aggregation
- [x] Window Function
- [x] Read / Write Files
- [x] Parquet
- [x] Partition
- [x] Shuffle
- [x] Cache / Persist
- [x] Performance Optimization
- [x] Mini ETL Project

Key takeaway:

```text
Spark is a distributed computing engine for large-scale data processing.
PySpark can be used to build batch ETL pipelines.
```

Spark first-round understanding:

```text
Read Data
    ↓
DataFrame Transformations
    ↓
Filter / Select / Join / GroupBy / Window
    ↓
Action
    ↓
Spark Execution Plan
    ↓
Shuffle / Partition / Cache
    ↓
Write Parquet / Partitioned Data
```

---

## Phase 5 - Airflow ⏭️ Next

Goal:

Learn how to schedule and manage data pipelines.

Planned topics:

- [ ] Airflow 是什么
- [ ] DAG
- [ ] Task
- [ ] Operator
- [ ] BashOperator
- [ ] PythonOperator
- [ ] Task Dependency
- [ ] Scheduling
- [ ] Retry
- [ ] Logs
- [ ] Backfill
- [ ] Run Spark ETL with Airflow

Why Airflow matters:

```text
Spark handles data processing.
Airflow handles task scheduling.
```

Airflow target workflow:

```text
DAG
    ↓
Task 1: prepare input data
    ↓
Task 2: run Spark ETL
    ↓
Task 3: validate output
    ↓
Task 4: finish pipeline
```

Key takeaway:

```text
Data engineering jobs should be scheduled, monitored, and retryable.
```

---

## Phase 6 - AWS

Goal:

Understand basic cloud data engineering services.

Planned topics:

- [ ] IAM
- [ ] S3
- [ ] Glue
- [ ] Glue Data Catalog
- [ ] Athena
- [ ] EC2
- [ ] Redshift Basics

Learning focus:

```text
S3      → data lake storage
IAM     → permission management
Glue    → ETL / metadata catalog
Athena  → query data in S3 using SQL
EC2     → cloud server
Redshift → cloud data warehouse
```

Target understanding:

```text
Raw Data
    ↓
S3
    ↓
Glue Catalog
    ↓
Athena SQL
    ↓
Analytics
```

Key takeaway:

```text
Modern data platforms usually store data in cloud object storage and query it with cloud data tools.
```

---

## Phase 7 - dbt

Goal:

Learn SQL-based data modeling and modern analytics engineering workflow.

Planned topics:

- [ ] dbt 是什么
- [ ] Project Structure
- [ ] Model
- [ ] source()
- [ ] ref()
- [ ] Materialization
- [ ] Test
- [ ] Documentation
- [ ] Incremental Model
- [ ] Snapshot

Why dbt matters:

```text
dbt makes SQL projects more structured, testable, and maintainable.
```

dbt target workflow:

```text
Source Data
    ↓
Staging Model
    ↓
Intermediate Model
    ↓
Mart Model
    ↓
Analytics Table
```

Key takeaway:

```text
dbt is useful for organizing SQL transformation logic in a modern data warehouse.
```

---

## Phase 8 - End-to-End Project

Goal:

Build a complete data engineering portfolio project.

Project idea:

```text
Insurance / Car Insurance Data Pipeline
```

Why this project:

```text
It matches my previous data warehouse experience in the insurance industry.
It connects my business background with modern data engineering tools.
```

Target pipeline:

```text
Raw CSV
    ↓
Spark ETL
    ↓
Cleaned Data
    ↓
Partitioned Parquet
    ↓
Airflow Scheduling
    ↓
AWS S3 / Local Simulation
    ↓
Athena / SQL Query
    ↓
dbt Modeling
    ↓
ADS / Analytics Tables
    ↓
README Documentation
```

Possible data layers:

```text
ODS
    ↓
DWD
    ↓
DWS
    ↓
ADS
```

Example tables:

```text
ods_policy_orders
dwd_policy_orders_cleaned
dws_city_policy_daily
ads_policy_dashboard
```

Project goals:

- [ ] Build a local data pipeline
- [ ] Process raw CSV with Spark
- [ ] Write partitioned Parquet files
- [ ] Schedule ETL with Airflow
- [ ] Simulate cloud storage or use AWS S3
- [ ] Query output data
- [ ] Build dbt models
- [ ] Write complete project documentation
- [ ] Push project to GitHub

Key takeaway:

```text
The final project should demonstrate real data engineering workflow, not only isolated technical exercises.
```

---

# 🧱 Overall Learning Path

```text
Basic Environment
Linux
Docker
Git
    ↓
Big Data Processing
Spark / PySpark
    ↓
Workflow Orchestration
Airflow
    ↓
Cloud Data Platform
AWS
    ↓
SQL Modeling
dbt
    ↓
Portfolio Project
End-to-End Data Engineering Pipeline
```

---

# ✅ Current Progress

Completed:

```text
Linux   ✅
Docker  ✅
Git     ✅
Spark   ✅
```

Next:

```text
Airflow ⏭️
```

Later:

```text
AWS
dbt
End-to-End Project
```

---

# 🧠 Learning Principles

## 1. Practice First

Do not only read concepts.

For each topic:

```text
Concept
    ↓
Command / Code
    ↓
Small Lab
    ↓
README Notes
```

## 2. Learn the Main Road First

Do not get stuck in too many details at the beginning.

First round goal:

```text
Understand the whole workflow.
```

Second round goal:

```text
Deepen important topics.
```

## 3. Connect New Tools with Data Warehouse Experience

Use existing data warehouse knowledge:

```text
ODS
DWD
DWS
ADS
Dimension Table
Fact Table
ETL
Hive SQL
```

Connect it with modern tools:

```text
Spark
Airflow
AWS
dbt
```

## 4. Build for Portfolio

Every phase should eventually support the final portfolio project.

The final goal is not just learning tools, but being able to explain:

```text
What problem this pipeline solves
How data flows through the system
Why each tool is used
How to run the project
How to troubleshoot common problems
```

---

# 🏁 Final Target

After completing this roadmap, I should be able to:

- Use Linux for server-side development
- Use Docker to run data engineering tools
- Use Git and GitHub to manage code
- Use Spark / PySpark to process data
- Use Spark SQL for transformation logic
- Write partitioned Parquet data
- Understand Shuffle and basic Spark optimization
- Use Airflow to schedule ETL jobs
- Understand basic AWS data services
- Use dbt to organize SQL models
- Build and explain an end-to-end data engineering project

Final goal:

```text
Become ready for Data Engineer / Data Warehouse Developer interviews.
```