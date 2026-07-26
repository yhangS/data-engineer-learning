from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("aggregation-basic")
        .getOrCreate()
    )

    data = [
        ("Beijing", "A", 10),
        ("Beijing", "A", 30),
        ("Beijing", "B", 20),
        ("Shanghai", "A", 40),
        ("Shanghai", "B", 50),
        ("Guangzhou", "A", 15)
    ]

    columns = ["city", "category", "amount"]

    df: DataFrame = spark.createDataFrame(data, columns)

    print("1. Original Data")
    df.show()

    print("2. Aggregation by city")
    city_result:DataFrame = df.groupBy(F.col("city")).agg(F.sum(F.col("amount")).alias("total_amount")) 

    city_result.show()

    print("3. Aggregation by city and category")
    city_category_result: DataFrame = df.groupBy("city", "category").agg(
        F.sum("amount").alias("total_amount"),
        F.count("*").alias("order_count"),
        F.avg("amount").alias("avg_amount")
    )

    city_category_result.show()

    spark.stop()


if __name__ == "__main__":
    main()