from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("union-by-name-basic")
        .getOrCreate()
    )

    data_2025 = [
        ("Beijing", "order_001", 10),
        ("Shanghai", "order_002", 20)
    ]

    columns_2025 = ["city", "order_id", "amount"]

    data_2026 = [
        ("order_003", 15, "Guangzhou"),
        ("order_004", 25, "Shenzhen")
    ]

    columns_2026 = ["order_id", "amount", "city"]

    df_2025: DataFrame = spark.createDataFrame(data_2025, columns_2025)
    df_2026: DataFrame = spark.createDataFrame(data_2026, columns_2026)

    print("1. Data 2025")
    df_2025.show()

    print("2. Data 2026")
    df_2026.show()

    print("3. union result")
    union_result: DataFrame = df_2025.union(df_2026)
    union_result.show()

    print("4. unionByName result")
    union_by_name_result: DataFrame = df_2025.unionByName(df_2026)
    union_by_name_result.show()

    spark.stop()


if __name__ == "__main__":
    main()