# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "01c2b3de-5b6f-4a2d-b189-b2f56692d188",
# META       "default_lakehouse_name": "britam_claims_lakehouse",
# META       "default_lakehouse_workspace_id": "822346d9-b6b9-4faa-81c7-c913ba6296fd",
# META       "known_lakehouses": [
# META         {
# META           "id": "01c2b3de-5b6f-4a2d-b189-b2f56692d188"
# META         }
# META       ]
# META     },
# META     "warehouse": {}
# META   }
# META }

# MARKDOWN ********************

# ### 1. Data Ingestion & Schema Inference
# Reading raw CSV files from the Lakehouse `Files` directory. 
# *Business Justification:* We keep raw data immutable in the `Files` area and read it into Spark DataFrames for scalable, distributed processing.

# CELL ********************

# Import required functions
from pyspark.sql.functions import col, upper, trim, when, coalesce, lit
from pyspark.sql.types import DateType

# Read Batch 1 (Historical Data)
df_batch1 = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("Files/claims_batch_1.csv")

# Read Batch 2 (Incremental New Data)
df_batch2 = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("Files/claims_batch_2.csv")

print(f"Batch 1 loaded: {df_batch1.count()} records")
print(f"Batch 2 loaded: {df_batch2.count()} records")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 2. Data Quality & Standardization Pipeline
# Applying a reusable cleaning function to ensure consistency. 
# *Rules Applied:*
# 1. **Standardization:** Uppercase and trim `vehicle_category` (fixes 'suv', 'S.U.V').
# 2. **Typo Correction:** Map 'Pendng' -> 'Pending', 'Aproved' -> 'Approved'.
# 3. **Missing Values:** Impute missing `claim_amount` with 0.0 (Business rule: requires manual finance review, but prevents pipeline failure).
# 4. **Type Casting:** Ensure `claim_date` is a proper DateType.
# 5. **Feature Engineering:** Create `claim_severity` (Low < 10k, Medium 10k-50k, High > 50k) for downstream risk modeling.

# CELL ********************

def clean_claims_data(df):
    return (
        df
        # 1. Standardize Vehicle Category
        .withColumn("vehicle_category", upper(trim(col("vehicle_category"))))
        .withColumn("vehicle_category", when(col("vehicle_category") == "S.U.V", "SUV").otherwise(col("vehicle_category")))
        
        # 2. Fix Status Typos
        .withColumn("claim_status", 
            when(col("claim_status") == "Pendng", "Pending")
            .when(col("claim_status") == "Aproved", "Approved")
            .otherwise(col("claim_status"))
        )
        
        # 3. Handle Missing Amounts (Coalesce replaces nulls with 0.0)
        .withColumn("claim_amount", coalesce(col("claim_amount"), lit(0.0)))
        
        # 4. Cast Date
        .withColumn("claim_date", col("claim_date").cast(DateType()))
        
        # 5. Feature Engineering: Claim Severity
        .withColumn("claim_severity", 
            when(col("claim_amount") < 10000, "Low")
            .when((col("claim_amount") >= 10000) & (col("claim_amount") <= 50000), "Medium")
            .otherwise("High")
        )
    )

# Apply cleaning to both batches
df_clean_1 = clean_claims_data(df_batch1)
df_clean_2 = clean_claims_data(df_batch2)

# Show a sample of the cleaned data to verify transformations
display(df_clean_1.select("claim_id", "vehicle_category", "claim_status", "claim_amount", "claim_severity").limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 3. Initial Load: Writing Batch 1 to Delta Lake
# We write the cleaned historical data as a managed Delta table. 
# *Engineering Best Practice:* Delta format provides ACID transactions, schema enforcement, and time travel, which are critical for financial/insurance data governance.

# CELL ********************

# Write Batch 1 as a new Delta table, overwriting any existing test data
df_clean_1.write.format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable("claims_cleaned")

print("✅ Batch 1 successfully written to 'claims_cleaned' Delta table.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4. The "Wow" Factor: Incremental Merge (Upsert)
# Instead of blindly appending (which risks duplicates if a batch is re-run), we use the Delta Lake `merge` API. 
# *Logic:* Match on `claim_id`. If it exists, update it. If it doesn't exist (like all of Batch 2), insert it. This guarantees idempotency and data integrity.

# CELL ********************

from delta.tables import DeltaTable

# Load the existing target Delta table
deltaTable = DeltaTable.forName(spark, "claims_cleaned")

# Perform the Merge (Upsert)
(
    deltaTable.alias("target")
    .merge(
        df_clean_2.alias("source"),
        "target.claim_id = source.claim_id"
    )
    .whenMatchedUpdateAll() # Updates existing records if a claim is amended
    .whenNotMatchedInsertAll() # Inserts new records (our 300 Batch 2 claims)
    .execute()
)

print("✅ Incremental merge complete. Batch 2 integrated without duplicates.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 5. Validation & Governance Check
# Verifying the final state of the table to ensure 1,500 total records and proper schema enforcement.

# CELL ********************

# Verify total count and distinct batches
display(spark.sql("""
    SELECT 
        COUNT(*) as total_records, 
        COUNT(DISTINCT batch_id) as distinct_batches,
        SUM(CASE WHEN claim_amount = 0.0 THEN 1 ELSE 0 END) as null_amounts_imputed
    FROM claims_cleaned
"""))

# Verify the data is ready for Power BI
display(spark.sql("SELECT claim_severity, COUNT(*) as count FROM claims_cleaned GROUP BY claim_severity ORDER BY count DESC"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# <!-- ### 2. Data Quality & Standardization Pipeline
# 
# Applying a reusable cleaning function to ensure consistency. 
# *Rules Applied:*
# 1. **Standardization:** Uppercase and trim `vehicle_category` (fixes 'suv', 'S.U.V').
# 2. **Typo Correction:** Map 'Pendng' -> 'Pending', 'Aproved' -> 'Approved'.
# 3. **Missing Values:** Impute missing `claim_amount` with 0.0 (Business rule: requires manual finance review, but prevents pipeline failure).
# 4. **Type Casting:** Ensure `claim_date` is a proper DateType.
# 5. **Feature Engineering:** Create `claim_severity` (Low < 10k, Medium 10k-50k, High > 50k) for downstream risk modeling. -->

# MARKDOWN ********************

# <!-- 
# ### 2. Data Quality & Standardization Pipeline
# Applying a reusable cleaning function to ensure consistency. 
# *Rules Applied:*
# 1. **Standardization:** Uppercase and trim `vehicle_category` (fixes 'suv', 'S.U.V').
# 2. **Typo Correction:** Map 'Pendng' -> 'Pending', 'Aproved' -> 'Approved'.
# 3. **Missing Values:** Impute missing `claim_amount` with 0.0 (Business rule: requires manual finance review, but prevents pipeline failure).
# 4. **Type Casting:** Ensure `claim_date` is a proper DateType.
# 5. **Feature Engineering:** Create `claim_severity` (Low < 10k, Medium 10k-50k, High > 50k) for downstream risk modeling. -->
