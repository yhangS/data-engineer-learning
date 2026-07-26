from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("cache-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "order_001", 10),
        ("Beijing", "order_002", 30),
        ("Shanghai", "order_003", 20),
        ("Guangzhou", "order_004", 15),
        ("Shanghai", "order_005", 25)
    ]

    columns = ["city", "order_id", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    result: DataFrame = df.groupBy("city").agg(
        F.sum("amount").alias("total_amount"),
        F.count("*").alias("order_count")
    )

    print("1. Cache result")
    result.cache()

    print("2. First action: show")
    result.show()

    print("3. Second action: count")
    row_count = result.count()
    print(f"Row count: {row_count}")

    print("4. Release cache")
    result.unpersist()

    spark.stop()


if __name__ == "__main__":
    main()