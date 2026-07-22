import pandas as pd
##Func:Preprocess Data

def preprocess_dataframe(df):

    report = []

    # Standardize missing values
    missing_values = [
        "", " ", "NA", "N/A", "NaN", "nan",
        "NULL", "null", "None",
        "Unknown", "unknown",
        "?", "-", "--",
        "missing", "Missing"
    ]

    df.replace(missing_values, pd.NA, inplace=True)
    report.append("✅ Missing values standardized.")


    # Remove extra spaces from text columns
    for column in df.select_dtypes(include="object").columns:

        df[column] = df[column].str.strip()

    report.append("✅ Removed extra spaces.")

     

##Automatic Type Detection

    skip_keywords=[
        "id",
        "code",
        "phone",
        "mobile",
        "pin",
        "zip"
    ]
    
    for column in df.columns:

        # Skip non-object columns
        if df[column].dtype != "object":
            continue

        # Skip identifier columns
        if any(word in column.lower() for word in skip_keywords):
            report.append(f" {column}: kept as String (identifier detected)")
            continue

        ##Numeric Detection

        numeric = pd.to_numeric(df[column], errors="coerce")

        original_non_null = df[column].notna().sum()
        converted_non_null = numeric.notna().sum()

        if original_non_null == converted_non_null and original_non_null > 0:


            if (numeric.dropna() % 1 == 0).all():
                df[column] = numeric.astype("Int64")
                report.append(f"✅ {column}: converted to Integer")
            else:
                df[column] = numeric.astype(float)
                report.append(f"✅ {column}: converted to Float")

            continue

##smart detetime detection 

        dates = pd.to_datetime(df[column],format="mixed", errors="coerce")

        date_count = dates.notna().sum()

        if original_non_null > 0 and (date_count / original_non_null) >= 0.9:

            df[column] = dates
            report.append(f"✅ {column}: converted to Datetime")

            continue

        # ---------- Keep as String ----------

        report.append(f" {column}: kept as String")

    for col in df.columns:
        if df[col].map(type).nunique() > 1:
            df[col] = df[col].astype(str)

    return df, report