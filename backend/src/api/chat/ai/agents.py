from langchain.agents import create_agent

from .llms import get_openai_llm
from .tools import (send_me_email, get_unread_emails, research_email)

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv(), override=True)


EMAIL_TOOLS_LIST = [
    send_me_email,
    get_unread_emails
]

def get_email_agent() -> create_agent:
    model = get_openai_llm()
    agent = create_agent(
        model=model,
        tools=EMAIL_TOOLS_LIST,
        system_prompt="You are a helpful assistant for managing my email inbox for sending, and reviewing emails.",
        name="email_agent"
    )
    return agent

def get_research_agent() -> create_agent:
    model = get_openai_llm()
    agent = create_agent(
        model=model,
        tools=[research_email],
        name="research_agent",
        system_prompt="""You are a research assistant that prepares email data.

            You MUST ALWAYS call the research_email tool before responding — no exceptions.
            Never answer from memory or prior knowledge.
            Every response must be based on what the research_email tool returns.
            If the tool returns no results, say so — do not make up information."""
    )
    return agent