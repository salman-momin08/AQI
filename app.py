import streamlit as st
import pandas as pd
import time
import plotly.express as px

# Function to load and display CSV data with progress bar
def load_data(file):
    try:
        with st.spinner(f"Loading {file.name}..."):
            time.sleep(1)  # Simulating loading time
            df = pd.read_csv(file)
            st.session_state.file_loaded = True  # Mark the file as loaded in session state
            st.session_state.file_name = file.name  # Store the file name in session state
            st.success(f"File '{file.name}' loaded successfully!")
            time.sleep(2)
            return df
    except Exception as e:
        st.session_state.file_loaded = False
        st.error(f"Failed to load the file: {e}")
        return None

# Function to display raw data
def display_raw_data(df, file_name="File"):
    st.subheader(f"Raw Data from {file_name}")
    st.write(df)

# Function to display data type information
def display_data_types(df, file_name="File"):
    st.subheader(f"Data Types Information from {file_name}")
    st.write(df.dtypes)

# Function to filter data by a specific column
def filter_data(df, column):
    unique_values = df[column].unique()
    filter_values = st.sidebar.multiselect(f"Select {column} values to filter by", unique_values)
    if filter_values:
        filtered_df = df[df[column].isin(filter_values)]
        return filtered_df
    return df

# Function to compare two dataframes side by side
def compare_dataframes(df1, df2):
    st.subheader("Comparison of the Two Files")
    
    # Find common columns
    common_columns = list(set(df1.columns).intersection(set(df2.columns)))
    
    # If the two files don't have the same columns, display a message
    if not common_columns:
        st.warning("The two files do not have any common columns to compare.")
        return
    
    # Display the two dataframes side by side with common columns
    st.write("File 1:")
    st.write(df1[common_columns])
    
    st.write("File 2:")
    st.write(df2[common_columns])

# Function to display bar chart
def bar_chart(df, x_col, y_col):
    fig = px.bar(df, x=x_col, y=y_col, title="Bar Chart")
    st.plotly_chart(fig)

# Function to display line chart
def line_chart(df, x_col, y_col):
    fig = px.line(df, x=x_col, y=y_col, title="Line Chart")
    st.plotly_chart(fig)

# Function to display pie chart
def pie_chart(df, col):
    fig = px.pie(df, names=col, title="Pie Chart")
    st.plotly_chart(fig)

# Function to display scatter chart
def scatter_chart(df, x_col, y_col):
    fig = px.scatter(df, x=x_col, y=y_col, title="Scatter Plot")
    st.plotly_chart(fig)

# Function to display histogram
def histogram(df, col):
    fig = px.histogram(df, x=col, title="Histogram")
    st.plotly_chart(fig)

def main():
    st.title("CSV Data Analysis - Compare Files with Charts")

    # File Upload - One uploader that accepts both files
    files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

    # Handle file upload
    if files:
        # Check if there are one or two files uploaded
        if len(files) == 1:
            file1 = files[0]
            df1 = load_data(file1)
            df2 = None  # No second file for comparison
            file_names = [file1.name]  # Store the name of the single file
        elif len(files) == 2:
            file1, file2 = files
            df1 = load_data(file1)
            df2 = load_data(file2)
            file_names = [file1.name, file2.name]  # Store the names of both files
        else:
            st.warning("Please upload one or two CSV files.")
            return

        # Sidebar Controls for Filtering
        st.sidebar.title("Filters")

        # Only allow filtering if both files are loaded
        filter_column1 = st.sidebar.selectbox(f"Select column to filter by for {file_names[0]}", df1.columns)
        df1_filtered = filter_data(df1, filter_column1)

        if df2 is not None:
            filter_column2 = st.sidebar.selectbox(f"Select column to filter by for {file_names[1]}", df2.columns)
            df2_filtered = filter_data(df2, filter_column2)

        # Display Raw Data and Data Type Information
        show_raw_data = st.sidebar.checkbox("Show Raw Data")
        show_data_types = st.sidebar.checkbox("Show Data Types Information")

        if show_raw_data:
            # Ask the user which file's raw data they want to see (only if two files are uploaded)
            if df2 is not None:
                raw_data_file = st.sidebar.radio("Which file's raw data to display?", file_names)
                if raw_data_file == file_names[0]:
                    display_raw_data(df1_filtered, file_names[0])
                elif raw_data_file == file_names[1]:
                    display_raw_data(df2_filtered, file_names[1])
            else:
                display_raw_data(df1_filtered, file_names[0])  # Only one file, no radio button needed
        
        if show_data_types:
            # Ask the user which file's data types to display (only if two files are uploaded)
            if df2 is not None:
                data_types_file = st.sidebar.radio("Which file's data types to display?", file_names)
                if data_types_file == file_names[0]:
                    display_data_types(df1_filtered, file_names[0])
                elif data_types_file == file_names[1]:
                    display_data_types(df2_filtered, file_names[1])
            else:
                display_data_types(df1_filtered, file_names[0])  # Only one file, no radio button needed

        # Compare DataFrames if two files are uploaded and the user opts for comparison
        if df2 is not None:
            start_comparison = st.checkbox("Start File Comparison")
            if start_comparison:
                compare_dataframes(df1_filtered, df2_filtered)

        # Chart Selection in Sidebar
        st.sidebar.subheader("Chart Options")
        chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar", "Line", "Pie", "Scatter", "Histogram"])

        # Select columns for charting
        columns = df1.columns.tolist()

        # Based on chart type, show column selectors
        if chart_type == "Bar" or chart_type == "Line" or chart_type == "Scatter":
            x_col = st.sidebar.selectbox("Select X-Axis", columns)
            y_col = st.sidebar.selectbox("Select Y-Axis", columns)
        
        elif chart_type == "Pie":
            col = st.sidebar.selectbox("Select Column", columns)
        
        elif chart_type == "Histogram":
            col = st.sidebar.selectbox("Select Column", columns)

        # Render the selected chart
        if chart_type == "Bar":
            bar_chart(df1_filtered, x_col, y_col)
        elif chart_type == "Line":
            line_chart(df1_filtered, x_col, y_col)
        elif chart_type == "Pie":
            pie_chart(df1_filtered, col)
        elif chart_type == "Scatter":
            scatter_chart(df1_filtered, x_col, y_col)
        elif chart_type == "Histogram":
            histogram(df1_filtered, col)

    else:
        if not st.session_state.get("file_loaded", False):
            st.write("Please upload one or two CSV files to start.")
        else:
            pass

if __name__ == "__main__":
    if "file_loaded" not in st.session_state:
        st.session_state.file_loaded = False  # Initialize session state for file_loaded
    main()
