import pandas as pd

def replace_null_values(df, column, method="mean"):
    """
    Replace missing values in a column.
    """

    if column not in df.columns:
        return df, f"❌ Column '{column}' does not exist."

    if method not in ["mean", "median", "mode"]:
        return df, f"❌ Invalid method '{method}'."

    missing = df[column].isna().sum()

    if missing == 0:
        return df, f"ℹ️ No missing values found in '{column}'."

    if method in ["mean", "median"]:

        if not pd.api.types.is_numeric_dtype(df[column]):
            return df, f"❌ '{column}' must be numeric to use {method}."

        if method == "mean":
            value = df[column].mean()
        else:
            value = df[column].median()

    else:
        mode = df[column].mode()

        if mode.empty:
            return df, f"❌ Unable to calculate mode for '{column}'."

        value = mode.iloc[0]

    df[column] = df[column].fillna(value)

    return df, f"✅ Replaced {missing} missing value(s) in '{column}' using {method}."

##Function:remove Duplicate Rows
def remove_duplicates(df):
    original_rows = len(df)

    df = df.drop_duplicates()

    removed = original_rows - len(df)

    if removed == 0:
        return df, "ℹ️ No duplicate rows found."

    return df, f"✅ Removed {removed} duplicate row(s)."

##Function: Sort Data

def sort_dataframe(df, column, ascending=True):

    if column not in df.columns:
        return df, f"❌ Column '{column}' does not exist."

    if df.empty:
        return df, "❌ Dataset is empty."

    df = df.sort_values(by=column, ascending=ascending)

    order = "ascending" if ascending else "descending"

    return df, f"✅ Dataset sorted by '{column}' ({order})."