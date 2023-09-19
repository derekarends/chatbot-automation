from pydantic import Field

from langchain.tools.base import BaseTool
from email_api import EmailApiWrapper


class EmailTool(BaseTool):
    api_wrapper: EmailApiWrapper = Field(default_factory=EmailApiWrapper)
    mode: str
    name = ""
    description = ""

    def _run(self, instructions: str | None) -> str:
        """Use the Email API to run an operation."""
        return self.api_wrapper.run(self.mode, instructions)

    async def _arun(self, _: str) -> str:
        """Use the Email API to run an operation."""
        raise NotImplementedError("EmailTool does not support async")
