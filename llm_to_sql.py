import ollama
import sqlite3
import pandas as pd


DB_PATH = "ecommerce.db"


def query_llm_for_sql(question: str) -> str:
    """
    Ask Mistral 7B (via Ollama) to generate SQL based on the question and schema.
    """

    schema = """
    Tables:

    1. ad_sales_metrics(
        date,
        item_id,
        ad_sales,
        impressions,
        ad_spend,
        clicks,
        units_sold
    )

    2. total_sales_metrics(
        date,
        item_id,
        total_sales,
        total_units_ordered
    )

    3. eligibility_table(
        eligibility_datetime_utc,
        item_id,
        eligibility,
        message
    )
    """

    prompt = f"""
    You are an SQL expert. Always output only the SQL query without explanation or formatting.

    Schema:
    {schema}

    Examples:
    Q: What is my total sales?
    A: SELECT SUM(total_sales) AS total_sales FROM total_sales_metrics;

    Q: Calculate the RoAS (Return on Ad Spend).
    A: SELECT SUM(total_sales)/SUM(ad_spend) AS RoAS
       FROM total_sales_metrics t
       JOIN ad_sales_metrics a ON t.item_id = a.item_id;

    Q: Which product had the highest CPC (Cost Per Click)?
    A: SELECT item_id, (ad_spend / NULLIF(clicks, 0)) AS cpc
       FROM ad_sales_metrics
       ORDER BY cpc DESC
       LIMIT 1;

    Q: Which products are not eligible?
    A: SELECT item_id FROM eligibility_table WHERE eligibility != 'Yes';

    Now, convert this question into an SQL query:
    Q: {question}
    A:
    """

    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
    sql_query = response['message']['content'].strip()

    if sql_query.startswith("```"):
        sql_query = sql_query.split("```")[1]
        sql_query = sql_query.replace("sql", "").strip()

    return sql_query


def run_sql_query(sql_query: str):
    """
    Run the SQL query on ecommerce.db and return results as a Pandas DataFrame.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        return f"Error executing SQL: {e}"


if __name__ == "__main__":
    question = "Which product had the highest CPC?"
    
    sql = query_llm_for_sql(question)
    print("Generated SQL Query:\n", sql)

    result = run_sql_query(sql)
    print("\nQuery Result:\n", result)
