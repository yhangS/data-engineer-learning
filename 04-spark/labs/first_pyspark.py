from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("drop-duplicates-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "order_001", 10),
        ("Shanghai", "order_002", 20),
        ("Beijing", "order_001", 10),
        ("Beijing", "order_003", 30),
        ("Shanghai", "order_004", 25),
        ("Guangzhou", "order_005", 15)
    ]

    columns = ["city", "order_id", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Drop duplicate rows")
    result1: DataFrame = df.dropDuplicates()

    result1.show()

    print("3. Drop duplicates by city")
    result2: DataFrame = df.dropDuplicates(["city"])

    result2.show()

    spark.stop()


if __name__ == "__main__":
    main()