class Modes:
    READ_EMAIL_FROM = 'read_email_from'
    SEND_EMAIL = 'send_email'


READ_EMAIL_FROM = """
    This tool is useful when you need to read an email from an email address in an email inbox.
    The input for this tool will be a dictionary specifying the fields of the email inbox, and will be passed into the `read_email_from` function.
    For example, to read an email from an email inbox, you would pass in the following string:
    {{ "from": "derekarends23@gmail.com" }}

    The output off this tool will be a dictionary, where each dictionary represents a message in the format of 
    {{ "subject": "a subject", "body": "a body" }}
    """

SEND_EMAIL = """
    This tool is useful when you need to send an email message.
    The input for this tool will be a dictionary specifying the fields of the email message, and will be passed into the `send_email` function.
    For example, to send a message with the subject "hello world" and body "hello world", you would pass in the following string:
    {{ "to": "derekdemo23@gmail.com", "subject": "hello world", "body": "hello world" }}
    """
