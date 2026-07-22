
import streamlit as st
import pandas as pd
import os
from utils.preprocessing import preprocess_dataframe
from utils.cleaning import(
    replace_null_values,
    remove_duplicates,
    sort_dataframe,
)
from utils.editing import(
    rename_column,
    delete_column,filter_dataframe,
    replace_values,
    update_cell_value,
    create_new_column,
)
from utils.reports import data_quality_report 
from utils.vizualization import (
    plot_histogram,
    plot_scatter,
    plot_boxplot,
    plot_heatmap,
    plot_line,
    plot_bar,
    plot_pie              
)   
from utils.ai_insights import generate_ai_insights
from utils.agent import run_agent
from utils.plan_formatter import format_execution_plan
from utils.planner import create_plan
from utils.dataset_context import get_dataset_context
from utils.health_check import dataset_health_check
from utils.pdf_report import generate_pdf_report


##Streamlit Page

st.set_page_config(
    page_title="KINTSUGI",
    layout="wide"
)




# Session State Initialization
if "df" not in st.session_state:
    st.session_state.df = None

if "history" not in st.session_state:
    st.session_state.history = []

if "redo_history" not in st.session_state:
    st.session_state.redo_history = []

if "operation_history" not in st.session_state:
    st.session_state.operation_history = []

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "dataset_versions" not in st.session_state:
    st.session_state.dataset_versions = []

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = []  

if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = {
        "last_operation": None,
        "last_columns": [],
        "last_chart": None
    }         

col1, col2 = st.columns([1, 8])

with col1:
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    st.image("KS.png", width=90)

with col2:
    st.title("KINTSUGI")
    st.caption("AI-Driven Data Analyst")

uploaded_file=st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
 

    os.makedirs("uploads",exist_ok=True)
    file_path=os.path.join("uploads",uploaded_file.name)

    with open(file_path,"wb") as f:
        f.write(uploaded_file.getbuffer())

    if (
        st.session_state.df is None
        or st.session_state.current_file != uploaded_file.name
    ):

        # Load the dataset
        st.session_state.df = pd.read_csv(file_path)

        # Reset history for the new dataset
        st.session_state.history.clear()
        st.session_state.redo_history.clear()
        st.session_state.operation_history.clear()
        st.session_state.chat_memory.clear()


        # Preprocess the dataset
        st.session_state.df, report = preprocess_dataframe(
            st.session_state.df
        )

        # Generate quality report
        quality = data_quality_report(
            st.session_state.df,
            report
        )

        # Remember the current file
        st.session_state.current_file = uploaded_file.name
        
        st.session_state.dataset_versions = [
            {
                "version": 1,
                "name": "Original Upload",
                "df": st.session_state.df.copy()
            }
        ]
        
    df = st.session_state.df

    

    st.success("✅ CSV Uploaded Successfully") 

    

    st.subheader("📊 Data Preview")

    st.dataframe(
        df,
        use_container_width=True
    )       

    health = dataset_health_check(df)
    
    st.subheader("🧠Dataset Health Check")
    

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Health Score", f"{health['score']}/100")

    with col2:
        st.metric("Missing Values", health["missing_values"])

    with col3:
        st.metric("Duplicate Rows", health["duplicate_rows"])

    with col4:
        st.metric("Outlier Columns", len(health["outlier_columns"]))


    st.markdown("### 💡 AI Suggestions")

    if health["duplicate_rows"] > 0:
        st.warning(
            f"Found {health['duplicate_rows']} duplicate rows. Consider removing them."
        )

    if health["missing_values"] > 0:
        st.warning(
            f"Found {health['missing_values']} missing values. Fill them before analysis."
        )

    if health["outlier_columns"]:
        st.info(
            "Outliers detected in: "
            + ", ".join(health["outlier_columns"])
        )

    if (
        health["duplicate_rows"] == 0
        and health["missing_values"] == 0
        and not health["outlier_columns"]
    ):
        st.success("🎉 Dataset looks clean and ready for analysis!")

    
    
    

###Metrics
    col1,col2,col3=st.columns(3)

    col1.metric("Rows",df.shape[0])
    col2.metric("Columns",df.shape[1])
    col3.metric("Missing Values",int(df.isnull().sum().sum()))

##Data types
    st.subheader("Column Data Types")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(
        columns={"index":"Column",0:"Data Type"}
    ))  

##Missing Values     

    st.subheader("❗Missing Values")
    st.dataframe(
        df.isnull().sum().reset_index().rename(
            columns={"index":"Column",0:"Missing Count"}
        )
    ) 

##Basic Statistics
    st.subheader("🔢Numeric Statistics")
    st.dataframe(df.describe())

    st.subheader("📁Category Summary")

    try:
        st.dataframe(df.describe(include=["object", "string", "category"]))
    except ValueError:
        st.info("No categorical columns found.")




###DATA CLEANING

    st.subheader("🧹Data Cleaning")

    selected_column=st.selectbox(
       "Select Column",
        df.columns
    )

    method=st.selectbox(
        "Replacement Method",
        ["mean", "median", "mode"]
    )

    if st.button("Replace Null Values"):

        df, message=replace_null_values(
            df,
            selected_column,
            method
        )
        
        st.session_state.df=df
        st.success(message)

        st.subheader("Updated Dataset")

        st.dataframe(df, use_container_width=True)


##Remove Duplicates

    st.subheader("Remove Duplicate Rows")

    if st.button("Remove Duplicate"):

        df, message= remove_duplicates(df)
        st.session_state.df=df
        st.success(message)
        st.subheader("Updated Dataset")
        st.dataframe(df, use_container_width=True)

##Sort Data
        
    st.subheader("📊Sort Data")

    sort_column=st.selectbox(
        "Select Column to Sort",
        df.columns,
        key="sort_column"
    )

    sort_order=st.radio(
        "Sort Order",
        ["Ascending", "Descending"]
    )

    if st.button("Sort Data"):
        ascending= True if sort_order== "Ascending" else False

        df, message= sort_dataframe(
            df,
            sort_column,
            ascending
        )
        
        st.session_state.df=df
        st.success(message)
        st.subheader("Sorted Dataset")
        st.dataframe(df, use_container_width=True)

##Rename Column

    st.subheader("🖋️Rename Column")

    old_column=st.selectbox(
        "Select Column",
        df.columns,
        key="rename_column"
    )

    new_column=st.text_input("Enter New Column Name")

    if st.button("Rename Column"):
        if new_column.strip()=="":
            st.error("Please enter a new column name.")

        else:
            df, message= rename_column(
                df,
                old_column,
                new_column
            )
            
            st.session_state.df=df
            st.success(message)
            st.dataframe(df, use_container_width=True) 

##Delete Column

    st.subheader("🗑️Delete Column")

    delete_col= st.selectbox(
        "Select Column to Delete",
        df.columns,
        key="delete_column"

    ) 

    if st.button("Delete Column"):

        df, message=delete_column(
            df,
            delete_col
        )             
        st.session_state.df=df
        st.success(message)
        st.dataframe(df, use_container_width=True) 



##filter data
    
    st.subheader("🔍Filter Data")

    filter_column= st.selectbox(
        "Select Column",
        df.columns,
        key="filter_column"
    )  

    operator= st.selectbox(
        "Condition",
        [">", "<" , "=="]
    ) 

    filter_value= st.number_input(
        "Enter Value",
        value=0  
    ) 

    if st.button("Apply Filter"):

        filtered_df, message= filter_dataframe(
            df,
            filter_column,
            operator,
            filter_value,
        )    

        st.success(message)
        st.subheader("Filtered Dataset")
        st.dataframe(filtered_df, use_container_width=True)

## Replace Values
    
    st.subheader("🔁Replace Values")

    replace_column= st.selectbox(
        "Select Column",
        df.columns,
        key="replace_values_column"
    )

    old_value=st.text_input(
        "Value to Replace",
        key="old_value"
    )

    new_value=st.text_input(
        "Replace With",
        key="new_value"
    )

    if st.button("Replace Values"):

        df, message= replace_values(
            
            df,
            replace_column,
            old_value,
            new_value
        )

        st.success(message)

        st.subheader("Updated Dataset")

        st.dataframe(df, use_container_width=True)

## Update Cell Value

    st.subheader("✏️ Update Cell Value")

    search_column = st.selectbox(
        "Search Column",
        df.columns,
        key="search_column"
    )

    search_value = st.text_input(
        "Search Value",
        key="search_value"
    )

    update_column = st.selectbox(
        "Column to Update",
        df.columns,
        key="update_column"
    )

    new_value = st.text_input(
        "New Value",
        key="new_value_update"
    )

    if st.button("Update Cell"):

        df, message = update_cell_value(
            df,
            search_column,
            search_value,
            update_column,
            new_value
        )

        st.success(message)

        st.subheader("Updated Dataset")

        st.dataframe(df, use_container_width=True) 

## Create New column

    st.subheader("🆕Create New Column")

    source_column= st.selectbox(
        "Source Column",
        df.columns,
        key="source_column"
    ) 

    multiplier= st.number_input(
        "Multiplier",
        value=1.0
    ) 

    new_column= st.text_input(
        "New Column Name",
        key="new_column_name"
    )

    if st.button("Create Column"):

        if new_column.strip()=="":
            st.error("Please enter a column name.")

        else:

            df, message= create_new_column(
                df,
                source_column,
                new_column,
                multiplier
            ) 

            st.success(message)

            st.dataframe(df, use_container_width=True)



##Vizualization Dashboard
    st.subheader("📈Visualization Dashboard")
    chart_type= st.selectbox(
        "Choose Chart",
        [
            "Histogram",
            "Scatter Plot",
            "Box Plot",
            "Correlation Heatmap",
            "Line Chart",
            "Bar Chart",
            "Pie Chart"
        ]
    )

    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns
    
    if chart_type=="Histogram":
        column=st.selectbox(
            "Select Numeric Column",
            numeric_columns,
            key="hist"
        )

        if st.button("Generate"):

            fig, message = plot_histogram(df, column)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)

    elif chart_type == "Scatter Plot":

        x = st.selectbox(
            "X-axis",
            numeric_columns,
            key="scatter_x"
        )

        y = st.selectbox(
            "Y-axis",
            numeric_columns,
            key="scatter_y"
        )

        if st.button("Generate"):

            fig, message = plot_scatter(df, x, y)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)

    
    elif chart_type == "Box Plot":

        column = st.selectbox(
            "Numeric Column",
            numeric_columns,
            key="box"
        )

        if st.button("Generate"):

            fig, message = plot_boxplot(df, column)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)


    elif chart_type == "Correlation Heatmap":

        if st.button("Generate"):

            fig, message = plot_heatmap(df)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)        
    


    elif chart_type == "Line Chart":

        x = st.selectbox(
            "X-axis",
            df.columns,
            key="line_x"
        )

        y = st.selectbox(
            "Y-axis",
            numeric_columns,
            key="line_y"
        )

        if st.button("Generate"):

            fig, message = plot_line(df, x, y)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)


    elif chart_type == "Bar Chart":

        x = st.selectbox(
            "Category",
            df.columns,
            key="bar_x"
        )

        y = st.selectbox(
            "Value",
            numeric_columns,
            key="bar_y"
        )

        if st.button("Generate"):

            fig, message = plot_bar(df, x, y)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)


    elif chart_type == "Pie Chart":

        column = st.selectbox(
            "Category Column",
            categorical_columns,
            key="pie"
        )

        if st.button("Generate"):

            fig, message = plot_pie(df, column)

            if fig is not None:
                st.success(message)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(message)   
    

    ## AI Insights
    
    st.subheader("🧠AI Insights")

    st.write(
        "Generate an AI-powered analysis of your dataset, including trends, "
        "data quality issues, and recommendations."
    )

    if st.button("Generate AI Insights"):

        with st.spinner("Analyzing dataset..."):

            insights = generate_ai_insights(st.session_state.df)

        st.success("Analysis Complete!")

        st.markdown(insights)



    ##Data visualization
    st.subheader("🤖 AI Data Assistant")

    user_query = st.text_input(
        "Ask KINTSUGI",
        placeholder="Example: Remove duplicate rows"
    )

    if st.button("Run AI Agent"):

        if user_query.strip() == "":
            st.warning("Please enter a request.")

        else:

            dataset_context = get_dataset_context(df)

            plan = create_plan(
                question=user_query,
                dataset_context=dataset_context
            )

            st.info("📝 Planned Operations")

            st.markdown(format_execution_plan(plan))

            try:
                response = run_agent(df, user_query , st.session_state.chat_memory, st.session_state.ai_memory)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

            if response["type"] == "multi_step":

                for result in response["responses"]:

                    if result["type"] == "analysis":

                        st.markdown(result["response"])

                    elif result["type"] == "visualization":

                        if result["figure"] is not None:
                            st.success(result["message"])
                            st.plotly_chart(
                                result["figure"],
                                use_container_width=True
                            )
                        else:
                            st.error(result["message"])
                            st.session_state.ai_memory["last_chart"] = result["message"]



                    elif result["type"] == "dataframe":

                        st.session_state.history.append(st.session_state.df.copy())
                        st.session_state.redo_history.clear()

                        st.session_state.operation_history.append(result["message"])
                        st.session_state.ai_memory["last_operation"] = result["message"]
                        st.success(result["message"])

                    elif result["type"] == "error":

                        st.error(result["message"])

                st.session_state.df = response["final_df"]

# Save a new dataset version
            if response["final_df"] is not None:
                last_operation = (
                    st.session_state.operation_history[-1]
                    if st.session_state.operation_history
                    else "AI Operation"
                )

                st.session_state.dataset_versions.append(
                        {
                            "version": len(st.session_state.dataset_versions) + 1,
                            "name": last_operation,
                            "df": st.session_state.df.copy()
                        }
                    )

                st.dataframe(
                    response["final_df"],
                    use_container_width=True
                )

                st.session_state.chat_memory.append(
                    {
                        "user": user_query,
                        "assistant": "Request completed successfully."
                    }
                )

                # Keep only the last 10 conversations
                if len(st.session_state.chat_memory) > 10:
                    st.session_state.chat_memory.pop(0)
        
            else:
                st.error("❌ The AI could not process your request.")


    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("↩ Undo"):

            if st.session_state.history:

                st.session_state.redo_history.append(
                    st.session_state.df.copy()
                )

                st.session_state.df = st.session_state.history.pop()

                st.success("Last operation undone.")

                st.dataframe(
                    st.session_state.df,
                    use_container_width=True
                )

            else:
                st.info("Nothing to undo.")

    with col2:
        if st.button("↪ Redo"):

            if st.session_state.redo_history:

                st.session_state.history.append(
                    st.session_state.df.copy()
                )

                st.session_state.df = st.session_state.redo_history.pop()

                st.success("Operation restored.")

                st.dataframe(
                    st.session_state.df,
                    use_container_width=True
                )

            else:
                st.info("Nothing to redo.")
                      
    
    ##Operation History
    st.subheader("📜","Operation History")

    if st.session_state.operation_history:

        for i, operation in enumerate(
            reversed(st.session_state.operation_history),
            start=1
        ):
            st.write(f"{i}. {operation}")

    else:
        st.info("No operations performed yet.")


    #download cleaned dataset
    st.markdown("---")
    st.subheader("📥","Download Cleaned Dataset")

    if st.session_state.df is not None:

        csv = st.session_state.df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )    
    
    #Generate Pdf Report
    if st.button("📄 Generate PDF Report"):

        generate_pdf_report(
            filename="Kintsugi_Report.pdf",
            dataset_name=uploaded_file.name,
            rows=st.session_state.df.shape[0],
            columns=st.session_state.df.shape[1],
            
            operation_history=st.session_state.operation_history,
            ai_summary="Dataset cleaned successfully."
        )

        with open("Kintsugi_Report.pdf", "rb") as pdf:

            st.download_button(
                "⬇ Download PDF",
                pdf,
                file_name="Kintsugi_Report.pdf",
                mime="application/pdf"
            )