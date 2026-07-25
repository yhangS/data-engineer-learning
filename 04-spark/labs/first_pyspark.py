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

    result:DataFrame = (
        df.filter(df.amount>20)
    .select("city","amount")
    .groupBy("city")
    .sum("amount")
    )


    print("1. Explain execution plan")
    result.explain(True)


    print("2. Action: show result")
    result.show()
    


    spark.stop()


if __name__ == "__main__":
    main()