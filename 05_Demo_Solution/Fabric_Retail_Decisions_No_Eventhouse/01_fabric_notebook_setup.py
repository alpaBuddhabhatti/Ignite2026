# Paste into a Microsoft Fabric Python notebook attached to your Lakehouse.
# FIRST upload the six base CSV files into Lakehouse > Files > ignite_data.
# The notebook uses Spark to register them as Delta tables.
from pyspark.sql import functions as F
from pyspark.sql.types import *

files = {
  "dim_store": ["StoreId", "StoreName", "Region"],
  "dim_product": ["ProductId", "Category", "ProductName"],
  "fact_daily_sales": ["SalesDate", "StoreId", "ProductId", "Units", "UnitPrice", "Revenue", "PromotionActive"],
  "fact_inventory": ["SnapshotDate", "StoreId", "ProductId", "OnHand", "IsLowStock"],
  "fact_promotion": ["Month", "StoreId", "Category", "PromotionActive", "CampaignSpend"],
  "fact_store_operations": ["OperationDate", "StoreId", "PlannedOpenMinutes", "ActualOpenMinutes", "StaffScheduled", "StaffPresent", "POSOutageMinutes"],
}
for name in files:
    path = f"Files/ignite_data/{name}.csv"
    df = spark.read.option("header", True).option("inferSchema", True).csv(path)
    # Preserve identifier codes as strings, and normalize dates.
    if name == "fact_daily_sales": df = df.withColumn("SalesDate", F.to_date("SalesDate"))
    if name == "fact_inventory": df = df.withColumn("SnapshotDate", F.to_date("SnapshotDate"))
    if name == "fact_store_operations": df = df.withColumn("OperationDate", F.to_date("OperationDate"))
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(name)
    print(name, spark.table(name).count())

# Empty reveal table: populated later during Demo 3.
reveal_schema = StructType([StructField("EvidenceId",StringType()),StructField("EvidenceDate",StringType()),StructField("StoreId",StringType()),StructField("EvidenceType",StringType()),StructField("Observation",StringType()),StructField("Source",StringType()),StructField("Confidence",StringType())])
spark.createDataFrame([],reveal_schema).write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("new_evidence")
print("Setup complete; new_evidence starts with 0 rows")
