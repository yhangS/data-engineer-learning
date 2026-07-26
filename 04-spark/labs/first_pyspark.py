from pyspark.sql import SparkSession, DataFrame


def main():
    spark = (
        SparkSession.builder
        .appName("partition-basic")
        .getOrCreate()
    )

    input_path = "/data/input/sales.csv"
    output_path = "/data/output/sales_partitioned"

    print("1. Read CSV")
    df: DataFrame = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    df.show()
    df.printSchema()

    print("2. Write Parquet partitioned by city")
    (
        df.write
        .mode("overwrite")
        .partitionBy("city")
        .parquet(output_path)
    )

    print("3. Read partitioned Parquet")
    result: DataFrame = spark.read.parquet(output_path)

    result.show()
    result.printSchema()

    spark.stop()


if __name__ == "__main__":
    main()