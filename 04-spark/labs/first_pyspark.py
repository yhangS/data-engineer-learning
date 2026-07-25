from pyspark.sql import SparkSession,DataFrame
from pyspark.sql import functions as F


def main():
    spark = SparkSession.builder \
        .appName("join-basic") \
        .getOrCreate()

    sales_data = [
        ("Beijing", 10),
        ("Shanghai", 20),
        ("Beijing", 30),
        ("Guangzhou", 15),
        ("Shenzhen", 25)
    ]

    sales_columns = ["city", "amount"]

    sales_df: DataFrame = spark.createDataFrame(sales_data, sales_columns)

    city_data = [
        ("Beijing", "North"),
        ("Shanghai", "East"),
        ("Guangzhou", "South")
    ]

    city_columns = ["city", "region"]

    city_df:DataFrame = spark.createDataFrame(city_data,city_columns)


    print("1. Sales Data")
    sales_df.show()

    print("2. City Dimension Data")
    city_df.show()

    print("3. Inner Join")
    inner_result:DataFrame = sales_df.join(city_df,on="city",how="inner")
    inner_result.show()

    print("4. Left Join")
    left_result:DataFrame = sales_df.join(city_df,on="city",how="left")
    left_result.show()

    print("5. Full Join")
    full_result:DataFrame = sales_df.join(city_df,on="city",how="full")
    full_result.show()
    
    spark.stop()


if __name__ == "__main__":
    main()