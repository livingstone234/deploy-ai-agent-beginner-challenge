from langchain_core.tools import tool

from ..myemailer.sender import send_mail
from ..myemailer.inbox_reader import read_inbox
from .services import generate_email_message

@tool
def send_me_email(subject: str, content: str, to_email: str = "myapp2821@gmail.com") -> str:
    """
    Send an email to an email address with the recipient address as your target with a subject and content.

    Arguments:
    - subject: str - Text subject of the email
    - content: str - Text body content of the email
    - to_email: str - Recipient's email address 
    """

    try: 
        send_mail(subject=subject, content=content, to_email=to_email)
    except:
        return "Not sent"
    return "Sent email"

@tool
def get_unread_emails(hours_ago=24) -> str:
    """Read all emails from my inbox within the last N hours.
    
    Arguments:
    - hours_ago: int = 24 - A number of hours ago to retrieve in the inbox

    Returns:
    A string of emails separated by a line "----"
    """

    try:
        emails = read_inbox(hours_ago=24, verbose=False)
    except:
        return "Error getting latest emails"
    
    cleaned = []
    for email in emails:
        data = email.copy()
        if "html_body" in data:
            data.pop('html_body')
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t{v}"
        cleaned.append(msg)
    return "\n-----\n".join(cleaned)

@tool
def research_email(query: str):
    """
    Perform research based on the query

    Arguments: 
    - query: str - Topic of research 
    """
    message = generate_email_message(query)
    msg = f"Subject: {message.subject}.\nBody: {message.contents}"
    return msg