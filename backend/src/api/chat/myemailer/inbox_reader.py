import os
from gmail_imap_parser import GmailImapParser
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


def read_inbox(hours_ago=24, unread_only=True, verbose=False):
    # Initialize
    parser = GmailImapParser(
        email_address=os.environ.get("EMAIL_ADDRESS"),
        app_password=os.environ.get("EMAIL_PASSWORD")
    )

    # Fetch unread emails from last 24 hours
    emails = parser.fetch_emails(hours=hours_ago, unread_only=unread_only)

    if verbose:
        for email in emails:
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['timestamp']}")
            print("---")
    return emails