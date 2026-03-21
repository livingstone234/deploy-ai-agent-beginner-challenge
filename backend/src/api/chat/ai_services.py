import os
from langchain_groq import ChatGroq

from pydantic import BaseModel, Field

class EmailMessage(BaseModel):
    subject: str
    contents: str
    invalid_request: bool = Field(default=False)

GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_GROQ_MODEL_NAME = os.environ.get("OPENAI_GROQ_MODEL_NAME")

if not GROQ_API_KEY:
    raise NotImplementedError("`GROQ_API_KEY` not set.")

openai_params = {
    "model":OPENAI_GROQ_MODEL_NAME,
    "api_key":GROQ_API_KEY
}

if GROQ_BASE_URL:
    openai_params['base_url'] = GROQ_BASE_URL

llm_base = ChatGroq(**openai_params)

llm = llm_base.with_structured_output(EmailMessage, method="json_mode")

messages = [
    ("system", """You are a helpful assistant for research and composing plaintext emails. 
    Respond ONLY with a valid JSON object with these exact keys:
    - subject: string
    - contents: string  
    - invalid_request: boolean (true if the request is inappropriate, false otherwise)
    
    Always set invalid_request to true or false, never null."""),
    ("human", "Create an email message about the benefits of coffee. Plaintext only, no markdown.")
]
response = llm.invoke(messages)

print(response)