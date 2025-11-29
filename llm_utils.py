import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompt_manager import industry_prompt, general_prompt

# 1. Setup

load_dotenv()  # loads GOOGLE_API_KEY from .env

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
)


def build_chain(a):
    if a=="General":
        text = general_prompt
    elif a=="Industry":
        text = industry_prompt
    else:
        text = "You are a helpful assistant"
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", text),
            (
                "human",
                "Conversation so far:\n{history}\n\nUser: {user_input}",
            ),
        ]
    )

    return prompt | llm | StrOutputParser()


def format_history(messages):
    """Turn Streamlit-style history into a plain text transcript."""
    lines = []
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)
