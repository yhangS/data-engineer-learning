# Spark

## 学习进度

- [x] Spark 是什么
- [x] Spark vs MapReduce
- [x] Spark 架构
- [x] PySpark Shell
- [x] 第一个 PySpark 脚本
- [x] DataFrame 基础
- [x] DataFrame API vs Spark SQL
- [x] Transformations 和 Actions
- [x] Lazy Evaluation 和 explain()
- [x] withColumn()
- [x] when()
- [x] orderBy() 和 limit()
- [ ] Join
- [ ] Partition
- [ ] Parquet
- [ ] Performance Optimization

---

# 1. Spark 是什么

## 概念

- Spark 是分布式计算引擎
- 用于处理大规模数据
- 通过并行计算提高处理速度
- Spark 可以处理批处理、SQL、流式计算、机器学习等场景

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

## Lab

本节主要理解概念，没有单独代码实验。

---

# 2. Spark vs MapReduce

## 概念

- MapReduce 是老一代分布式计算框架
- Spark 是新一代分布式计算引擎
- MapReduce 每个阶段大量依赖磁盘读写
- Spark 支持内存计算，通常更快、更灵活

## 对比

```text
MapReduce:
Map → Disk → Reduce → Disk

Spark:
DAG → Memory / Shuffle → Result
```

## Lab

本节主要理解 Spark 为什么比 MapReduce 更适合现代数据处理，没有单独代码实验。

---

# 3. Spark 架构

## 概念

- Driver：运行主程序，生成执行计划，调度任务
- Executor：真正执行 Task，处理数据
- Cluster Manager：负责资源分配
- Partition：数据分块
- Task：处理一个 Partition 的任务

## 关系

```text
PySpark Program
      ↓
Driver
      ↓
Cluster Manager
      ↓
Executor
      ↓
Task
```

## Lab

本节主要理解 Spark 程序运行时的角色关系，没有单独代码实验。

---

# 4. PySpark Shell

## 概念

- PySpark 是 Spark 的 Python API
- PySpark Shell 用于快速验证 Spark 环境
- SparkSession 是 PySpark 程序入口

## Lab

进入 PySpark Shell：

```bash
sudo docker run -it --rm apache/spark-py:latest /opt/spark/bin/pyspark
```

在 PySpark Shell 中执行：

```python
data = [("Beijing", 10), ("Shanghai", 20), ("Beijing", 30)]

df = spark.createDataFrame(data, ["city", "amount"])

df.show()
```

预期结果：

```text
+--------+------+
|    city|amount|
+--------+------+
| Beijing|    10|
|Shanghai|    20|
| Beijing|    30|
+--------+------+
```

---

# 5. 第一个 PySpark 脚本

## 概念

- 真实开发中，不会一直在 PySpark Shell 里写代码
- 推荐用 VS Code 写 `.py` 脚本
- 用 `spark-submit` 提交执行

## Lab

文件：

```text
04-spark/labs/first_pyspark.py
```

代码：

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
        ("Beijing", 30),
        ("Guangzhou", 15),
        ("Shanghai", 25)
    ]

    columns = ["city", "amount"]

    df = spark.createDataFrame(data, columns)

    print("Original Data:")
    df.show()

    result = df.groupBy("city").sum("amount")

    print("Aggregated Result:")
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

执行：

```bash
sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

---

# 6. DataFrame 基础

## 概念

- DataFrame 是 Spark 中最常用的数据结构
- 可以理解为分布式表
- 有列名、数据类型和多行数据
- 类似 Hive 表，也类似 Pandas DataFrame
- 但 Spark DataFrame 是分布式的

## 常用操作

| 操作 | 作用 |
|------|------|
| `show()` | 查看数据 |
| `printSchema()` | 查看字段结构 |
| `select()` | 选择列 |
| `filter()` | 过滤数据 |
| `groupBy()` | 分组 |

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("dataframe-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Schema")
    df.printSchema()

    print("3. Select Columns")
    df.select("city", "amount").show()

    print("4. Filter amount > 20")
    df.filter(df.amount > 20).show()

    print("5. Group By city")
    df.groupBy("city").sum("amount").show()

    spark.stop()


if __name__ == "__main__":
    main()
```

---

# 7. DataFrame API vs Spark SQL

## 概念

Spark 有两种常用写法：

```text
DataFrame API
Spark SQL
```

它们表达方式不同，但底层都会交给 Spark 引擎执行。

## 临时视图

```python
df.createOrReplaceTempView("sales")
```

这会把 DataFrame 注册成一个临时视图，之后可以用 SQL 查询。

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("dataframe-api-vs-sql")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. DataFrame API: filter amount > 20")
    df.filter(df.amount > 20).show()

    print("3. SQL: filter amount > 20")
    df.createOrReplaceTempView("sales")

    spark.sql("""
        SELECT city, category, amount
        FROM sales
        WHERE amount > 20
    """).show()

    print("4. DataFrame API: group by city")
    df.groupBy("city").sum("amount").show()

    print("5. SQL: group by city")
    spark.sql("""
        SELECT city, SUM(amount) AS total_amount
        FROM sales
        GROUP BY city
    """).show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## SQL 对应关系

| SQL | DataFrame API |
|-----|---------------|
| `SELECT col1, col2` | `df.select("col1", "col2")` |
| `WHERE amount > 20` | `df.filter(df.amount > 20)` |
| `GROUP BY city` | `df.groupBy("city")` |
| `SUM(amount)` | `.sum("amount")` |
| `ORDER BY amount` | `df.orderBy("amount")` |
| `LIMIT 10` | `df.limit(10)` |

---

# 8. Transformations 和 Actions

## 概念

Spark 操作分为两类：

```text
Transformations
Actions
```

- Transformation：只描述计算步骤，不立刻执行
- Action：真正触发 Spark 执行

## 常见 Transformations

| 操作 | 作用 |
|------|------|
| `select()` | 选择列 |
| `filter()` | 过滤 |
| `withColumn()` | 新增或修改列 |
| `groupBy()` | 分组 |
| `join()` | 关联 |
| `orderBy()` | 排序 |

## 常见 Actions

| 操作 | 作用 |
|------|------|
| `show()` | 显示数据 |
| `count()` | 统计行数 |
| `collect()` | 拉取数据到 Driver |
| `take()` | 取前几行 |
| `write` | 写出数据 |

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("transformations-and-actions")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Create Transformation")

    result: DataFrame = (
        df.filter(df.amount > 20)
          .select("city", "amount")
          .groupBy("city")
          .sum("amount")
    )

    print("2. No result has been printed yet")

    print("3. Action: show")
    result.show()

    print("4. Action: count")
    row_count = result.count()
    print(f"Row count: {row_count}")

    spark.stop()


if __name__ == "__main__":
    main()
```

## 说明

```text
filter / select / groupBy / sum 是 Transformation
show / count 是 Action
```

## 推荐写法

链式调用推荐使用括号：

```python
result = (
    df.filter(df.amount > 20)
      .select("city", "amount")
      .groupBy("city")
      .sum("amount")
)
```

不要写成：

```python
result = df.filter(df.amount > 20)
           .select("city", "amount")
```

这种写法会报错。

---

# 9. Lazy Evaluation 和 explain()

## 概念

Lazy Evaluation 中文叫惰性执行。

- Spark 遇到 Transformation 不马上计算
- Spark 会先记录执行计划
- 遇到 Action 时才真正执行
- 这样 Spark 可以优化整个执行流程

## explain()

`explain()` 用来查看 Spark 执行计划。

```python
result.explain()
```

更详细：

```python
result.explain(True)
```

## 执行计划

运行 `result.explain(True)` 后，会看到：

```text
Parsed Logical Plan
Analyzed Logical Plan
Optimized Logical Plan
Physical Plan
```

简单理解：

| 名称 | 含义 |
|------|------|
| Logical Plan | 逻辑计划：想做什么 |
| Optimized Logical Plan | 优化后的逻辑计划 |
| Physical Plan | 物理计划：Spark 实际怎么执行 |

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("lazy-evaluation-and-explain")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    result: DataFrame = (
        df.filter(df.amount > 20)
          .select("city", "amount")
          .groupBy("city")
          .sum("amount")
    )

    print("1. Explain execution plan")
    result.explain(True)

    print("2. Action: show result")
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

---

# 10. withColumn()

## 概念

`withColumn()` 用来：

```text
新增列
修改已有列
```

基本格式：

```python
df.withColumn("column_name", expression)
```

真实开发中推荐导入：

```python
from pyspark.sql import functions as F
```

引用字段推荐写：

```python
F.col("amount")
```

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("with-column-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Add new column: amount_x10")
    df_with_new_column: DataFrame = df.withColumn(
        "amount_x10",
        F.col("amount") * 10
    )

    df_with_new_column.show()

    print("3. Modify existing column: amount")
    df_modified: DataFrame = df.withColumn(
        "amount",
        F.col("amount") + 100
    )

    df_modified.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## SQL 对应关系

PySpark：

```python
df.withColumn("amount_x10", F.col("amount") * 10)
```

对应 SQL：

```sql
SELECT
    city,
    category,
    amount,
    amount * 10 AS amount_x10
FROM sales;
```

PySpark：

```python
df.withColumn("amount", F.col("amount") + 100)
```

对应 SQL：

```sql
SELECT
    city,
    category,
    amount + 100 AS amount
FROM sales;
```

---

# 11. when()

## 概念

`F.when(...).otherwise(...)` 对应 Hive SQL 里的：

```sql
CASE WHEN ... THEN ... ELSE ... END
```

常用于：

```text
字段打标
条件转换
分类字段生成
```

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("when-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Add amount_level column")
    result: DataFrame = df.withColumn(
        "amount_level",
        F.when(F.col("amount") >= 20, "high")
         .otherwise("low")
    )

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## 多条件写法

```python
result = df.withColumn(
    "amount_level",
    F.when(F.col("amount") >= 30, "high")
     .when(F.col("amount") >= 20, "middle")
     .otherwise("low")
)
```

对应 SQL：

```sql
CASE
    WHEN amount >= 30 THEN 'high'
    WHEN amount >= 20 THEN 'middle'
    ELSE 'low'
END AS amount_level
```

## 注意

条件顺序很重要，Spark 会从上往下判断。

---

# 12. orderBy() 和 limit()

## 概念

`orderBy()` 用来排序。

`limit()` 用来限制行数。

常用于：

```text
Top N 分析
查看金额最高的记录
排序后的明细检查
```

## Lab

代码：

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("order-by-and-limit")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Shanghai", "A", 20),
        ("Beijing", "B", 30),
        ("Guangzhou", "B", 15),
        ("Shanghai", "B", 25)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Order by amount ascending")
    df.orderBy(F.col("amount").asc()).show()

    print("3. Order by amount descending")
    df.orderBy(F.col("amount").desc()).show()

    print("4. Top 3 amount")
    result: DataFrame = (
        df.orderBy(F.col("amount").desc())
          .limit(3)
    )

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## SQL 对应关系

PySpark：

```python
df.orderBy(F.col("amount").desc()).limit(3)
```

对应 SQL：

```sql
SELECT
    city,
    category,
    amount
FROM sales
ORDER BY amount DESC
LIMIT 3;
```

## 注意

`orderBy()` 通常比较重，因为排序可能需要跨分区移动数据。

```text
轻操作：select / filter
重操作：groupBy / join / orderBy
```

---

# 常用运行命令

## 运行 PySpark 脚本

```bash
sudo docker run -it --rm \
-v /home/kevin/data-engineer-learning/04-spark/labs:/app \
apache/spark-py:latest \
/opt/spark/bin/spark-submit /app/first_pyspark.py
```

## 进入 PySpark Shell

```bash
sudo docker run -it --rm apache/spark-py:latest /opt/spark/bin/pyspark
```

## 激活 Python 虚拟环境

```bash
source .venv/bin/activate
```

## 退出 Python 虚拟环境

```bash
deactivate
```

## 查看 PySpark 版本

```bash
python -c "import pyspark; print(pyspark.__version__)"
```

---

# 总结

## 当前重点

```text
DataFrame 是 Spark 中的分布式表

Spark SQL 和 DataFrame API 本质上表达同一个逻辑

Transformation 不立刻执行

Action 才触发执行

Lazy Evaluation 让 Spark 可以优化执行计划

withColumn 用于新增或修改字段

when 用于 CASE WHEN 条件判断

orderBy + limit 用于排序和 Top N
```

## 推荐导入

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
```

## 推荐链式调用写法

```python
result = (
    df.filter(F.col("amount") > 20)
      .select("city", "amount")
      .groupBy("city")
      .sum("amount")
)
```

## 下一节

```text
Join
```