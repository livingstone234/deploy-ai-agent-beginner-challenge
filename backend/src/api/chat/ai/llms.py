import os
from langchain_groq import ChatGroq


GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL") or "https://api.groq.com"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_GROQ_MODEL_NAME = os.environ.get("OPENAI_GROQ_MODEL_NAME") or "openai/gpt-oss-120b"
# OPENAI_GROQ_MODEL_NAME = os.environ.get("OPENAI_GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
if not GROQ_API_KEY:
    raise NotImplementedError("`GROQ_API_KEY` not set.")

def get_openai_llm(model=OPENAI_GROQ_MODEL_NAME) -> ChatGroq:
    openai_params = {
        "model":model,
        "api_key":GROQ_API_KEY
    }
    if GROQ_BASE_URL:
        openai_params['base_url'] = GROQ_BASE_URL
        
    return ChatGroq(**openai_params)
