import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm= ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_ai_insights(df):
    rows,cols= df.shape

    missing=df.isnull().sum().sum()
    
    duplicates=df.duplicated().sum()

    numeric_col=df.select_dtypes(include="number").columns.tolist()

    categorical_col=df.select_dtypes(
        include=["object", "string","category"]
    ).columns.tolist()

    summary=f"""
Dataset Summary

Rows: {rows}

Columns:{cols}

Missing Values:{missing}

Duplicate Rows:{duplicates}

Numeric Columns:{numeric_col}

Categorical Columns:{categorical_col}

Statistics

{df.describe(include="all").to_string()}
    """
    prompt=ChatPromptTemplate.from_template(
        """
You are an expert Data Analyst.

Analyze the dataset summary below.

Provide:

1. Executive Summary

2. Data Quality Issues

3. Important Patterns

4. Possible Outliers

5. Recommended Cleaning Steps

6. Suggested Visualizations

7. Machine Learning Readiness

Keep the answer professional and concise.

Dataset:

{summary}
"""
    )
    chain = prompt | llm

    response= chain.invoke(
        {
            "summary":summary
        }
    )    

    return response.content

