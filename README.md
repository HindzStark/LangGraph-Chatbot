# LangGraph + Streamlit Chatbot Variants

This project contains multiple Streamlit chatbot frontends backed by LangGraph:

- Basic chat UI
- Streaming response UI
- Multi-thread conversation UI
- SQLite-persisted conversation UI

## Project Structure

- `1_streamlit_frontend.py` - basic chat frontend
- `2_streamlit_frontend_stream.py` - streaming output frontend
- `3_streamlit_frontend_threading.py` - in-memory multi-thread conversations
- `4_streamlit_database_frontend.py` - database-backed multi-thread conversations
- `langgraph_backend.py` - LangGraph backend with in-memory checkpointing
- `langraph_backend_database.py` - LangGraph backend with SQLite checkpointing
- `requirements.txt` - Python dependencies

## Prerequisites

- Python 3.11+
- OpenAI API key

## Setup

1. (Optional) create and activate a virtual environment:

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

   Optional for LangSmith tracing:

   ```env
   LANGCHAIN_API_KEY=your_langsmith_api_key
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=chatbot
   ```

## Run

Run one frontend at a time:

```bash
streamlit run 1_streamlit_frontend.py
```

```bash
streamlit run 2_streamlit_frontend_stream.py
```

```bash
streamlit run 3_streamlit_frontend_threading.py
```

```bash
streamlit run 4_streamlit_database_frontend.py
```

## Notes

- `langgraph_backend.py` uses `InMemorySaver`, so history is not persisted across restarts.
- `langraph_backend_database.py` uses `SqliteSaver` and writes to `chatbot.db`.
- In the database frontend, previous thread IDs are restored from SQLite checkpoints.
