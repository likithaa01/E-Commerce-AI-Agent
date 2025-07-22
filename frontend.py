import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

FASTAPI_URL = "http://127.0.0.1:8000/ask"  

st.set_page_config(page_title="E-commerce AI Agent", layout="centered")

st.title("🛍️ E-commerce Data AI Agent")
st.write("Ask me anything about your e-commerce data!")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(FASTAPI_URL, json={"question": question})
                if response.status_code == 200:
                    data = response.json()

                    st.subheader("Generated SQL Query:")
                    sql_placeholder = st.empty()
                    for i in range(len(data['generated_sql'])):
                        sql_placeholder.text(data['generated_sql'][:i+1])
                        time.sleep(0.01)

                    st.subheader("Result:")
                    result = data["result"]
                    if isinstance(result, list) and len(result) > 0:
                        df = pd.DataFrame(result)
                        st.dataframe(df)

                        st.write("Columns in DataFrame:", df.columns.tolist())

                        if "date" in df.columns:
                            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                            numeric_cols = [col for col in numeric_cols if col != "date"]

                            if numeric_cols:
                                y_col = numeric_cols[0]  # Pick the first numeric column
                                fig = px.line(df, x="date", y=y_col, title=f"{y_col} Trend")
                                st.plotly_chart(fig)
                            else:
                                st.info("No numeric columns found to plot a graph.")
                        else:
                            st.info("No 'date' column found for plotting a trend graph.")
                    else:
                        st.write(result)
                else:
                    st.error(f"Error connecting to FastAPI backend. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Request failed: {e}")
