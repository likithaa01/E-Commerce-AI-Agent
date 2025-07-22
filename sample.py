import ollama

prompt = """
Convert this question to an SQL query:
Question: Which product had the highest CPC?
Database Schema:
Table ad_sales_metrics(product_id, clicks, cost_per_click, ad_spend, ...)
"""
response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
print(response['message']['content'])
