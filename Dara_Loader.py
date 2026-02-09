from promptflow import tool
import pandas as pd
import os


@tool
def load_data():
    """
    Loads the DataCo Supply Chain CSV file and returns schema information.
    """

    file_path = "data/DataCoSupplyChainDataset.csv"

    if not os.path.exists(file_path):
        return {
            "error": f"File not found: {file_path}",
            "schema": "",
            "sample_data": "",
            "columns": []
        }

    try:
        # Load CSV
        df = pd.read_csv(file_path, encoding="ISO-8859-1")

        # Clean column names
        df.columns = [
            col.replace(" ", "_")
               .replace("(", "")
               .replace(")", "")
               .replace("/", "_")
            for col in df.columns
        ]

        # Build schema info
        schema = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            sample_values = df[col].dropna().unique()[:3].tolist()
            schema.append(f"- {col} ({dtype}): e.g., {sample_values}")

        return {
            "file_path": file_path,
            "schema": "\n".join(schema),
            "sample_data": df.head(5).to_string(index=False),
            "columns": df.columns.tolist()
        }

    except Exception as e:
        return {
            "error": str(e),
            "schema": "",
            "sample_data": "",
            "columns": []
        }
    
