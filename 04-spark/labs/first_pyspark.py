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

    print("2. Order by amount ascending")
    df.orderBy(
        F.col("amount").asc()
    ).show()

    print("3. Order by amount descending")
    df.orderBy(
        F.col("amount").desc()
    ).show()

    print("4. Top 3 amount")
    result:DataFrame = df.orderBy(
        F.col("amount").desc()
    ).limit(3)

    result.show()

    spark.stop()


if __name__ == "__main__":
    main()