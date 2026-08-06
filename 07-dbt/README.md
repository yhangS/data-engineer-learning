# dbt Learning

## 学习目标

理解 dbt 在现代数据工程和现代数仓中的作用。

dbt 不是用来替代 Spark / Airflow / AWS 的工具，而是用来解决：

```text
SQL 数据转换如何工程化
数据模型如何组织
模型依赖如何管理
数据质量如何测试
数据文档如何维护
```

一句话：

> dbt = SQL + Git + Testing + Documentation + Lineage

---

# 学习进度

- [x] dbt 是什么
- [x] ETL vs ELT
- [x] dbt 项目结构
- [x] Model
- [x] `ref()`
- [x] `source()`
- [x] Materialization
- [x] dbt Test
- [x] Documentation
- [x] Data Lineage
- [x] dbt + Git + CI/CD
- [x] dbt 综合项目设计
- [x] dbt 在真实 Data Engineer 项目中的位置

---

# 1. dbt 是什么

## 概念

dbt 全称是：

```text
data build tool
```

dbt 是一个数据转换工具。

它让 Data Engineer / Analytics Engineer 可以使用 SQL 在数据仓库中构建数据模型。

dbt 主要解决：

```text
SQL 如何组织
模型之间的依赖如何管理
数据质量如何测试
数据文档如何生成
数据血缘如何追踪
```

---

## dbt 不是什么

dbt 不是数据库。

dbt 不负责存储数据。

dbt 不负责大规模原始数据处理。

dbt 不负责调度整个数据管道。

对应关系：

```text
Spark
    负责大规模数据处理

Airflow
    负责任务调度

AWS
    负责云平台和数据存储

dbt
    负责数据仓库中的 SQL 建模
```

---

## dbt 的核心定位

```text
Raw Tables
    ↓
dbt SQL Models
    ↓
Analytics Tables
    ↓
BI / Dashboard
```

一句话：

> dbt 负责把数据仓库中的原始表加工成可供分析使用的业务模型。

---

# 2. ETL vs ELT

## ETL

ETL：

```text
Extract
Transform
Load
```

顺序：

```text
数据源
    ↓
抽取 Extract
    ↓
转换 Transform
    ↓
加载 Load
    ↓
数据仓库
```

传统 Hadoop / Hive 数仓中，经常是 ETL 模式。

例如：

```text
业务数据库
    ↓
ETL 工具 / Spark / MapReduce
    ↓
清洗转换
    ↓
Hive / 数仓表
```

---

## ELT

ELT：

```text
Extract
Load
Transform
```

顺序：

```text
数据源
    ↓
加载到数据湖 / 云数仓
    ↓
再进行转换
```

现代云数仓更常见 ELT。

例如：

```text
Source
    ↓
S3 / Redshift / Snowflake / BigQuery
    ↓
dbt SQL Transform
    ↓
Analytics Tables
```

---

## 为什么云时代喜欢 ELT？

因为现代云数仓计算能力更强，存储和计算可以分离。

传统：

```text
计算资源有限
    ↓
先转换再加载
```

现代：

```text
云存储便宜
计算资源弹性
    ↓
先存原始数据
再按需求转换
```

---

## Spark ETL vs dbt ELT

| 工具 | 主要作用 | 适合场景 |
|---|---|---|
| Spark | 大规模数据处理 | 文件转换、复杂清洗、大数据计算 |
| dbt | SQL 建模 | 指标表、分析表、数据质量、文档 |

---

# 3. dbt 项目结构

一个典型 dbt 项目：

```text
dbt_project/
├── dbt_project.yml
├── models/
│   ├── staging/
│   │   ├── stg_orders.sql
│   │   ├── stg_customers.sql
│   │   └── schema.yml
│   │
│   └── marts/
│       ├── sales_daily.sql
│       ├── customer_summary.sql
│       └── schema.yml
│
├── tests/
├── macros/
├── seeds/
└── README.md
```

---

## dbt_project.yml

`dbt_project.yml` 是 dbt 项目的配置文件。

它告诉 dbt：

```text
项目叫什么
models 在哪里
默认 materialization 是什么
项目配置如何加载
```

示例：

```yaml
name: sales_project

version: '1.0'

profile: sales_project

model-paths:
  - models
```

---

## models/

`models/` 是 dbt 最核心的目录。

一个 SQL 文件就是一个 dbt Model。

例如：

```text
models/staging/stg_orders.sql
```

对应一个模型：

```text
stg_orders
```

---

# 4. Model

## 概念

在 dbt 中：

```text
一个 SQL 文件 = 一个 Model
```

例如：

```text
models/staging/stg_orders.sql
```

内容：

```sql
SELECT
    order_id,
    customer_id,
    amount,
    created_at

FROM raw_orders
```

dbt 执行后会生成：

```text
stg_orders
```

这个模型可以是：

```text
View
Table
Incremental Table
```

具体由 Materialization 决定。

---

# 5. staging 和 marts

## staging 层

staging 负责轻量清洗和标准化。

常见工作：

```text
字段重命名
类型转换
去掉无用字段
基础清洗
统一字段命名
```

示例：

```sql
SELECT
    id AS order_id,
    customer AS customer_id,
    CAST(amount AS DECIMAL) AS amount,
    create_time AS created_at

FROM {{ source('raw', 'orders') }}
```

特点：

```text
不做复杂业务逻辑
不做复杂聚合
尽量一张 raw 表对应一张 staging 表
```

---

## marts 层

marts 是业务分析层。

负责生成业务指标表和报表表。

例如：

```text
sales_daily
customer_summary
product_performance
```

示例：

```sql
SELECT
    DATE(created_at) AS sales_date,
    SUM(amount) AS revenue,
    COUNT(order_id) AS order_count

FROM {{ ref('stg_orders') }}

GROUP BY
    DATE(created_at)
```

---

## 传统数仓和 dbt 分层对比

| 传统数仓 | dbt / 现代数仓 |
|---|---|
| ODS | Raw / Source |
| DWD | staging / intermediate |
| DWS | marts |
| ADS | marts / BI tables |

---

# 6. `ref()`

## 概念

`ref()` 是 dbt 最重要的语法之一。

它用来引用另一个 dbt Model。

例如：

```sql
FROM {{ ref('stg_orders') }}
```

意思：

```text
当前模型依赖 stg_orders
```

dbt 会自动根据 `ref()` 生成模型依赖关系。

---

## 示例

`stg_orders.sql`：

```sql
SELECT
    order_id,
    customer_id,
    amount,
    created_at

FROM {{ source('raw', 'orders') }}
```

`sales_daily.sql`：

```sql
SELECT
    DATE(created_at) AS sales_date,
    SUM(amount) AS revenue

FROM {{ ref('stg_orders') }}

GROUP BY
    DATE(created_at)
```

依赖关系：

```text
stg_orders
    ↓
sales_daily
```

---

## 为什么不用直接写表名？

不推荐：

```sql
FROM stg_orders
```

推荐：

```sql
FROM {{ ref('stg_orders') }}
```

原因：

```text
dbt 可以自动识别依赖
dbt 可以生成 lineage
dbt 可以根据环境生成正确表名
dbt 可以按依赖顺序运行模型
```

---

# 7. `source()`

## 概念

`source()` 用来引用原始数据源表。

例如：

```sql
FROM {{ source('raw', 'orders') }}
```

通常 source 在 YAML 文件中声明。

---

## sources.yml 示例

```yaml
version: 2

sources:
  - name: raw
    tables:
      - name: orders
      - name: customers
      - name: products
```

然后 SQL 中使用：

```sql
SELECT
    order_id,
    customer_id,
    amount,
    created_at

FROM {{ source('raw', 'orders') }}
```

---

## `source()` vs `ref()`

| 语法 | 用途 |
|---|---|
| `source()` | 引用外部原始表 |
| `ref()` | 引用 dbt 内部模型 |

---

# 8. SQL 和 YAML 的分工

## SQL 负责什么？

SQL 负责业务逻辑。

例如：

```text
SELECT
JOIN
WHERE
GROUP BY
CASE WHEN
窗口函数
指标计算
```

复杂关联逻辑应该写在 SQL 中。

---

## YAML 负责什么？

YAML 不负责 JOIN 逻辑。

YAML 主要负责：

```text
声明 source
描述 model
描述 column
配置 tests
配置 documentation
配置部分 model 属性
```

---

## 生产中的常见模式

假设需要生成销售报表，关联订单、用户、商品。

目录：

```text
models/
├── staging/
│   ├── stg_orders.sql
│   ├── stg_users.sql
│   └── stg_products.sql
│
└── marts/
    └── sales_report.sql
```

`sales_report.sql`：

```sql
SELECT
    o.order_id,
    u.user_name,
    p.product_name,
    o.amount

FROM {{ ref('stg_orders') }} o

LEFT JOIN {{ ref('stg_users') }} u
    ON o.user_id = u.user_id

LEFT JOIN {{ ref('stg_products') }} p
    ON o.product_id = p.product_id
```

YAML 描述这个模型和字段，但不描述 JOIN 过程。

---

## 重点

> dbt 不是用 YAML 替代 SQL，而是用 YAML 给 SQL 增加工程化能力。

---

# 9. dbt compile 和 dbt run

## dbt compile

`dbt compile` 只生成最终 SQL，不执行。

例如：

dbt model：

```sql
SELECT *
FROM {{ ref('stg_orders') }}
```

compile 后变成普通 SQL：

```sql
SELECT *
FROM analytics.stg_orders
```

作用：

```text
解析 Jinja 模板
解析 ref/source
生成目标数据库能识别的 SQL
检查基本语法和依赖
```

---

## dbt run

`dbt run` 会编译并执行模型。

流程：

```text
读取 model SQL
    ↓
解析 ref/source
    ↓
生成最终 SQL
    ↓
提交到目标数据库执行
    ↓
生成 View / Table / Incremental Table
```

---

## 你之前公司中的模式

可能是：

```text
dbt model / YAML
    ↓
dbt compile
    ↓
生成 SQL 文件
    ↓
DolphinScheduler 调度
    ↓
Hive SQL 执行
    ↓
MapReduce 运行
```

这种方式可以理解为：

```text
dbt 主要作为 SQL 模板管理和 SQL 生成工具
```

现代云数仓中更常见：

```text
Airflow
    ↓
dbt run
    ↓
Redshift / Snowflake / BigQuery 执行 SQL
```

---

# 10. Materialization

## 概念

Materialization 决定 dbt Model 最终如何存储到数据库中。

常见类型：

```text
view
table
incremental
```

---

## View

View 不保存数据，只保存 SQL 定义。

```sql
{{ config(
    materialized='view'
) }}

SELECT *
FROM {{ source('raw', 'orders') }}
```

特点：

```text
不占存储
每次查询重新计算
适合简单模型和 staging 层
```

---

## Table

Table 保存 SQL 查询结果。

```sql
{{ config(
    materialized='table'
) }}

SELECT
    customer_id,
    SUM(amount) AS total_amount

FROM {{ ref('stg_orders') }}

GROUP BY customer_id
```

特点：

```text
查询快
结果长期保存
每次 dbt run 重新生成
适合业务分析层
```

---

## Incremental

Incremental 只处理新增或变更数据。

适合大表。

```sql
{{ config(
    materialized='incremental'
) }}

SELECT *
FROM {{ ref('stg_orders') }}

{% if is_incremental() %}

WHERE created_at > (
    SELECT MAX(created_at)
    FROM {{ this }}
)

{% endif %}
```

第一次运行：

```text
全量加载
```

之后运行：

```text
只处理新增数据
```

---

## 对比

| 类型 | 是否保存数据 | 查询速度 | 适合场景 |
|---|---|---|---|
| View | 否 | 较慢 | staging、小模型 |
| Table | 是 | 快 | 中等数据量业务表 |
| Incremental | 是 | 快 | 大表、生产环境 |

---

# 11. dbt Test

## 概念

dbt Test 用来做数据质量检查。

执行命令：

```bash
dbt test
```

dbt 会根据 YAML 中的测试规则生成 SQL 检查数据。

---

## 常见测试

### not_null

字段不能为空。

```yaml
columns:
  - name: order_id
    tests:
      - not_null
```

---

### unique

字段必须唯一。

```yaml
columns:
  - name: order_id
    tests:
      - unique
```

---

### accepted_values

字段值必须在指定范围内。

```yaml
columns:
  - name: status
    tests:
      - accepted_values:
          values:
            - pending
            - completed
            - cancelled
```

---

### relationships

检查外键关系。

```yaml
columns:
  - name: customer_id
    tests:
      - relationships:
          to: ref('stg_customers')
          field: customer_id
```

---

## schema.yml 示例

```yaml
version: 2

models:
  - name: stg_orders
    description: "Cleaned orders staging model"

    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Customer identifier"
        tests:
          - not_null

      - name: amount
        description: "Order amount"
        tests:
          - not_null
```

---

## dbt Test 的本质

dbt Test 本质上也是 SQL。

例如 `not_null` 可以理解为：

```sql
SELECT *
FROM stg_orders
WHERE order_id IS NULL
```

如果返回 0 行，测试通过。

---

# 12. Documentation

## 概念

dbt 可以根据 YAML 中的描述生成数据文档。

常用命令：

```bash
dbt docs generate
dbt docs serve
```

---

## 文档内容

dbt Docs 可以展示：

```text
模型说明
字段说明
字段测试
模型依赖
数据血缘
```

---

## YAML 文档示例

```yaml
version: 2

models:
  - name: sales_daily
    description: "Daily sales summary table"

    columns:
      - name: sales_date
        description: "Date of sales"

      - name: revenue
        description: "Total sales amount"

      - name: order_count
        description: "Number of orders"
```

---

# 13. Data Lineage

## 概念

Data Lineage 表示数据血缘。

也就是：

```text
数据从哪里来
经过哪些转换
最后被哪里使用
```

---

## dbt 如何生成 lineage？

dbt 根据：

```sql
{{ ref('model_name') }}
```

自动识别模型依赖。

例如：

```text
raw_orders
    ↓
stg_orders
    ↓
fct_orders
    ↓
sales_daily
    ↓
Dashboard
```

---

## Airflow DAG vs dbt Lineage

| 对比 | Airflow | dbt |
|---|---|---|
| 对象 | Task | Model |
| 关注点 | 任务执行顺序 | 数据模型依赖 |
| 语言 | Python | SQL + YAML |
| 作用 | 调度 | 建模和血缘 |

---

# 14. dbt + Git + CI/CD

## 为什么 dbt 需要 Git？

dbt 项目主要由：

```text
.sql
.yml
.md
```

组成。

这些都是代码，应该使用 Git 管理。

---

## 企业开发流程

```text
Developer
    ↓
Git Branch
    ↓
修改 SQL / YAML
    ↓
dbt compile
    ↓
dbt run / dbt test
    ↓
Pull Request
    ↓
Code Review
    ↓
Merge
    ↓
Deploy
```

---

## 常见开发命令

```bash
git checkout -b feature/customer-monthly-sales

dbt compile

dbt run

dbt test

git add .

git commit -m "add customer monthly sales model"
```

---

## CI/CD 中的 dbt

CI 阶段常见检查：

```text
dbt compile
dbt test
SQL lint
文档检查
```

生产阶段：

```text
Airflow / Scheduler
    ↓
dbt run
    ↓
dbt test
```

---

# 15. dbt 和 Airflow 的关系

## dbt

负责：

```text
SQL 怎么转换
模型依赖
数据质量
文档
血缘
```

## Airflow

负责：

```text
什么时候运行
任务依赖
失败重试
日志
告警
```

---

## 生产中的组合

```text
Airflow DAG
    ↓
Spark ETL
    ↓
Load Warehouse
    ↓
dbt run
    ↓
dbt test
    ↓
Refresh Dashboard
```

---

# 16. dbt 和 Spark 的关系

## Spark

适合：

```text
大规模原始数据处理
复杂清洗
文件格式转换
半结构化数据处理
写 Parquet
```

## dbt

适合：

```text
数据仓库中的 SQL 模型
指标表
维度表 / 事实表
数据质量测试
数据文档
```

---

## 典型链路

```text
Raw Data
    ↓
Spark / Glue ETL
    ↓
Clean Data / Warehouse
    ↓
dbt Models
    ↓
Analytics Tables
    ↓
BI Dashboard
```

---

# 17. dbt 和 AWS 的关系

典型 AWS 现代数仓链路：

```text
Source
    ↓
S3 Raw
    ↓
Glue / Spark ETL
    ↓
Redshift
    ↓
dbt
    ↓
Analytics Tables
    ↓
BI Dashboard
```

也可以是：

```text
S3 + Athena
    ↓
dbt Athena Adapter
    ↓
SQL Models
```

但更常见的现代云数仓组合是：

```text
Redshift / Snowflake / BigQuery
    ↓
dbt
```

---

# 18. dbt 综合项目设计

## 项目背景

模拟电商数据平台。

数据源：

```text
customers
products
orders
```

业务需求：

```text
每日销售额
用户消费汇总
商品销售分析
```

---

## 项目结构

```text
data-engineering-project/
├── spark/
│   └── orders_etl.py
│
├── airflow/
│   └── daily_pipeline.py
│
├── dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/
│       │   ├── stg_orders.sql
│       │   ├── stg_customers.sql
│       │   ├── stg_products.sql
│       │   └── schema.yml
│       │
│       └── marts/
│           ├── sales_daily.sql
│           ├── customer_summary.sql
│           └── schema.yml
│
└── README.md
```

---

## staging models

### stg_orders.sql

```sql
SELECT
    order_id,
    customer_id,
    product_id,
    amount,
    created_at

FROM {{ source('raw', 'orders') }}
```

---

### stg_customers.sql

```sql
SELECT
    customer_id,
    customer_name,
    country,
    created_at

FROM {{ source('raw', 'customers') }}
```

---

### stg_products.sql

```sql
SELECT
    product_id,
    product_name,
    category,
    price

FROM {{ source('raw', 'products') }}
```

---

## marts models

### sales_daily.sql

```sql
{{ config(
    materialized='table'
) }}

SELECT
    DATE(created_at) AS sales_date,
    SUM(amount) AS revenue,
    COUNT(order_id) AS order_count

FROM {{ ref('stg_orders') }}

GROUP BY
    DATE(created_at)
```

---

### customer_summary.sql

```sql
{{ config(
    materialized='table'
) }}

SELECT
    customer_id,
    COUNT(order_id) AS order_count,
    SUM(amount) AS total_amount

FROM {{ ref('stg_orders') }}

GROUP BY
    customer_id
```

---

## schema.yml 示例

```yaml
version: 2

models:
  - name: sales_daily
    description: "Daily sales summary table"

    columns:
      - name: sales_date
        description: "Date of sales"
        tests:
          - not_null

      - name: revenue
        description: "Total sales amount"
        tests:
          - not_null

      - name: order_count
        description: "Number of orders"
        tests:
          - not_null
```

---

# 19. 常用命令

## 编译 SQL

```bash
dbt compile
```

---

## 运行模型

```bash
dbt run
```

---

## 运行测试

```bash
dbt test
```

---

## 生成文档

```bash
dbt docs generate
```

---

## 启动文档服务

```bash
dbt docs serve
```

---

## 只运行某个模型

```bash
dbt run --select sales_daily
```

---

## 运行某个模型及其上游依赖

```bash
dbt run --select +sales_daily
```

---

## 运行某个模型及其下游依赖

```bash
dbt run --select sales_daily+
```

---

# 20. 面试表达

## What is dbt?

```text
dbt is a data transformation framework.

It allows data engineers and analytics engineers to build,
test and document data models using SQL in the data warehouse.
```

---

## What is dbt materialization?

```text
Materialization defines how dbt models are created and stored in the database.

Common types include views, tables and incremental models.
```

---

## What is dbt test?

```text
dbt tests are used to validate data quality rules,
such as not null, uniqueness and relationships.
```

---

## What is data lineage?

```text
Data lineage shows where data comes from,
how it is transformed,
and where it is used.
```

---

## How do SQL and YAML work in dbt?

```text
SQL defines the transformation logic.

YAML describes sources, models, columns, tests and documentation.
```

---

# 21. dbt 第一轮总结

## 已掌握内容

```text
dbt 是 SQL 数据转换工程化工具
SQL 负责业务转换逻辑
YAML 负责描述、测试和文档
ref() 用来管理模型依赖
source() 用来声明和引用原始表
Materialization 决定模型如何存储
dbt test 用来保障数据质量
dbt docs 用来生成数据文档
dbt lineage 用来追踪模型依赖
dbt 项目应该使用 Git 管理
生产环境通常由 Airflow 调度 dbt run / dbt test
```

---

## dbt 在整体 Data Engineering Roadmap 中的位置

```text
Linux
    ↓
Docker
    ↓
Git
    ↓
Spark
    ↓
Airflow
    ↓
AWS
    ↓
dbt
    ↓
Mini Data Engineering Project
```

---

## 下一阶段

进入：

```text
08-mini-project
```

目标：

把前面所有内容串起来：

```text
CSV / Raw Data
    ↓
Spark ETL
    ↓
Parquet / Clean Data
    ↓
Airflow DAG
    ↓
dbt Models
    ↓
Analytics Tables
    ↓
README Documentation
```