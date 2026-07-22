import pandas as pd

##Function :Data Quality Report

def data_quality_report(df, report):

    quality = {}

    quality["Total Rows"] = df.shape[0]
    quality["Total Columns"] = df.shape[1]

    quality["Missing Values"] = df.isnull().sum().sum()

    quality["Duplicate Rows"] = df.duplicated().sum()

    quality["Numeric Columns"] = len(
        df.select_dtypes(include="number").columns
    )

    quality["Categorical Columns"] = len(
        df.select_dtypes(include="object").columns
    )

    quality["Datetime Columns"] = len(
        df.select_dtypes(include="datetime").columns
    )

    return quality 