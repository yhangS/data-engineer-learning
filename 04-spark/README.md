# Spark

## 学习进度

- [x] Spark 是什么
- [x] Spark vs MapReduce
- [x] Spark 架构
- [x] PySpark 环境
- [x] 第一个 PySpark 脚本
- [x] DataFrame 基础
- [x] DataFrame API vs Spark SQL
- [x] Transformations 和 Actions
- [x] Lazy Evaluation 和 explain()
- [x] DataFrame 常用 API
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

---

# 1. Spark 是什么

## 概念

Spark 是一个分布式计算引擎，用来处理大规模数据。

它可以把大数据拆成多个分区，然后交给多个任务并行处理。

## 关系

```text
Large Data
    ↓
Spark
    ↓
Distributed Processing
    ↓
Result
```

## 重点

- Spark 不是数据库
- Spark 是计算引擎
- Spark 适合做大数据 ETL、批处理、分析计算
- Spark 可以处理 CSV、JSON、Parquet 等文件
- Spark 常用于数据仓库、数据湖、大数据平台

---

# 2. Spark vs MapReduce

## 概念

MapReduce 是比较早期的大数据计算框架，Spark 是更现代的大数据计算引擎。

MapReduce 通常每一步都依赖磁盘读写，Spark 可以更多利用内存计算，所以在很多场景下 Spark 更快。

## 对比

```text
MapReduce:
Map → Disk → Reduce → Disk

Spark:
DAG → Memory / Shuffle → Result
```

## 重点

- MapReduce 比较传统
- Spark 更适合复杂 ETL 和迭代计算
- Hive SQL 的底层执行引擎可以是 MapReduce、Tez，也可以是 Spark
- Spark 不等于 Hive，但 Spark 可以执行类似 Hive SQL 的数据处理逻辑

---

# 3. Spark Architecture

## 概念

Spark 的核心角色：

- Driver：负责任务调度
- Executor：负责执行任务
- Cluster Manager：负责资源分配
- Partition：数据分区
- Task：处理一个 Partition 的任务

## 关系

```text
Driver
  │
  ▼
Cluster Manager
  │
  ▼
Executor
  │
  ▼
Task
```

## 重点

- Driver 负责安排任务
- Executor 负责真正计算
- Partition 是数据被切分后的单位
- Task 是执行计算的单位
- 一个 Partition 通常对应一个 Task
- Spark 通过多个 Task 并行处理数据

---

# 4. PySpark 环境

## 概念

PySpark 是 Spark 的 Python API。

我们当前使用 Docker 运行 Spark，不直接在本机安装复杂 Spark 环境。

当前环境：

```text
Windows 10
    ↓
VMware Ubuntu Server
    ↓
Docker
    ↓
apache/spark-py 镜像
    ↓
PySpark / spark-submit
```

## PySpark Shell

```bash
sudo docker run -it --rm apache/spark-py:latest /opt/spark/bin/pyspark
```

## 运行 PySpark 脚本

```bash
sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

## 挂载 data 目录运行脚本

```bash
sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
-v /home/kevin/data-engineer-learning/04-spark/data:/data \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

## 重点

- Docker 容器提供 Spark 运行环境
- VS Code 负责写代码
- `.venv` 主要用于 VS Code 代码提示
- 真正运行 Spark 代码时使用 Docker
- 容器里的 `/app` 对应宿主机的 `04-spark/labs`
- 容器里的 `/data` 对应宿主机的 `04-spark/data`

---

# 5. 第一个 PySpark 脚本

## 概念

Spark 程序一般从 `SparkSession` 开始。

`SparkSession` 是 PySpark 程序的入口。

## 示例

```python
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("first-pyspark-job")
        .getOrCreate()
    )

    data = [
        ("Beijing", 10),
        ("Shanghai", 20),
        ("Beijing", 30)
    ]

    columns = ["city", "amount"]

    df = spark.createDataFrame(data, columns)

    df.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## 重点

- `SparkSession.builder` 创建 Spark 程序入口
- `createDataFrame()` 创建 DataFrame
- `show()` 触发执行并展示结果
- `spark.stop()` 关闭 SparkSession

---

# 6. DataFrame 基础

## 概念

DataFrame 可以理解为 Spark 里的分布式表。

它有字段名、字段类型和多行数据。

## 常用方法

```python
df.show()
df.printSchema()
df.select("city", "amount")
df.filter(F.col("amount") > 20)
df.groupBy("city")
```

## 示例

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("dataframe-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", 10),
        ("Shanghai", 20),
        ("Beijing", 30)
    ]

    columns = ["city", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    df.show()
    df.printSchema()

    result: DataFrame = df.filter(F.col("amount") > 20)

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## 重点

- DataFrame 像表
- 但它是分布式的
- Spark 会把 DataFrame 拆成多个 Partition 并行处理
- `show()` 是 Action，会触发执行

---

# 7. df. 和 F. 的区别

## 概念

```text
df.  → 操作整张表
F.   → 构造字段计算逻辑
```

## 示例

```python
from pyspark.sql import functions as F

df.filter(F.col("amount") > 20)
```

拆开理解：

```text
df.filter(...)        对整张表过滤
F.col("amount") > 20  定义字段判断条件
```

## 常见写法

```python
df.withColumn("amount_x10", F.col("amount") * 10)

df.groupBy("city").agg(
    F.sum("amount").alias("total_amount")
)

df.orderBy(F.col("amount").desc())
```

## 重点

> df 管表，F 管列。

---

# 8. DataFrame API vs Spark SQL

## 概念

Spark 有两种常见写法：

```text
DataFrame API
Spark SQL
```

它们底层都会变成 Spark 执行计划。

## DataFrame API

```python
result = df.groupBy("city").agg(
    F.sum("amount").alias("total_amount")
)
```

## Spark SQL

```python
df.createOrReplaceTempView("sales")

result = spark.sql("""
    SELECT
        city,
        SUM(amount) AS total_amount
    FROM sales
    GROUP BY city
""")
```

## 重点

- DataFrame API 更适合工程代码
- Spark SQL 更接近 Hive SQL
- 两种写法底层都会被 Spark 优化和执行
- 有 Hive SQL 基础时，学习 Spark SQL 会更自然

---

# 9. Transformations 和 Actions

## 概念

Spark 操作分为两类：

```text
Transformations：转换，不会立刻执行
Actions：动作，会触发执行
```

## Transformations

```python
df.select("city")
df.filter(F.col("amount") > 20)
df.withColumn("amount_x10", F.col("amount") * 10)
df.groupBy("city")
df.join(other_df, on="city", how="left")
```

## Actions

```python
df.show()
df.count()
df.collect()
df.take(10)
df.write.parquet("/path")
```

## 重点

- Transformation 只是构建执行计划
- Action 才会真正触发 Spark 任务
- 这就是 Spark 的 Lazy Evaluation

---

# 10. Lazy Evaluation 和 explain()

## 概念

Lazy Evaluation 表示 Spark 不会马上执行每一步代码。

Spark 会先记录执行计划，等遇到 Action 再统一优化和执行。

## 示例

```python
result = (
    df.filter(F.col("amount") > 20)
      .groupBy("city")
      .agg(F.sum("amount").alias("total_amount"))
)

result.explain(True)
result.show()
```

## explain()

`explain(True)` 可以查看 Spark 的执行计划。

常见内容：

```text
Parsed Logical Plan
Analyzed Logical Plan
Optimized Logical Plan
Physical Plan
```

## 重点

- Spark 会先生成逻辑计划
- 再优化成物理计划
- 最后真正执行
- `explain(True)` 可以帮助理解 Spark 到底怎么执行

---

# 11. DataFrame 常用 API

## withColumn

新增列或修改列。

```python
df.withColumn("amount_x10", F.col("amount") * 10)
```

## when / otherwise

类似 SQL 里的 `CASE WHEN`。

```python
df.withColumn(
    "amount_level",
    F.when(F.col("amount") >= 30, "high")
     .otherwise("normal")
)
```

## orderBy / limit

排序和取前几条。

```python
df.orderBy(F.col("amount").desc()).limit(10)
```

## drop

删除字段。

```python
df.drop("amount_level")
```

## dropDuplicates

去重。

```python
df.dropDuplicates(["city"])
```

## unionByName

按字段名合并两个 DataFrame。

```python
df1.unionByName(df2)
```

## 重点

- 常用 API 不需要一次性背完
- 重点是能看懂真实项目代码
- 多数 DataFrame API 都和 SQL 有对应关系

---

# 12. Join

## 概念

Join 用来把两张 DataFrame 按字段关联起来。

类似 Hive SQL：

```sql
SELECT *
FROM sales s
LEFT JOIN city_dim c
ON s.city = c.city;
```

## PySpark 写法

```python
result = sales_df.join(
    city_df,
    on="city",
    how="left"
)
```

## 常见 Join 类型

```text
inner：只保留两边都匹配的数据
left：保留左表全部数据
```

## 处理字段冲突

如果两张表有同名字段，推荐使用 `alias()` 和 `select()` 明确选择字段。

```python
sales = sales_df.alias("s")
city = city_df.alias("c")

result = (
    sales.join(city, on=F.col("s.city") == F.col("c.city"), how="left")
         .select(
             F.col("s.city").alias("city"),
             F.col("s.amount").alias("amount"),
             F.col("c.region").alias("region")
         )
)
```

## Join 后 null

左连接后右表字段为 null，通常说明：

- 维表缺数据
- 关联字段不一致
- 源数据脏
- 维表同步延迟

## 重点

- 数仓中事实表 join 维表非常常见
- Join 可能触发 Shuffle
- 小维表 Join 大事实表时，后面可以考虑 broadcast join

---

# 13. Aggregation

## 概念

Aggregation 是分组聚合。

对应 Hive SQL：

```sql
SELECT
    city,
    SUM(amount) AS total_amount,
    COUNT(*) AS order_count
FROM sales
GROUP BY city;
```

## PySpark 写法

```python
result = df.groupBy("city").agg(
    F.sum("amount").alias("total_amount"),
    F.count("*").alias("order_count"),
    F.avg("amount").alias("avg_amount")
)
```

## 多字段分组

```python
result = df.groupBy("city", "category").agg(
    F.sum("amount").alias("total_amount"),
    F.count("*").alias("order_count")
)
```

## 重点

```text
groupBy()    按字段分组
agg()        对每组计算指标
```

> Aggregation 是数仓开发最核心的操作之一。

---

# 14. Window Function

## 概念

Window Function 用来做组内排序、组内排名、组内取最新一条等操作。

区别：

```text
groupBy：多行变一行
Window：保留明细行，同时增加排名 / 统计字段
```

## Hive SQL

```sql
ROW_NUMBER() OVER (
    PARTITION BY city
    ORDER BY amount DESC
) AS rn
```

## PySpark

```python
from pyspark.sql.window import Window

window_spec = Window.partitionBy("city").orderBy(
    F.col("amount").desc()
)

result = df.withColumn(
    "rn",
    F.row_number().over(window_spec)
)
```

## 取每组第一条

```python
top1_result = result.filter(F.col("rn") == 1)
```

## 重点

- Window Function 常用于组内排序
- 常用于去重
- 常用于取最新记录
- 常用于每组取 Top 1 / Top N

---

# 15. Read / Write Files

## 概念

Spark 可以直接读写文件。

常见格式：

```text
CSV
JSON
Parquet
```

## 读取 CSV

```python
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/data/input/sales.csv")
)
```

## 写出 CSV

```python
(
    df.write
    .mode("overwrite")
    .option("header", True)
    .csv("/data/output/sales_result")
)
```

## 创建测试 CSV

```bash
mkdir -p ~/data-engineer-learning/04-spark/data/input
mkdir -p ~/data-engineer-learning/04-spark/data/output

cat > ~/data-engineer-learning/04-spark/data/input/sales.csv << 'EOF'
city,order_id,amount
Beijing,order_001,10
Beijing,order_002,30
Shanghai,order_003,20
Guangzhou,order_004,15
EOF
```

## Docker 执行命令

```bash
sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
-v /home/kevin/data-engineer-learning/04-spark/data:/data \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

## 查看输出

```bash
ls -R ~/data-engineer-learning/04-spark/data/output
```

```bash
cat ~/data-engineer-learning/04-spark/data/output/sales_result/part-*.csv
```

## 重点

- Spark 写文件通常写出的是目录
- 目录里会有 `part-*` 文件
- `_SUCCESS` 表示任务成功
- 写文件时要注意 Docker 挂载目录权限

---

# 16. Parquet

## 概念

Parquet 是列式存储文件格式，适合大数据分析和数仓场景。

## CSV vs Parquet

```text
CSV：文本格式，适合简单查看和交换数据
Parquet：列式存储，适合 Spark / Hive / 数据湖分析
```

## 写 Parquet

```python
df.write.mode("overwrite").parquet("/data/output/sales_parquet")
```

## 读 Parquet

```python
parquet_df = spark.read.parquet("/data/output/sales_parquet")
```

## 示例

```python
result.write.mode("overwrite").parquet("/data/output/sales_parquet")

parquet_df = spark.read.parquet("/data/output/sales_parquet")

parquet_df.show()
parquet_df.printSchema()
```

## 重点

- Parquet 自带 schema
- Parquet 通常比 CSV 更适合大数据分析
- Parquet 是列式存储
- Parquet 文件不能直接用 `cat` 查看
- 真实 Spark 数仓项目里，Parquet 比 CSV 更常用

---

# 17. Partition

## 概念

Partition 在 Spark 里有两个常见含义：

```text
1. Spark 内部并行计算的数据分区
2. 文件写出时按字段分目录存储
```

本阶段重点掌握第二种：文件分区。

## 示例

```python
(
    df.write
    .mode("overwrite")
    .partitionBy("city")
    .parquet("/data/output/sales_partitioned")
)
```

输出目录类似：

```text
sales_partitioned/
├── city=Beijing/
├── city=Shanghai/
└── city=Guangzhou/
```

## Hive 对应

```sql
PARTITIONED BY (dt string)
```

## 按日期分区

真实数仓里更常见的是按日期分区：

```python
(
    df.write
    .mode("overwrite")
    .partitionBy("dt")
    .parquet("/data/output/sales_partitioned")
)
```

## 重点

- 分区可以减少查询扫描范围
- 真实数仓中最常见的是按日期分区
- 例如 `dt=2026-07-26`
- 分区字段会体现在目录名里
- Spark 读取整个分区目录时，会自动识别分区字段

---

# 18. Shuffle

## 概念

Shuffle 是 Spark 在不同分区之间重新分发数据的过程。

比如：

```python
df.groupBy("city")
```

Spark 需要把相同 `city` 的数据放到一起，这个过程通常会触发 Shuffle。

## 常见触发 Shuffle 的操作

```text
groupBy
join
orderBy
distinct
dropDuplicates
```

## explain 中的关键字

```text
Exchange
```

如果执行计划里看到 `Exchange`，通常说明发生了 Shuffle。

## 示例

```python
group_result = df.groupBy("city").agg(
    F.sum("amount").alias("total_amount")
)

group_result.explain(True)
group_result.show()
```

## 重点

- Shuffle 会带来网络传输
- Shuffle 会带来磁盘读写
- Shuffle 会带来内存压力
- Shuffle 是 Spark 性能优化里的核心概念

---

# 19. Cache / Persist

## 概念

`cache()` 用来缓存会被重复使用的中间结果。

如果一个 DataFrame 后面会被多个 Action 使用，可以考虑缓存。

## 示例

```python
result = df.groupBy("city").agg(
    F.sum("amount").alias("total_amount")
)

result.cache()

result.show()
result.count()

result.unpersist()
```

## 重点

- `cache()` 不会立刻执行
- 第一次 Action 时才会真正缓存
- 只用一次的数据不要乱 cache
- 用完可以 `unpersist()` 释放缓存
- cache 不等于永久保存，程序结束后缓存就没有了

---

# 20. Performance Optimization

## 概念

Spark 性能优化的核心不是一上来调参数，而是先看数据流是否合理。

## 核心思路

```text
少读数据
少 Shuffle
少重复计算
```

## 常见方向

### 1. 提前过滤

```python
df.filter(F.col("dt") == "2026-07-26")
```

### 2. 只选择需要字段

```python
df.select("city", "amount")
```

### 3. 减少 Shuffle

避免不必要的：

```text
groupBy
join
orderBy
distinct
```

### 4. 合理 cache

```python
result.cache()
```

### 5. 小表广播 Join

```python
from pyspark.sql.functions import broadcast

result = fact_df.join(
    broadcast(dim_df),
    on="city",
    how="left"
)
```

## 重点

> Spark 优化核心：少读数据、少 Shuffle、少重复计算。

---

# 21. Mini ETL Project

## 项目目标

模拟一个最小 Spark ETL：

```text
Read CSV
    ↓
Clean / Filter
    ↓
Aggregation
    ↓
Write Parquet
    ↓
Partition
```

## 准备输入数据

```bash
cat > ~/data-engineer-learning/04-spark/data/input/orders.csv << 'EOF'
dt,city,order_id,amount,status
2026-07-25,Beijing,order_001,10,success
2026-07-25,Beijing,order_002,30,success
2026-07-25,Shanghai,order_003,20,failed
2026-07-26,Shanghai,order_004,40,success
2026-07-26,Guangzhou,order_005,15,success
2026-07-26,Beijing,order_006,25,success
EOF
```

## ETL 代码

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("mini-etl-project")
        .getOrCreate()
    )

    input_path = "/data/input/orders.csv"
    output_path = "/data/output/dws_city_sales_daily"

    print("1. Read source CSV")
    ods_orders: DataFrame = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    ods_orders.show()
    ods_orders.printSchema()

    print("2. Clean data: keep success orders only")
    dwd_orders: DataFrame = (
        ods_orders
        .filter(F.col("status") == "success")
        .select(
            "dt",
            "city",
            "order_id",
            "amount"
        )
    )

    dwd_orders.show()

    print("3. Aggregate: daily sales by city")
    dws_city_sales_daily: DataFrame = (
        dwd_orders
        .groupBy("dt", "city")
        .agg(
            F.sum("amount").alias("total_amount"),
            F.count("*").alias("order_count")
        )
    )

    dws_city_sales_daily.show()

    print("4. Write result as partitioned Parquet")
    (
        dws_city_sales_daily.write
        .mode("overwrite")
        .partitionBy("dt")
        .parquet(output_path)
    )

    print("5. Read result back")
    result: DataFrame = spark.read.parquet(output_path)

    result.show()
    result.printSchema()

    spark.stop()


if __name__ == "__main__":
    main()
```

## 执行命令

```bash
sudo rm -rf ~/data-engineer-learning/04-spark/data/output/dws_city_sales_daily

sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
-v /home/kevin/data-engineer-learning/04-spark/data:/data \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

## 查看输出

```bash
ls -R ~/data-engineer-learning/04-spark/data/output/dws_city_sales_daily
```

输出类似：

```text
dws_city_sales_daily/
├── _SUCCESS
├── dt=2026-07-25/
│   └── part-xxxxx.snappy.parquet
└── dt=2026-07-26/
    └── part-xxxxx.snappy.parquet
```

## 数仓分层对应

```text
ods_orders
    ↓
ODS：原始订单数据

dwd_orders
    ↓
DWD：清洗后的订单明细

dws_city_sales_daily
    ↓
DWS：按日期、城市汇总的销售指标
```

## 重点

> 一个最小 Spark ETL 就是：读数据 → 清洗过滤 → 聚合指标 → 写 Parquet → 按日期分区。

---

# 22. 常用命令

## 进入 PySpark Shell

```bash
sudo docker run -it --rm apache/spark-py:latest /opt/spark/bin/pyspark
```

## 运行 PySpark 脚本

```bash
sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
-v /home/kevin/data-engineer-learning/04-spark/data:/data \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

## 查看输出目录

```bash
ls -R ~/data-engineer-learning/04-spark/data/output
```

## 查看 CSV 输出

```bash
cat ~/data-engineer-learning/04-spark/data/output/sales_result/part-*.csv
```

## 删除输出目录

```bash
sudo rm -rf ~/data-engineer-learning/04-spark/data/output/sales_result
```

## 解决写文件权限问题

```bash
sudo chmod -R 777 ~/data-engineer-learning/04-spark/data
```

---

# 23. Spark 第一轮总结

## 已掌握内容

- Spark 是分布式计算引擎
- DataFrame 是 Spark 里的分布式表
- `df.` 用来操作表
- `F.` 用来构造列计算表达式
- Transformation 不会立刻执行
- Action 会触发执行
- `explain(True)` 可以查看执行计划
- Join 用来关联事实表和维表
- Aggregation 用来做分组聚合
- Window Function 用来做组内排序和取数
- Spark 可以读写 CSV、Parquet
- Spark 写文件通常写出目录
- Parquet 适合数仓和大数据分析
- Partition 可以按字段分目录存储
- Shuffle 是性能优化核心
- Cache 适合缓存重复使用的中间结果
- Spark 优化核心是少读数据、少 Shuffle、少重复计算

## 当前阶段目标

第一轮 Spark 学习目标不是精通所有 API，而是：

```text
看到 PySpark 代码不陌生
能写简单 ETL
知道 Spark 核心执行逻辑
能理解数仓里 Spark 的作用
```

## 下一阶段

下一阶段进入 Airflow：

```text
05-airflow
    ↓
DAG
Task
Operator
任务依赖
调度周期
失败重跑
调度 Spark ETL
```