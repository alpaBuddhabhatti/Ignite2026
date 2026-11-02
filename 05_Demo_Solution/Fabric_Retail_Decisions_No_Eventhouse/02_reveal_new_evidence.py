# Run ONLY during Demo 3 after uploading new_evidence_reveal.csv to Files/ignite_data.
# This is a manual batch refresh, NOT real-time streaming.
from pyspark.sql import functions as F
path = "Files/ignite_data/new_evidence_reveal.csv"
df = spark.read.option("header",True).csv(path)
assert df.count() == 3, "Expected exactly 3 synthetic audit observations"
df.write.format("delta").mode("append").saveAsTable("new_evidence")
display(spark.sql("SELECT * FROM new_evidence ORDER BY EvidenceId"))
