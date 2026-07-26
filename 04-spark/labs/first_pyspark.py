from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def main():
    spark = (
        SparkSession.builder
        .appName("window-function-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "order_001", 10),
        ("Beijing", "order_002", 30),
        ("Beijing", "order_003", 20),
        ("Shanghai", "order_004", 40),
        ("Shanghai", "order_005", 25),
        ("Guangzhou", "order_006", 15)
    ]

    columns = ["city", "order_id", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    window_spec = Window.partitionBy("city").orderBy(
        F.col("amount").desc()
    )

    print("2. Add row_number by city")
    result: DataFrame = df.withColumn(
        "rn",
        F.row_number().over(window_spec)
    )

    result.show()

    print("3. Top 1 order in each city")
    top1_result: DataFrame = result.filter(
        F.col("rn") == 1
    )

    top1_result.show()

    spark.stop()


if __name__ == "__main__":
    main()