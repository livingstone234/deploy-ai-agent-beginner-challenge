from .llms import get_openai_llm
from .schemas import EmailMessageSchema

def genearte_email_message(query: str) -> EmailMessageSchema:
    llm_base = get_openai_llm()
    llm = llm_base.with_structured_output(EmailMessageSchema, method="json_mode")

    messages = [
        ("system", """You are a helpful assistant for research and composing plaintext emails. 
        Respond ONLY with a valid JSON object with these exact keys:
        - subject: string
        - contents: string  
        - invalid_request: boolean (true if the request is inappropriate, false otherwise)
        
        Always set invalid_request to true or false, never null."""),
        ("human", f"{query} Plaintext only, no markdown.")
    ]
    response = llm.invoke(messages)
    return response