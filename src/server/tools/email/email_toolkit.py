from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from email_tool import EmailTool
from email_api import EmailApiWrapper


class EmailToolKit(BaseToolkit):
    """Email Toolkit."""

    tools: list[BaseTool] = []

    @classmethod
    def from_api_wrapper(cls, api_wrapper: EmailApiWrapper) -> "EmailToolKit":
        operations = api_wrapper.list_operations()
        tools = [
            EmailTool(
                name=operation["name"],
                description=operation["description"],
                mode=operation["mode"],
                api_wrapper=api_wrapper,
            )
            for operation in operations
        ]
        return cls(tools=tools)

    def get_tools(self) -> list[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
