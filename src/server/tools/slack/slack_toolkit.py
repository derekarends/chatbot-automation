"""Slack Toolkit."""

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from .slack_tool import SlackTool
from .slack_api import SlackApiWrapper


class SlackToolKit(BaseToolkit):
    """Slack Toolkit."""

    tools: list[BaseTool] = []

    @classmethod
    def from_slack_api_wrapper(cls, slack_api_wrapper: SlackApiWrapper) -> "SlackToolKit":
        operations = slack_api_wrapper.list_operations()
        tools = [
            SlackTool(
                name=operation["name"],
                description=operation["description"],
                mode=operation["mode"],
                api_wrapper=slack_api_wrapper,
            )
            for operation in operations
        ]
        return cls(tools=tools)

    def get_tools(self) -> list[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
