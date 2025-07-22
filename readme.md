# 🛍️ E-commerce Data AI Agent

This project builds an **AI agent** that answers natural language questions about e-commerce datasets.  
It uses:
- **Mistral 7B (via Ollama)** for converting user questions into SQL queries.
- **SQLite** for storing and querying data.
- **FastAPI** as the backend API.
- **Streamlit** as the frontend UI (bonus feature).
- **Plotly** for generating interactive charts.

---

## **Features**
- **Natural Language to SQL**: Ask any question about sales, ads, and product eligibility.
- **Automatic SQL Execution**: Queries the SQLite database for answers.
- **API Endpoint (`/ask`)**: Accepts questions and returns SQL + results as JSON.
- **Frontend UI (Streamlit)**: Provides a web-based interface with:
  - Query responses
  - Typing effect for LLM responses
  - Charts for trend-based queries (bonus)
- **Bonus**:
  - Graphs/visuals for certain queries.
  - Simulated real-time "typing" effect.

---

## **Running the Project**
**Start FastAPI Backend**
```bash
python app.py
```
- The backend will start at: HTTP://127.0.0.1:8000

**Start Streamlit Frontend**
- Open another terminal and run:
```bash
streamlit run frontend.py
```
- The frontend will start at: HTTP://localhost:8501 

---
