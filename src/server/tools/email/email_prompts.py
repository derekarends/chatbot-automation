class Modes:
    SEARCH_EMAIL_FROM = 'search_email_from'
    SEARCH_EMAIL_SUBJECT = 'search_email_subject'
    SEND_EMAIL = 'send_email'


SEARCH_EMAIL_FROM = """
    This tool is useful when you need to search for an email based on the from line.
    The input for this tool will be a dictionary specifying the from address to search for, and will be passed into the `search_email_from` function.
    For example, to search for an email from an email inbox, you would pass in the following string:
    {{ "from": "derek@gmail.com" }}

    The output off this tool will be a dictionary, where each dictionary represents a message in the format of 
    {{ "subject": "a subject", "body": "a body" }}
    """

SEARCH_EMAIL_SUBJECT = """
    This tool is useful when you need to search for an email based on subject line.
    The input for this tool will be a dictionary specifying the subject to search for, and will be passed into the `search_email_subject` function.
    For example, to read an email's subject line, you would pass in the following string:
    {{ "subject": "Top gear" }}

    The output off this tool will be a dictionary, where each dictionary represents a message in the format of 
    {{ "from": "derek@gmail.com", "subject": "a subject", "body": "a body" }}
    """

SEND_EMAIL = """
    This tool is useful when you need to send an email message.
    The input for this tool will be a dictionary specifying the fields of the email message, and will be passed into the `send_email` function.
    For example, to send a message with the subject "hello world" and body "hello world", you would pass in the following string:
    {{ "to": "derekdemo23@gmail.com", "subject": "hello world", "body": "hello world" }}
    """
