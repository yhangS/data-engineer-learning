from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("union-by-name-missing-columns")
        .getOrCreate()
    )

    data_2025 = [
        ("Beijing", "order_001", 10),
        ("Shanghai", "order_002", 20)
    ]

    columns_2025 = ["city", "order_id", "amount"]

    data_2026 = [
        ("Guangzhou", "order_003", 15, "app"),
        ("Shenzhen", "order_004", 25, "web")
    ]

    columns_2026 = ["city", "order_id", "amount", "channel"]

    df_2025: DataFrame = spark.createDataFrame(data_2025, columns_2025)
    df_2026: DataFrame = spark.createDataFrame(data_2026, columns_2026)

    print("1. Data 2025")
    df_2025.show()

    print("2. Data 2026")
    df_2026.show()

    print("3. Union by name with missing columns")
    result: DataFrame = df_2025.unionByName(
        df_2026,
        allowMissingColumns=True
    )

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()