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
- [x] DataFrame 常用 API
- [x] Join 基础
- [x] Join 字段冲突
- [x] Join 后 null 处理
- [ ] Aggregation
- [ ] Window Function
- [ ] Read / Write Files
- [ ] Parquet
- [ ] Partition
- [ ] Shuffle
- [ ] Cache / Persist
- [ ] Performance Optimization
- [ ] Mini ETL Project

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

    df.show()
    df.printSchema()
    df.select("city", "amount").show()
    df.filter(df.amount > 20).show()
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

    df.createOrReplaceTempView("sales")

    print("DataFrame API: filter amount > 20")
    df.filter(df.amount > 20).show()

    print("Spark SQL: filter amount > 20")
    spark.sql("""
        SELECT city, category, amount
        FROM sales
        WHERE amount > 20
    """).show()

    print("DataFrame API: group by city")
    df.groupBy("city").sum("amount").show()

    print("Spark SQL: group by city")
    spark.sql("""
        SELECT city, SUM(amount) AS total_amount
        FROM sales
        GROUP BY city
    """).show()

    spark.stop()


if __name__ == "__main__":
    main()
```

## 对应关系

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

    result: DataFrame = (
        df.filter(df.amount > 20)
          .select("city", "amount")
          .groupBy("city")
          .sum("amount")
    )

    print("No result has been printed yet")

    result.show()

    row_count = result.count()
    print(f"Row count: {row_count}")

    spark.stop()


if __name__ == "__main__":
    main()
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
result.explain(True)
```

运行后会看到：

```text
Parsed Logical Plan
Analyzed Logical Plan
Optimized Logical Plan
Physical Plan
```

| 名称 | 含义 |
|------|------|
| Logical Plan | 逻辑计划：想做什么 |
| Optimized Logical Plan | 优化后的逻辑计划 |
| Physical Plan | 物理计划：Spark 实际怎么执行 |

## Lab

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

    result.explain(True)
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

---

# 10. DataFrame 常用 API

## 10.1 withColumn()

### 概念

`withColumn()` 用来新增列或修改已有列。

```python
df.withColumn("column_name", expression)
```

### Lab

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
        ("Beijing", "B", 30)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    result: DataFrame = df.withColumn(
        "amount_x10",
        F.col("amount") * 10
    )

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

---

## 10.2 when()

### 概念

`F.when(...).otherwise(...)` 对应 SQL 里的：

```sql
CASE WHEN ... THEN ... ELSE ... END
```

### Lab

```python
result: DataFrame = df.withColumn(
    "amount_level",
    F.when(F.col("amount") >= 30, "high")
     .when(F.col("amount") >= 20, "middle")
     .otherwise("low")
)

result.show()
```

---

## 10.3 orderBy() 和 limit()

### 概念

- `orderBy()` 用来排序
- `limit()` 用来限制行数

### Lab

```python
result: DataFrame = (
    df.orderBy(F.col("amount").desc())
      .limit(3)
)

result.show()
```

---

## 10.4 drop()

### 概念

`drop()` 用来删除不需要的字段。

### Lab

```python
result: DataFrame = df.drop("city_name")

result.show()
```

---

## 10.5 dropDuplicates()

### 概念

`dropDuplicates()` 用来去重。

```python
df.dropDuplicates()
df.dropDuplicates(["city"])
```

注意：

- 整行去重比较安全
- 按部分字段去重时，Spark 不保证保留哪一条

### Lab

```python
result1: DataFrame = df.dropDuplicates()

result2: DataFrame = df.dropDuplicates(["city"])

result1.show()
result2.show()
```

---

## 10.6 union()

### 概念

`union()` 用来上下合并两个 DataFrame，类似 SQL 的 `UNION ALL`。

注意：

- `union()` 按字段位置合并
- 不会自动去重

### Lab

```python
result: DataFrame = df_2025.union(df_2026)

result.show()
```

---

## 10.7 unionByName()

### 概念

`unionByName()` 按字段名合并，比 `union()` 更安全。

### Lab

```python
result: DataFrame = df_2025.unionByName(df_2026)

result.show()
```

字段缺失时：

```python
result: DataFrame = df_2025.unionByName(
    df_2026,
    allowMissingColumns=True
)

result.show()
```

---

## 10.8 cast()

### 概念

`cast()` 用来转换字段类型。

对应 SQL：

```sql
CAST(amount AS INT)
```

PySpark：

```python
F.col("amount").cast("int")
```

### Lab

```python
result: DataFrame = df.withColumn(
    "amount_int",
    F.col("amount").cast("int")
)

result.show()
result.printSchema()
```

---

# 11. Join 基础

## 概念

Join 用来把两张表按某个字段关联起来。

常见 Join 类型：

| Join 类型 | 含义 |
|----------|------|
| `inner` | 只保留两边都匹配的数据 |
| `left` | 保留左表全部数据，右表匹配不到则为 null |
| `right` | 保留右表全部数据，左表匹配不到则为 null |
| `full` | 保留两边所有数据，匹配不到则为 null |

## Lab

```python
from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("join-basic")
        .getOrCreate()
    )

    sales_data = [
        ("Beijing", 10),
        ("Shanghai", 20),
        ("Beijing", 30),
        ("Guangzhou", 15),
        ("Shenzhen", 25)
    ]

    sales_columns = ["city", "amount"]

    sales_df: DataFrame = spark.createDataFrame(
        sales_data,
        sales_columns
    )

    city_data = [
        ("Beijing", "North"),
        ("Shanghai", "East"),
        ("Guangzhou", "South")
    ]

    city_columns = ["city", "region"]

    city_df: DataFrame = spark.createDataFrame(
        city_data,
        city_columns
    )

    inner_result: DataFrame = sales_df.join(
        city_df,
        on="city",
        how="inner"
    )

    left_result: DataFrame = sales_df.join(
        city_df,
        on="city",
        how="left"
    )

    inner_result.show()
    left_result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

---

# 12. Join 字段冲突

## 概念

真实开发里，两张表经常有相同字段名。

例如：

```text
sales_df: city, name, amount
city_df:  city, name, region
```

Join 后两边都有 `name`，容易冲突。

推荐做法：

```text
1. 给表起别名 alias()
2. 明确选择字段 select()
3. 给冲突字段重命名 alias()
```

## Lab

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("join-column-conflict")
        .getOrCreate()
    )

    sales_data = [
        ("Beijing", "order_001", 10),
        ("Shanghai", "order_002", 20),
        ("Beijing", "order_003", 30),
        ("Guangzhou", "order_004", 15),
        ("Shenzhen", "order_005", 25)
    ]

    sales_columns = ["city", "name", "amount"]

    sales_df: DataFrame = spark.createDataFrame(
        sales_data,
        sales_columns
    )

    city_data = [
        ("Beijing", "Beijing CN", "North"),
        ("Shanghai", "Shanghai CN", "East"),
        ("Guangzhou", "Guangzhou CN", "South")
    ]

    city_columns = ["city", "name", "region"]

    city_df: DataFrame = spark.createDataFrame(
        city_data,
        city_columns
    )

    sales = sales_df.alias("s")
    city = city_df.alias("c")

    result: DataFrame = (
        sales.join(
            city,
            on=F.col("s.city") == F.col("c.city"),
            how="left"
        )
        .select(
            F.col("s.city").alias("city"),
            F.col("s.name").alias("order_name"),
            F.col("s.amount").alias("amount"),
            F.col("c.name").alias("city_name"),
            F.col("c.region").alias("region")
        )
    )

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

---

# 13. Join 后 null 处理

## 概念

`left join` 后，如果右表匹配不到，右表字段会变成 null。

常用方法：

| 方法 | 作用 |
|------|------|
| `fillna()` | 把 null 填成默认值 |
| `isNull()` | 判断字段是否为 null |
| `isNotNull()` | 判断字段是否不为 null |

## Lab

```python
filled_df: DataFrame = joined_df.fillna(
    {
        "city_name": "Unknown City",
        "region": "Unknown Region"
    }
)

unmatched_df: DataFrame = joined_df.filter(
    F.col("region").isNull()
)

filled_df.show()
unmatched_df.show()
```

## 真实开发意义

在数仓里，left join 维表后出现 null，通常说明：

```text
1. 维表缺数据
2. join key 不一致
3. 源数据有脏值
4. 维表更新延迟
```

---

# 14. 当前 Spark Roadmap

后续主线不再继续发散零散 API，改为按 Spark 核心能力推进：

```text
Aggregation
    ↓
Window Function
    ↓
Read / Write Files
    ↓
Parquet
    ↓
Partition
    ↓
Shuffle
    ↓
Cache / Persist
    ↓
Performance Optimization
    ↓
Mini ETL Project
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

withColumn / when / cast 等是常用 DataFrame API

join 是事实表关联维表的核心操作

left join 后的 null 要检查业务含义
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
Aggregation
```