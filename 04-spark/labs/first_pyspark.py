from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("mini-etl-project")
        .getOrCreate()
    )

    input_path = "/data/input/orders.csv"
    output_path = "/data/output/dws_city_sales_daily"

    print("1. Read source CSV")
    ods_orders:DataFrame = (
            spark.read
            .option("header",True)
            .option("inferSchema",True)
            .csv(input_path)
        )

    ods_orders.show()
    ods_orders.printSchema()

    print("2. Clean data: keep success orders only")
    dwd_orders = ods_orders.filter(F.col("status")=="success") \
        .select([F.col("dt"),F.col("city"),F.col("order_id"),F.col("amount"),F.col("status")])  

    dwd_orders.show()

    print("3. Aggregate: daily sales by city")
    dws_city_sales_daily = dwd_orders.groupBy(F.col("dt"),F.col("city")).agg(
        F.sum(F.col("amount")).alias("total_amount"),
        F.count("*").alias("order_count")
    )

    dws_city_sales_daily.show()

    print("4. Write result as partitioned Parquet")
    dws_city_sales_daily.write.mode("overwrite").partitionBy("dt").parquet(output_path)

    print("5. Read result back")
    result:DataFrame = spark.read.parquet(output_path)
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()