from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("union-basic")
        .getOrCreate()
    )

    data_2025 = [
        ("Beijing", "order_001", 10),
        ("Shanghai", "order_002", 20),
        ("Guangzhou", "order_003", 15)
    ]

    data_2026 = [
        ("Beijing", "order_004", 30),
        ("Shanghai", "order_005", 25),
        ("Shenzhen", "order_006", 40)
    ]

    columns = ["city", "order_id", "amount"]

    df_2025: DataFrame = spark.createDataFrame(data_2025, columns)
    df_2026: DataFrame = spark.createDataFrame(data_2026, columns)

    print("1. Data 2025")
    df_2025.show()

    print("2. Data 2026")
    df_2026.show()

    print("3. Union Result")
    result: DataFrame = df_2025.union(df_2026)

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()