from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("performance-basic")
        .getOrCreate()
    )

    data = [
        ("2026-07-26", "Beijing", "order_001", 10),
        ("2026-07-26", "Beijing", "order_002", 30),
        ("2026-07-26", "Shanghai", "order_003", 20),
        ("2026-07-25", "Guangzhou", "order_004", 15),
        ("2026-07-25", "Shanghai", "order_005", 25)
    ]

    columns = ["dt", "city", "order_id", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Filter early and select needed columns")
    filtered_df: DataFrame = (
        df.filter(F.col("dt") == "2026-07-26")
          .select("city", "amount")
    )

    filtered_df.show()

    print("3. Aggregation after filtering")
    result: DataFrame = filtered_df.groupBy("city").agg(
        F.sum("amount").alias("total_amount")
    )

    result.explain(True)
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()