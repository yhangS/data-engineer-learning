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

    print("2. Add amount_level column")
    result:DataFrame = df.withColumn(
        "amount_level",
        F.when(F.col("amount")>=20,"high")
        .otherwise("low")
    )

    result.show()
    
    spark.stop()


if __name__ == "__main__":
    main()