from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("parquet-basic")
        .getOrCreate()
    )

    input_path = "/data/input/sales.csv"
    output_path = "/data/output/sales_parquet"

    print("1. Read CSV")
    df: DataFrame = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    df.show()
    df.printSchema()

    print("2. Aggregation")
    result: DataFrame = df.groupBy("city").agg(
        F.sum("amount").alias("total_amount"),
        F.count("*").alias("order_count")
    )

    result.show()

    print("3. Write result as Parquet")
    (
        result.write
        .mode("overwrite")
        .parquet(output_path)
    )

    print("4. Read Parquet result")
    parquet_df: DataFrame = spark.read.parquet(output_path)

    parquet_df.show()
    parquet_df.printSchema()

    spark.stop()


if __name__ == "__main__":
    main()