from pyspark.sql import SparkSession


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

    df = spark.createDataFrame(data, columns)

    print("1. Create Transformation")
    result:DataFrame = (
        df.filter(df.amount>20)
    .select("city","amount")
    .groupBy("city")
    .sum("amount")
    )


    print("2. No result has been printed yet")


    print("3. Action: show")
    result.show()
    

    print("4. Action: count")
    row_count = result.count()
    print(f"Row count: {row_count}")

    spark.stop()


if __name__ == "__main__":
    main()