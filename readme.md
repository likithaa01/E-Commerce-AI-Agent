\# 🛍️ E-commerce Data AI Agent

This project builds an \*\*AI agent\*\* that answers natural language
questions about e-commerce datasets. It uses: - \*\*Mistral 7B (via
Ollama)\*\* for converting user questions into SQL queries. -
\*\*SQLite\*\* for storing and querying data. - \*\*FastAPI\*\* as the
backend API. - \*\*Streamlit\*\* as the frontend UI (bonus feature). -
\*\*Plotly\*\* for generating interactive charts.

\-\--

\## \*\*Features\*\* - \*\*Natural Language to SQL\*\*: Ask any question
about sales, ads, and product eligibility. - \*\*Automatic SQL
Execution\*\*: Queries the SQLite database for answers. - \*\*API
Endpoint (\`/ask\`)\*\*: Accepts questions and returns SQL + results as
JSON. - \*\*Frontend UI (Streamlit)\*\*: Provides a web-based interface
with:  - Query responses  - Typing effect for LLM responses  - Charts
for trend-based queries (bonus) - \*\*Bonus\*\*:  - Graphs/visuals for
certain queries.  - Simulated real-time \"typing\" effect.

\-\--

\## \*\*Project Structure\*\* ├── app.py \# FastAPI backend ├──
frontend.py \# Streamlit frontend ├── load_data.py \# Loads CSV files
into SQLite ├── ecommerce.db \# SQLite database (created after running
load_data.py) ├── data/ │ ├── Product-Level Total Sales and Metrics
(mapped).csv │ ├── Product-Level Ad Sales and Metrics (mapped).csv │ └──
Product-Level Eligibility Table (mapped).csv ├── requirements.txt └──
README.md

\-\--

\## \*\*Prerequisites\*\* - Python 3.9+ -
\[Ollama\](https://ollama.com/download) (for running Mistral 7B
locally) - Installed Mistral model: \`\`\`bash ollama pull mistral

Installation Clone this repository:

bash Copy code git clone \<your-repo-url\> cd \<your-repo-folder\>
Create a virtual environment and activate it:

bash Copy code python -m venv venv source venv/bin/activate \# For
Mac/Linux venv\\Scripts\\activate \# For Windows Install dependencies:

bash Copy code pip install -r requirements.txt Place your CSV files
(ad_sales.csv, total_sales.csv, eligibility.csv) inside the data/
folder.

Run the data loader to create ecommerce.db:

bash Copy code python load_data.py 🛠️ Running the Project ✅ Start
FastAPI Backend bash Copy code python app.py The backend will start at:
http://127.0.0.1:8000

🧪 Test the API with curl: bash Copy code curl -X POST
\"http://127.0.0.1:8000/ask\" \\ -H \"Content-Type: application/json\"
\\ -d \"{\\\"question\\\":\\\"What is my total sales?\\\"}\" 🖥️ Start
Streamlit Frontend Open another terminal and run:

bash Copy code streamlit run streamlit_app.py The frontend will start
at: http://localhost:8501
