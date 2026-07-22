import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np

def plot_histogram(df, column):

    if column not in df.columns:
        return None, f"❌ Column '{column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[column]):
        return None, "❌ Histogram requires a numeric column."

    fig = px.histogram(
        df,
        x=column,
        nbins=20,
        title=f"Histogram of {column}"
    )

    return fig, "✅ Histogram created."



def plot_scatter(df, x_column, y_column):

    for col in [x_column, y_column]:
        if col not in df.columns:
            return None, f"❌ Column '{col}' does not exist."

        if not pd.api.types.is_numeric_dtype(df[col]):
            return None, "❌ Scatter plot requires numeric columns."

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{x_column} vs {y_column}"
    )

    return fig, "✅ Scatter plot created."


def plot_boxplot(df, column):

    if column not in df.columns:
        return None, f"❌ Column '{column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[column]):
        return None, "❌ Box plot requires a numeric column."

    fig = px.box(
        df,
        y=column,
        title=f"Box Plot of {column}"
    )

    return fig, "✅ Box plot created."



def plot_heatmap(df):

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None, "❌ Heatmap requires at least two numeric columns."

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    return fig, "✅ Correlation heatmap created."


def plot_line(df, x_column, y_column):

    if x_column not in df.columns:
        return None, f"❌ Column '{x_column}' does not exist."

    if y_column not in df.columns:
        return None, f"❌ Column '{y_column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[y_column]):
        return None, f"❌ '{y_column}' must be numeric."

    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} over {x_column}"
    )

    return fig, "✅ Line chart created."


def plot_bar(df, x_column, y_column):

    if x_column not in df.columns:
        return None, f"❌ Column '{x_column}' does not exist."

    if y_column not in df.columns:
        return None, f"❌ Column '{y_column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[y_column]):
        return None, f"❌ '{y_column}' must be numeric."

    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} by {x_column}"
    )

    return fig, "✅ Bar chart created."

def plot_pie(df, column):

    if column not in df.columns:
        return None, f"❌ Column '{column}' does not exist."

    if df[column].dropna().empty:
        return None, f"❌ '{column}' has no values to plot."

    counts = df[column].value_counts()

    fig = px.pie(
        names=counts.index,
        values=counts.values,
        title=f"Distribution of {column}"
    )

    return fig, "✅ Pie chart created."

def create_visualization(df, chart_type, x=None, y=None):

    chart_type = chart_type.lower()

    aliases = {
        "hist": "histogram",
        "distribution": "histogram",
        "scatter plot": "scatter",
        "scatterplot": "scatter",
        "box": "boxplot",
        "box plot": "boxplot",
        "line chart": "line",
        "bar chart": "bar",
        "pie chart": "pie",
    }

    chart_type = aliases.get(chart_type, chart_type)

    if chart_type == "histogram":
        return plot_histogram(df, x)

    elif chart_type == "scatter":
        return plot_scatter(df, x, y)

    elif chart_type == "boxplot":
        return plot_boxplot(df, x)

    elif chart_type == "heatmap":
        return plot_heatmap(df)

    elif chart_type == "line":
        return plot_line(df, x, y)

    elif chart_type == "bar":
        return plot_bar(df, x, y)

    elif chart_type == "pie":
        return plot_pie(df, x)

    else:
        return None, f"❌ Unsupported chart type '{chart_type}'."