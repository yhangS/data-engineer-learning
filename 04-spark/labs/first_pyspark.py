from pyspark.sql import SparkSession


def main():
    # 1. Create SparkSession
    spark = SparkSession.builder \
        .appName("first-pyspark-job") \
        .getOrCreate()

    # 2. Create sample data
    data = [
        ("Beijing", 10),
        ("Shanghai", 20),
        ("Beijing", 30),
        ("Guangzhou", 15),
        ("Shanghai", 25)
    ]

    columns = ["city", "amount"]

    # 3. Create DataFrame
    df = spark.createDataFrame(data, columns)

    print("Original Data:")
    df.show()

    # 4. Group by city
    result = df.groupBy("city").sum("amount")

    print("Aggregated Result:")
    result.show()

    # 5. Stop SparkSession
    spark.stop()


if __name__ == "__main__":
    main()