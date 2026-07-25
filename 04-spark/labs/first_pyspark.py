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

    print("1. Original Data")
    df.show()

    print("2. DataFrame API Filter:amount > 20")
    df.filter(df.amount>20).show()

    print("3. SQL Filter:amount > 20")
    df.createOrReplaceTempView("sales")

    spark.sql("""
    select city,category,amount from sales where amount > 20
    """).show()

    print("4. DataFrame API:group by city")
    df.groupBy("city").sum("amount").show()

    print("5. SQL:group by city")
    spark.sql("""
    select city,sum(amount) from sales group by city
    """).show()

    spark.stop()


if __name__ == "__main__":
    main()