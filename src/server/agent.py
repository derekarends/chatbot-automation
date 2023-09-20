from tools.slack.slack_tool import SlackApiWrapper
from tools.slack.slack_toolkit import SlackToolKit
from tools.email.email_api import EmailApiWrapper
from tools.email.email_toolkit import EmailToolKit
from tools.docs.doc_api import DocApiWrapper
from tools.docs.doc_toolkit import DocToolKit
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["SLACK_BOT_TOKEN"] = os.getenv('SLACK_BOT_TOKEN')


class Agent:
    agent = None

    def __init__(self):
        llm = OpenAI(temperature=.7)

        docs_api = DocApiWrapper()
        docs_toolkit = DocToolKit.from_api_wrapper(docs_api)
        docs_tools = docs_toolkit.get_tools()

        email_api = EmailApiWrapper()
        email_toolkit = EmailToolKit.from_api_wrapper(email_api)
        email_tools = email_toolkit.get_tools()

        slack_api = SlackApiWrapper()
        slack_toolkit = SlackToolKit.from_slack_api_wrapper(slack_api)
        slack_tools = slack_toolkit.get_tools()

        tools = []
        [tools.append(tool) for tool in docs_tools]
        [tools.append(tool) for tool in email_tools]
        [tools.append(tool) for tool in slack_tools]

        self.agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True)

    def run(self, text):
        return self.agent.run(text)
