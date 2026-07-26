from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("shuffle-basic")
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

    print("1. Original Data")
    df.show()

    print("2. Filter only")
    filter_result: DataFrame = df.filter(F.col("amount") > 10)

    filter_result.explain(True)
    filter_result.show()

    print("3. Group by city")
    group_result: DataFrame = df.groupBy("city").agg(
        F.sum("amount").alias("total_amount")
    )

    group_result.explain(True)
    group_result.show()

    spark.stop()


if __name__ == "__main__":
    main()