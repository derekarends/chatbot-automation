"""
This tool allows agents to interact with the Doc Api
and operate on a Doc instance.
"""

from pydantic import Field

from langchain.tools.base import BaseTool
from doc_api import DocApiWrapper


class DocTool(BaseTool):
    api_wrapper: DocApiWrapper = Field(default_factory=DocApiWrapper)
    mode: str
    name = ""
    description = ""

    def _run(self, instructions: str | None) -> str:
        """Use the Doc API to run an operation."""
        return self.api_wrapper.run(self.mode, instructions)

    async def _arun(self, _: str) -> str:
        """Use the Doc API to run an operation."""
        raise NotImplementedError("DocTool does not support async")
