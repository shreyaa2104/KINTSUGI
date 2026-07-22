import pandas as pd

def answer_locally(df: pd.DataFrame, question: str):

    q = question.lower()

    # Rows
    if "row" in q:
        return f"The dataset contains **{df.shape[0]} rows**."

    # Columns
    if "column" in q and ("how many" in q or "number" in q):
        return f"The dataset contains **{df.shape[1]} columns**."

    # Missing values
    if "missing" in q:

        missing = df.isnull().sum()

        if missing.sum() == 0:
            return "✅ No missing values found."

        return (
            "### Missing Values\n\n"
            + missing[missing > 0].to_markdown()
        )

    # Duplicate rows
    if "duplicate" in q:

        duplicates = int(df.duplicated().sum())

        return f"Duplicate Rows: **{duplicates}**"

    # Column names
    if "column names" in q or "list columns" in q:

        cols = "\n".join(
            f"- {c}" for c in df.columns
        )

        return cols

    # Data types
    if "data type" in q or "datatype" in q:

        return df.dtypes.astype(str).to_markdown()

    return None