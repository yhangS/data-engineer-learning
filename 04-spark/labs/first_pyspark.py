from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = SparkSession.builder \
        .appName("dataframe-api-vs-sql") \
        .getOrCreate()

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
    df_with_new_column:DataFrame = df.withColumn(
        "amount_x10",
        F.col("amount")*10
        )

    df_with_new_column.show()

    print("3. Modify existing column: amount")
    df_modified:DataFrame = df.withColumn(
        "amount",
        F.col("amount")+100
    )

    df_modified.show()

    spark.stop()


if __name__ == "__main__":
    main()