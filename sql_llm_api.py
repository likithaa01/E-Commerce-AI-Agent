from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
import ollama
import uvicorn

DB_PATH = "ecommerce.db"
MODEL_NAME = "mistral"  

SCHEMA = """
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

PROMPT_TEMPLATE = f"""
You are an SQL expert. Always output only the SQL query without explanations or formatting.

Schema:
{SCHEMA}

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
"""

app = FastAPI(title="E-Commerce Data AI Agent")

class Question(BaseModel):
    question: str

def query_llm_for_sql(question: str) -> str:
    prompt = PROMPT_TEMPLATE + f"\n\nNow, convert this question into an SQL query:\nQ: {question}\nA:"
    response = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])
    sql_query = response['message']['content'].strip()

    if sql_query.startswith("```"):
        sql_query = sql_query.split("```")[1]
        sql_query = sql_query.replace("sql", "").strip()

    return sql_query

def run_sql_query(sql_query: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df.to_dict(orient="records")  
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
def ask_question(q: Question):
    sql = query_llm_for_sql(q.question)

    result = run_sql_query(sql)

    return {
        "question": q.question,
        "generated_sql": sql,
        "result": result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
