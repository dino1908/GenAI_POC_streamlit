# Streamlit + LangChain + Gemini POC

A small proof-of-concept app that showcases how to wire up:

- **Streamlit** for a simple, interactive frontend  
- **LangChain** as the LLM orchestration layer  
- **Gemini** as the underlying LLM  
- **SQLite** as a lightweight local database  
- A **Prompt Manager** to easily tweak prompts without changing core code  

The demo use case is a **Stock Suggester**: you enter some basic inputs, and the app uses Gemini (via LangChain) plus your prompt configuration to suggest stocks (for learning/demo purposes only – not financial advice).

---

## Features

- 🧩 **Modular architecture**  
  Separate modules for UI, LLM logic, database access, and prompt management.

- 🧠 **LLM powered by Gemini via LangChain**  
  Uses LangChain wrappers around Gemini so you can swap models or chains easily.

- 📝 **Prompt Manager**  
  Central place to manage prompts. Update prompts or add variants without touching core logic.

- 💾 **SQLite backing store**  
  Simple local DB for saving queries, responses, or any experiment data.

- 📊 **Stock Suggester demo**  
  Example flow that takes user inputs and returns a model-generated stock suggestion.

---

## Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)  
- **LLM Orchestration:** [LangChain](https://python.langchain.com/)  
- **LLM Provider:** Google **Gemini**  
- **Database:** SQLite  
- **Language:** Python

---

