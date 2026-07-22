import pandas as pd


def dataset_health_check(df: pd.DataFrame) -> dict:
    """Analyze dataset quality and return health statistics."""

    total_cells = df.shape[0] * df.shape[1]

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    numeric_cols = df.select_dtypes(include="number").columns

    outlier_columns = []

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        if ((df[col] < lower) | (df[col] > upper)).sum() > 0:
            outlier_columns.append(col)

    object_columns = list(
        df.select_dtypes(include="object").columns
    )

    score = 100

    if total_cells > 0:
        score -= (missing_values / total_cells) * 50

    score -= duplicate_rows * 0.5

    score -= len(outlier_columns) * 2

    score = max(0, round(score))

    return {
        "score": score,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "outlier_columns": outlier_columns,
        "object_columns": object_columns,
    }