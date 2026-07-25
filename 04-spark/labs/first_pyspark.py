from pyspark.sql import SparkSession,DataFrame
from pyspark.sql import functions as F


def main():
    spark = SparkSession.builder \
        .appName("join-column-conflict") \
        .getOrCreate()

    sales_data = [
        ("Beijing", "order_001", 10),
        ("Shanghai", "order_002", 20),
        ("Beijing", "order_003", 30),
        ("Guangzhou", "order_004", 15),
        ("Shenzhen", "order_005", 25)
    ]

    sales_columns = ["city", "name", "amount"]

    sales_df: DataFrame = spark.createDataFrame(
        sales_data,
        sales_columns
    )

    city_data = [
        ("Beijing", "Beijing CN", "North"),
        ("Shanghai", "Shanghai CN", "East"),
        ("Guangzhou", "Guangzhou CN", "South")
    ]

    city_columns = ["city", "name", "region"]

    city_df: DataFrame = spark.createDataFrame(
        city_data,
        city_columns
    )

    print("1. Sales Data")
    sales_df.show()

    print("2. City Dimension Data")
    city_df.show()

    sales = sales_df.alias("s")
    city = city_df.alias("c")

    print("3. Left Join with aliases")
    result :DataFrame = (
        sales.join(
            city,
            on=F.col("s.city") == F.col("c.city"),
            how="left"
        )
        .select(
            F.col("s.city").alias("city"),
            F.col("s.name").alias("order_name"),
            F.col("s.amount").alias("amount"),
            F.col("c.region").alias("region"),
            F.col("c.name").alias("city_name"),
        )
    )
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()