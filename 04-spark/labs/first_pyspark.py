from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("read-write-files-basic")
        .getOrCreate()
    )

    input_path = "/data/input/sales.csv"
    output_path = "/data/output/sales_result"

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

    print("3. Write result as CSV")
    (
        result.write
        .mode("overwrite")
        .option("header", True)
        .csv(output_path)
    )

    spark.stop()


if __name__ == "__main__":
    main()