import pandas as pd

##Func.:Rename Column

def rename_column(df, old_column, new_column):

    if old_column not in df.columns:
        return df, f"❌ Column '{old_column}' does not exist."

    if not new_column.strip():
        return df, "❌ New column name cannot be empty."

    if new_column == old_column:
        return df, "ℹ️ New column name is the same as the current name."

    if new_column in df.columns:
        return df, f"❌ Column '{new_column}' already exists."

    df = df.rename(columns={old_column: new_column})

    return df, f"✅ Column renamed from '{old_column}' to '{new_column}'."

##Func. : Delete Column

def delete_column(df, column):

    if column not in df.columns:
        return df, f"❌ Column '{column}' does not exist."

    if len(df.columns) == 1:
        return df, "❌ Cannot delete the last remaining column."

    df = df.drop(columns=[column])

    return df, f"✅ Column '{column}' deleted."

##Func.: Filter Data

def filter_dataframe(df, column, operator, value):

    if column not in df.columns:
        return df, f"❌ Column '{column}' does not exist."

    if operator not in [">", "<", "=="]:
        return df, "❌ Invalid operator."

    try:

        if operator == ">":
            filtered_df = df[df[column] > value]

        elif operator == "<":
            filtered_df = df[df[column] < value]

        else:
            filtered_df = df[df[column] == value]

    except Exception:
        return df, f"❌ Cannot apply '{operator}' on column '{column}'."

    return filtered_df, f"✅ Filter returned {len(filtered_df)} row(s)."

##Func: Replace Values

def replace_values(df, column, old_value, new_value):

    if column not in df.columns:
        return df, f"❌ Column '{column}' does not exist."

    count = (df[column] == old_value).sum()

    if count == 0:
        return df, f"ℹ️ '{old_value}' not found in '{column}'."

    df[column] = df[column].replace(old_value, new_value)

    return df, f"✅ Replaced {count} value(s)."

##FUNC: Update cell value

def update_cell_value(df, search_column, search_value, update_column, new_value):

    if search_column not in df.columns:
        return df, f"❌ Column '{search_column}' does not exist."

    if update_column not in df.columns:
        return df, f"❌ Column '{update_column}' does not exist."

    mask = df[search_column] == search_value

    count = mask.sum()

    if count == 0:
        return df, f"ℹ️ No rows found where '{search_column}' = '{search_value}'."

    df.loc[mask, update_column] = new_value

    return df, f"✅ Updated {count} row(s)." 

##Func: Create New Column

def create_new_column(df, source_column, new_column, multiplier):

    if source_column not in df.columns:
        return df, f"❌ Column '{source_column}' does not exist."

    if new_column in df.columns:
        return df, f"❌ Column '{new_column}' already exists."

    if not pd.api.types.is_numeric_dtype(df[source_column]):
        return df, f"❌ '{source_column}' must be numeric."

    df[new_column] = df[source_column] * multiplier

    return df, f"✅ Column '{new_column}' created successfully."