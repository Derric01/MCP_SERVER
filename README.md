# 🧠 AI Assistant with Gemini, LangChain & MCP (Conceptual Overview)

This repository demonstrates a **minimal AI assistant setup** using **Google’s Gemini API** in Python.  
The current implementation (`app.py`) shows how to make API calls to Gemini, handle **rate limits**, and build a foundation for AI-powered apps.  

Although this repo only has a basic Gemini example, it is designed to be extended later with **LangChain** and **MCP servers** for more advanced features like RAG (Retrieval-Augmented Generation), PDF/CSV ingestion, and multi-agent workflows.  

---

## 🚀 What’s Inside

- `app.py` → connects to **Gemini** (`gemini-2.0-flash`)  
  - Loads API key from `.env`  
  - Handles retries on rate-limit errors  
  - Sends a simple text query to the model  
- `venv/` → Python virtual environment (not tracked on GitHub by default)  

---

## 🧩 Key Concepts (for when you extend this project)

### 🔹 Gemini API (Current)
- Used here as the **LLM backend**.  
- Your `app.py` demonstrates how to interact with Gemini safely (error handling, retries).  

### 🔹 LangChain (Future)
- A framework that simplifies building **AI-powered applications** by:  
  - Chaining prompts together into workflows  
  - Managing **memory** and conversation state  
  - Connecting LLMs to external **data sources** (e.g., PDFs, CSVs, Databases)  
  - Supporting **vector databases** like Chroma for semantic search  

Think of LangChain as the **glue** between your AI model (Gemini) and your data (files, databases, APIs).  

### 🔹 MCP Server (Future)
- **Model Context Protocol (MCP)** is an emerging standard that lets LLMs securely connect to external tools and services.  
- Example: An MCP server can let your model query **files, databases, or APIs** in real-time.  
- This makes your AI assistant **not just smart, but also connected** to your real-world data and applications.  

---

## 📂 Roadmap (Planned Extensions)

1. ✅ **Gemini integration** (done in `app.py`)  
2. 🔜 **LangChain integration** → for chaining prompts & connecting to data  
3. 🔜 **Chroma or another vector DB** → to store embeddings from PDFs/CSVs  
4. 🔜 **MCP server support** → to let the AI talk to tools/APIs securely  

---

## ⚡ Usage

1. Clone repo & set up env:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
