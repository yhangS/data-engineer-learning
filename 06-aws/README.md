# AWS Data Engineering Learning

## 学习目标

理解 AWS 在 Data Engineering 中的作用：

```text
数据存储
    ↓
数据处理
    ↓
数据查询
    ↓
数据分析
```

重点掌握：

- IAM
- S3
- Glue Data Catalog
- Athena
- Glue ETL
- Redshift

---

# AWS Data Engineering Architecture

完整数据链路：

```text
              Data Source

                  |
                  v

                 S3
          (Data Lake Storage)

                  |
                  |
             Glue ETL
          (Spark Processing)

                  |
                  v

                 S3
        (Processed Parquet Data)

                  |
                  |
          Glue Data Catalog
             (Metadata)

                  |
          ----------------

          |              |

        Athena       Redshift

        SQL查询       数据仓库

                  |
                  |

             BI Dashboard
```

---

# 1. AWS 是什么

## 概念

AWS（Amazon Web Services）是云计算平台。

对于 Data Engineer：

AWS 提供：

```text
计算资源
存储资源
数据处理服务
数据分析服务
权限管理
```

---

# 2. AWS 和传统数据平台对应关系

传统 Hadoop：

```text
HDFS
 |
 |
Hive Metastore
 |
 |
Hive SQL
```

AWS：

```text
S3
 |
 |
Glue Data Catalog
 |
 |
Athena SQL
```

对应关系：

| Hadoop生态 | AWS |
|-|-|
| HDFS | S3 |
| Hive Metastore | Glue Data Catalog |
| Hive SQL | Athena |
| Spark | Glue ETL |
| 数仓 | Redshift |

---

# 3. IAM（Identity and Access Management）

## 概念

IAM 是 AWS 的权限管理系统。

解决：

```text
谁可以访问什么资源？
谁可以执行什么操作？
```

---

## IAM 核心组成

### User

用户。

例如：

```text
Kevin
DataEngineer
Developer
```

---

### Group

用户组。

例如：

```text
DataEngineer-Team

成员:
Kevin
Alice
Bob
```

统一管理权限。

---

### Role

角色。

非常重要。

真实数据工程中：

Spark / Glue / Airflow

不会保存账号密码。

而是：

```text
Application

      |

 Assume Role

      |

获得 AWS 权限
```

---

### Policy

权限规则。

例如：

允许读取 S3：

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject"
  ],
  "Resource": [
    "arn:aws:s3:::company-data/*"
  ]
}
```

---

## IAM 在数据工程中的作用

例如：

Spark Job：

```text
Spark

 ↓

IAM Role

 ↓

读取 S3 数据
```

---

# 4. S3（Simple Storage Service）

## 概念

S3 是 AWS 最核心的数据存储服务。

可以理解：

```text
S3 = 云上的 Data Lake
```

---

## S3 结构

S3：

```text
Bucket

  |

Object
```

例如：

```text
s3://company-data/orders/2026/orders.parquet
```

拆分：

Bucket：

```text
company-data
```

Object：

```text
orders/2026/orders.parquet
```

---

# 5. S3 和文件系统区别

Linux：

```text
目录
 |
文件
```

例如：

```text
/home/data/orders.csv
```

---

S3：

没有真正目录。

实际上：

```text
orders/2026/orders.csv
```

只是一个 Object Key。

其中：

```text
orders/2026/
```

只是 Prefix。

---

# 6. Data Lake 数据组织

企业常见：

```text
company-data

├── raw
│
├── dwd
│
├── dws
│
└── ads
```

对应数仓：

```text
Raw Layer

    ↓

DWD

    ↓

DWS

    ↓

ADS
```

---

# 7. S3 + Spark

本地：

```python
df = spark.read.csv(
    "file:///data/input/orders.csv"
)
```

AWS：

```python
df = spark.read.parquet(
    "s3://company-data/orders/"
)
```

写入：

```python
df.write.parquet(
    "s3://company-data/dwd/orders/"
)
```

---

# 8. S3 + Partition

数据：

```text
orders/

year=2026/

month=08/

day=05/

part-000.parquet
```

查询：

```sql
WHERE
year=2026
AND month=08
AND day=05
```

只扫描对应分区。

优势：

```text
减少扫描数据

提高查询速度

降低成本
```

---

# 9. Glue Data Catalog

## 概念

Glue Data Catalog：

```text
AWS版 Hive Metastore
```

作用：

管理数据元信息。

---

## 保存什么？

保存：

```text
表名

字段

字段类型

数据位置

Partition信息
```

例如：

Table:

```text
orders
```

Columns:

```text
order_id string

amount double

date date
```

Location:

```text
s3://company-data/orders/
```

---

## 注意

Glue Catalog：

不保存数据。

数据：

```text
S3
```

元数据：

```text
Glue Catalog
```

---

# 10. Athena

## 概念

Athena 是：

```text
Serverless SQL Query Engine
```

作用：

直接使用 SQL 查询 S3 数据。

---

## 架构

```text
S3

 |

Glue Catalog

 |

Athena

 |

SQL Result
```

---

## 示例

S3:

```text
s3://company-data/orders/
```

Glue Catalog:

```text
table:
orders
```

Athena:

```sql
SELECT *
FROM orders;
```

---

# 11. Athena 和 Spark 区别

## Spark

负责：

```text
ETL

清洗

转换

Join

复杂计算
```

例如：

```python
df.groupBy("city")
.sum("amount")
```

---

## Athena

负责：

```text
SQL查询

数据分析

临时探索

BI查询
```

例如：

```sql
SELECT
city,
SUM(amount)
FROM sales
GROUP BY city;
```

---

关系：

```text
Spark

负责生产数据


Athena

负责消费数据
```

---

# 12. Glue ETL

## 概念

AWS Glue ETL：

```text
AWS托管的Spark环境
```

类似：

```text
Spark + AWS管理
```

---

## 本地Spark

```text
docker

↓

spark-submit

↓

PySpark
```

---

## Glue

```text
Glue Job

↓

AWS Spark Environment

↓

执行PySpark

↓

写入S3
```

---

# 13. Glue Job

Glue Job 本质：

一个 ETL 程序。

例如：

```python
df = spark.read.parquet(
    "s3://company/raw/orders/"
)


result = (
    df
    .filter("amount > 0")
)


result.write.parquet(
    "s3://company/dwd/orders/"
)
```

---

# 14. Glue ETL 工作流程

```text
Raw Data

(S3)

↓

Glue Job

(Spark ETL)

↓

Clean Data

(S3 Parquet)

↓

Glue Catalog

↓

Athena
```

---

# 15. Glue Crawler

## 概念

Crawler：

自动发现数据结构。

例如：

扫描：

```text
s3://company/orders/
```

发现：

字段：

```text
id

amount

date
```

自动创建：

```text
Database

Table

Schema
```

---

# 16. Redshift

## 概念

Redshift：

```text
AWS Cloud Data Warehouse
```

云数据仓库。

---

## Data Lake vs Data Warehouse

### Data Lake

代表：

```text
S3
```

特点：

保存：

```text
Raw Data

CSV

JSON

Parquet

Logs
```

---

### Data Warehouse

代表：

```text
Redshift
```

特点：

保存：

```text
结构化数据

业务指标

报表数据
```

---

# 17. Athena vs Redshift

| | Athena | Redshift |
|-|-|-|
| 类型 | SQL查询服务 | 数据仓库 |
| 数据位置 | S3 | Redshift |
| 用途 | 数据探索 | 企业分析 |
| 用户 | Analyst | BI团队 |
| 数据 | Data Lake | Warehouse |

---

# 18. Redshift 和数仓模型

传统：

```text
ODS

 ↓

DWD

 ↓

DWS

 ↓

ADS
```

Redshift：

类似：

```text
Raw

 ↓

Detail

 ↓

Summary

 ↓

Application
```

---

# 19. Airflow + AWS + Spark 完整流程

真实企业：

```text
              Airflow

                 |

                 |

          Trigger Spark Job

                 |

                 v

               Glue ETL

                 |

                 v

                S3

           (Parquet Data)

                 |

                 v

          Glue Data Catalog

                 |

        ----------------

        |              |

     Athena        Redshift

        |              |

        ---------

             |

        BI Dashboard
```

---

# 20. Data Engineer 日常工作

一个典型任务：

每天凌晨：

```text
Airflow启动

↓

检查输入数据

↓

运行Glue/Spark ETL

↓

读取S3 Raw数据

↓

清洗转换

↓

写入S3 Parquet

↓

更新Catalog

↓

Athena查询

↓

刷新BI报表
```

---

# 21. 面试总结

## What is S3?

回答：

```text
Amazon S3 is a cloud object storage service.

It is commonly used as the storage layer of a data lake.
```

---

## What is Glue Data Catalog?

回答：

```text
Glue Data Catalog is a metadata repository.

It stores table schemas, locations and partitions,
similar to Hive Metastore.
```

---

## What is Athena?

回答：

```text
Athena is a serverless SQL query service.

It allows users to analyze data stored in S3 using SQL.
```

---

## What is Glue?

回答：

```text
AWS Glue provides managed Spark environments for ETL processing.

Data engineers can transform data stored in S3
and prepare datasets for analytics.
```

---

## What is Redshift?

回答：

```text
Amazon Redshift is a cloud data warehouse.

It is used for large-scale analytical queries and BI workloads.
```

---

# AWS 第一轮学习完成

## 已掌握

- [x] AWS 数据工程整体架构
- [x] IAM 权限模型
- [x] S3 数据湖存储
- [x] S3 Partition
- [x] Glue Data Catalog
- [x] Athena SQL 查询
- [x] Glue ETL（Spark）
- [x] Redshift 数据仓库
- [x] Airflow + Spark + AWS 数据链路


## 下一阶段

进入：

```text
07-dbt
```

学习：

```text
SQL Transformation

Data Modeling

Analytics Engineering

dbt Project Structure

dbt Model

dbt Test

dbt Documentation
```

最终串成：

```text
Git
 ↓
Docker
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