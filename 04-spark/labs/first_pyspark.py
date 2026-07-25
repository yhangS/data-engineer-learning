from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder \
        .appName("dataframe-basic") \
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

    print("1. Original Data")
    df.show()

    print("2. Schema")
    df.printSchema()

    print("3. Select Columns")
    df.select("city", "amount").show()

    print("4. Filter amount > 20")
    df.filter(df.amount > 20).show()

    print("5. Group By city")
    df.groupBy("city").sum("amount").show()

    spark.stop()


if __name__ == "__main__":
    main()