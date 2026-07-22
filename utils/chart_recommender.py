import pandas as pd


def recommend_charts(df: pd.DataFrame):
    recommendations = []

    numeric_cols = list(df.select_dtypes(include="number").columns)
    categorical_cols = list(df.select_dtypes(include=["object", "category"]).columns)
    datetime_cols = list(df.select_dtypes(include="datetime").columns)

    # Histogram
    best_histogram = None
    best_variance = -1

    for col in numeric_cols:

        # Skip columns with too few unique values
        if df[col].nunique() < 10:
            continue

        # Skip ID-like columns
        if df[col].nunique() > 0.9 * len(df):
            continue

        variance = df[col].var()

        if variance > best_variance:
            best_variance = variance
            best_histogram = col

    if best_histogram:
        recommendations.append({
            "chart": "Histogram",
            "column": best_histogram,
            "reason": "Best numeric column for understanding data distribution."
        })


    # Box Plot
    best_box = None
    max_outliers = -1

    for col in numeric_cols:

        if df[col].nunique() < 10:
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = ((df[col] < lower) | (df[col] > upper)).sum()

        if outliers > max_outliers:
            max_outliers = outliers
            best_box = col

    if best_box:
        recommendations.append({
            "chart": "Box Plot",
            "column": best_box,
            "reason": "This column has the highest number of potential outliers."
        })

    # Bar Chart
    best_bar = None

    for col in categorical_cols:

        unique = df[col].nunique()

        # Avoid columns with too many categories
        if unique > 20:
            continue

        # Avoid columns with only one category
        if unique < 2:
            continue

        # Prefer columns with fewer missing values
        if best_bar is None:
            best_bar = col
        elif df[col].isnull().sum() < df[best_bar].isnull().sum():
            best_bar = col

    if best_bar:
        recommendations.append({
            "chart": "Bar Chart",
            "column": best_bar,
            "reason": "Best categorical column for comparing category frequencies."
        })


    # Scatter Plot
    if len(numeric_cols) >= 2:

        candidates = []

        for col in numeric_cols:

            # Skip ID-like columns
            if df[col].nunique() > 0.9 * len(df):
                continue

            # Skip columns with very few unique values
            if df[col].nunique() < 10:
                continue

            candidates.append((col, df[col].var()))

        candidates.sort(key=lambda x: x[1], reverse=True)

        if len(candidates) >= 2:

            recommendations.append({
                "chart": "Scatter Plot",
                "column": f"{candidates[0][0]} vs {candidates[1][0]}",
                "reason": "Compare the relationship between two informative numeric columns."
            })    

    # Heatmap
    if len(numeric_cols) >= 2:
        recommendations.append({
            "chart": "Correlation Heatmap",
            "column": "All Numeric Columns",
            "reason": "Find relationships between variables."
        })

    # Line Chart
    if datetime_cols and numeric_cols:
        recommendations.append({
            "chart": "Line Chart",
            "column": f"{datetime_cols[0]} vs {numeric_cols[0]}",
            "reason": "Analyze trends over time."
        })

    return recommendations