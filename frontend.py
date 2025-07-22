import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

FASTAPI_URL = "http://127.0.0.1:8000/ask"  # Ensure FastAPI is running

st.set_page_config(page_title="E-commerce AI Agent", layout="centered")

st.title("🛍️ E-commerce Data AI Agent")
st.write("Ask me anything about your e-commerce data!")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            # Send question to FastAPI backend
            response = requests.post(FASTAPI_URL, json={"question": question})
            if response.status_code == 200:
                data = response.json()

                # Typing effect for SQL
                st.subheader("Generated SQL Query:")
                sql_placeholder = st.empty()
                for i in range(len(data['generated_sql'])):
                    sql_placeholder.text(data['generated_sql'][:i+1])
                    time.sleep(0.01)

                # Display Result
                st.subheader("Result:")
                result = data["result"]
                if isinstance(result, list) and len(result) > 0:
                    df = pd.DataFrame(result)
                    st.dataframe(df)
                    
                    # Plot chart if required
                    if data.get("chart_required", False) and "date" in df.columns and "total_sales" in df.columns:
                        fig = px.line(df, x="date", y="total_sales", title="Sales Trend")
                        st.plotly_chart(fig)
                else:
                    st.write(result)
            else:
                st.error("Error connecting to FastAPI backend.")
