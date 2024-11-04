from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

# Initialize Spark session
spark = SparkSession.builder.appName("TelecomDataAnalysis").getOrCreate()

# Load data (assuming CSV files are stored in HDFS or local storage)
data = spark.read.csv("telecom_data.csv", header=True, inferSchema=True)

# Sample data schema could include: ['user_id', 'call_duration', 'messages_sent', 'data_usage_mb', 'location']

# Data Preprocessing: Select relevant columns and clean the data
clean_data = data.select('user_id', 'call_duration', 'messages_sent', 'data_usage_mb', 'location')

# Aggregating data by users to get total usage
aggregated_data = clean_data.groupBy('user_id').agg(
    sum('call_duration').alias('total_call_duration'),
    sum('messages_sent').alias('total_messages'),
    sum('data_usage_mb').alias('total_data_usage'),
    avg('location').alias('avg_location')
)

# Multi-Dimensional Analysis - KMeans Clustering to classify users into segments
# Combine features into a single vector for clustering
assembler = VectorAssembler(inputCols=['total_call_duration', 'total_messages', 'total_data_usage'], outputCol='features')
feature_data = assembler.transform(aggregated_data)

# Apply KMeans Clustering
kmeans = KMeans(k=3, seed=1)  # Set number of clusters (e.g., 3 clusters)
model = kmeans.fit(feature_data)

# Predict user clusters
clustered_data = model.transform(feature_data)

# Show clustered results
clustered_data.select('user_id', 'total_call_duration', 'total_messages', 'total_data_usage', 'prediction').show()

# Example output would show which users fall into which cluster, providing insights into user behavior
