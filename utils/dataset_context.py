import pandas as pd

def get_dataset_context(df: pd.DataFrame)-> str:
    """
    Generates a concise dataset summary for the AI. 
    """
    rows, cols = df.shape

    missing = df.isnull().sum().to_dict()

    duplicates = int(df.duplicated().sum())

    dtypes = df.dtypes.astype(str).to_dict()

    numeric_summary = ""

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        numeric_summary = numeric_df.describe().to_string()

    categorical_summary = ""

    categorical_df = df.select_dtypes(
        include=["object", "string", "category"]
    )

    if not categorical_df.empty:
        categorical_summary = categorical_df.describe().to_string()

    sample_data = df.head(5).to_markdown(index=False)

    context = f"""
Dataset Overview

Rows: {rows}
Columns: {cols}

Column Names:
{list(df.columns)}

Data Types:
{dtypes}

Missing Values:
{missing}

Duplicate Rows:
{duplicates}

Numeric Summary:
{numeric_summary}

Categorical Summary:
{categorical_summary}

Sample Data:
{sample_data}
"""

    return context