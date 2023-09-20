"""Doc Toolkit."""

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from .doc_tool import DocTool
from .doc_api import DocApiWrapper


class DocToolKit(BaseToolkit):
    """Doc Toolkit."""

    tools: list[BaseTool] = []

    @classmethod
    def from_api_wrapper(cls, api_wrapper: DocApiWrapper) -> "DocToolKit":
        operations = api_wrapper.list_operations()
        tools = [
            DocTool(
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
