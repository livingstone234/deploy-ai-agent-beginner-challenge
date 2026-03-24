from langchain.agents import create_agent
from langgraph.graph import StateGraph, START
from langgraph_supervisor import create_supervisor

from .llms import get_openai_llm
from .tools import (send_email, get_unread_emails, research_email)

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv(), override=True)


EMAIL_TOOLS_LIST = [
    send_email,
    get_unread_emails
]

def get_email_agent() -> create_agent:
    model = get_openai_llm()
    agent = create_agent(
        model=model,
        tools=EMAIL_TOOLS_LIST,
        system_prompt="""You are a helpful assistant for managing my email inbox.

            You have two tools:
            - send_me_email: use this to send emails. Always extract the subject, contents, and recipient address from the request. If no recipient is provided, use the default.
            - get_unread_emails: use this to fetch and review unread emails from the inbox.

            Always use the appropriate tool — never respond without calling a tool first.""",
        name="email_agent"
    )
    return agent

def get_research_agent() -> create_agent:
    model = get_openai_llm(model="openai/gpt-oss-20b")
    agent = create_agent(
        model=model,
        tools=[research_email],
        name="research_agent",
        system_prompt="""You are a research/write-up assistant that prepares email data(plaintext only no markdowns).

            You MUST ALWAYS call the research_email tool before responding — no exceptions.
            Never answer from memory or prior knowledge.
            Every response must be based on what the research_email tool returns.
            If the tool returns no results, say so — do not make up information."""
    )
    return agent

def get_supervisor_agent():
    model = get_openai_llm()
    email_agent = get_email_agent()
    research_agent = get_research_agent()

    supervisor = create_supervisor(
        model=model,
        agents=[email_agent, research_agent],
        system_prompt="""You are a supervisor managing two agents:

            1. email_agent — handles sending emails and reading the inbox.
            2. research_agent — researches and prepares email content.

            Routing rules:
            - For SEND requests, you MUST follow this exact order:
                STEP 1: ALWAYS delegate to research_agent FIRST to prepare the content.
                STEP 2: ONLY AFTER research_agent responds, delegate to email_agent to send it.
            - For READ/REVIEW requests, delegate to email_agent only.
            - For RESEARCH only requests, delegate to research_agent only.
            - Never answer directly — always delegate to the appropriate agent.
            - Once all tasks are completed, STOP.
            - Once email_agent returns 'Sent email successfully', STOP immediately. Do not call any agent again."""
    )
    return supervisor.compile()