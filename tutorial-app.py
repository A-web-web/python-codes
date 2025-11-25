import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Data Analysis App",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Interactive Data Analysis App")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=['csv']
    )

    # Sample data option
    use_sample = st.checkbox("Use sample data")

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
elif use_sample:
    # Create sample data
    np.random.seed(42)
    df = pd.DataFrame({
        'Category': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Value1': np.random.normal(100, 15, 100),
        'Value2': np.random.normal(50, 10, 100),
        'Date': pd.date_range('2023-01-01', periods=100, freq='D')
    })
    st.info("Using sample data")
else:
    st.warning("Please upload a file or use sample data")
    st.stop()

# Main content
if 'df' in locals():
    # Display data
    st.header("Data Preview")
    st.dataframe(df.head())

    # Statistics
    st.header("Statistics")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Data Info")
        st.write(f"Shape: {df.shape}")
        st.write("Columns:", list(df.columns))

    with col2:
        st.subheader("Numerical Summary")
        st.dataframe(df.describe())

    # Visualization
    st.header("Visualizations")

    # Select columns for plotting
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if numeric_cols:
        col1, col2 = st.columns(2)

        with col1:
            # Histogram
            selected_col = st.selectbox(
                "Select column for histogram", numeric_cols)
            fig = px.histogram(df, x=selected_col,
                               title=f"Distribution of {selected_col}")
            st.plotly_chart(fig)

        with col2:
            # Scatter plot
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("X-axis", numeric_cols, key='x')
                y_col = st.selectbox("Y-axis", numeric_cols, key='y')

                if categorical_cols:
                    color_col = st.selectbox(
                        "Color by", [None] + categorical_cols)
                else:
                    color_col = None

                fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                 title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig)

    # Data filtering
    st.header("Data Filtering")

    col1, col2 = st.columns(2)

    with col1:
        if numeric_cols:
            min_val = st.slider(
                "Minimum value",
                float(df[numeric_cols[0]].min()),
                float(df[numeric_cols[0]].max()),
                float(df[numeric_cols[0]].min())
            )

    with col2:
        if numeric_cols:
            max_val = st.slider(
                "Maximum value",
                float(df[numeric_cols[0]].min()),
                float(df[numeric_cols[0]].max()),
                float(df[numeric_cols[0]].max())
            )

    # Apply filter
    filtered_df = df[
        (df[numeric_cols[0]] >= min_val) &
        (df[numeric_cols[0]] <= max_val)
    ]

    st.write(f"Filtered data shape: {filtered_df.shape}")
    st.dataframe(filtered_df)
