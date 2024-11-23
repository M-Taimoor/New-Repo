import pandas as pd
import os

# Step 1: Define file paths
SOURCE_FILE = "source_data.csv"  # Example source file
TRANSFORMED_FILE = "transformed_data.csv"  # Transformed file
DVC_TRACKED_FILE = "warehouse_data.csv"  # Final data tracked by DVC

# Step 2: Extract Data
def extract_data():
    # Create a sample source dataset if it doesn't exist
    if not os.path.exists(SOURCE_FILE):
        data = {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "income": [50000, 60000, 70000],
        }
        df = pd.DataFrame(data)
        df.to_csv(SOURCE_FILE, index=False)
    return pd.read_csv(SOURCE_FILE)

# Step 3: Transform Data
def transform_data(df):
    # Example transformation: Add a new column and filter rows
    df["income_in_k"] = df["income"] / 1000  # Income in thousands
    return df[df["age"] > 25]  # Filter for age > 25

# Step 4: Load Data
def load_data(df):
    # Save transformed data
    df.to_csv(TRANSFORMED_FILE, index=False)
    # Simulate loading into the warehouse
    df.to_csv(DVC_TRACKED_FILE, index=False)

# Step 5: Data Lineage Verification (Test)
def verify_data_lineage():
    # Compare source and transformed data for lineage verification
    source_df = pd.read_csv(SOURCE_FILE)
    transformed_df = pd.read_csv(TRANSFORMED_FILE)
    dvc_df = pd.read_csv(DVC_TRACKED_FILE)

    # Check lineage: All transformed data must have valid IDs from the source
    valid_ids = set(source_df["id"])
    transformed_ids = set(transformed_df["id"])
    assert transformed_ids.issubset(valid_ids), "Lineage test failed: Invalid IDs in transformed data."

    # Check that the final data matches the transformed data
    assert transformed_df.equals(dvc_df), "Lineage test failed: Final data does not match transformed data."

    print("Data lineage verification passed!")

# Main function to run the ETL process
def run_etl_pipeline():
    # Extract
    source_data = extract_data()
    print("Source Data Extracted:\n", source_data)

    # Transform
    transformed_data = transform_data(source_data)
    print("Transformed Data:\n", transformed_data)

    # Load
    load_data(transformed_data)
    print("Data loaded into DVC-tracked file.")

    # Verify Lineage
    verify_data_lineage()

if __name__ == "__main__":
    run_etl_pipeline()
