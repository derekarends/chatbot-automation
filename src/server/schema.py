from abc import abstractmethod

from pydantic import BaseModel, Field


class LoadRequest(BaseModel):
    """ Load Request object. """

    path: str
    collection_name: str = Field(alias='collectionName')


class ConversationMessage(BaseModel):
    """ Conversation Request object. """

    text: str | None
    is_chat_owner: bool = Field(alias='isChatOwner')


class ConversationRequest(BaseModel):
    """ Conversation Request object. """

    history: list[ConversationMessage]
    message: ConversationMessage
    collection_name: str | None = Field(default=None, alias='collectionName')


class ConversationResponse(BaseModel):
    """ Response from the conversation API. """

    response: str
    tool: str | None = None


class BaseMessage(BaseModel):
    """Open AI Message object."""

    content: str
    name: str | None = None

    @property
    @abstractmethod
    def role(self) -> str:
        """Role of the message, used for serialization."""

    def to_dict(self) -> dict:
        """Converts the message to a dictionary."""

        message_dict = {"role": self.role, "content": self.content}

        if self.name is not None:
            message_dict["name"] = self.name

        return message_dict

    @staticmethod
    def from_dict(_dict: dict) -> "BaseMessage":
        """Converts a dictionary to a message."""

        role = _dict["role"]
        if role == "user":
            return UserMessage(content=_dict["content"], name=_dict.get("name"))
        elif role == "assistant":
            return AssistantMessage(content=_dict["content"], name=_dict.get("name"))
        elif role == "system":
            return SystemMessage(content=_dict["content"], name=_dict.get("name"))
        elif role == "function":
            return FunctionMessage(content=_dict["content"], name=_dict.get("name"))
        else:
            return ChatMessage(content=_dict["content"], role=role, name=_dict.get("name"))


class ChatMessage(BaseMessage):
    """Type of message that is spoken by the chat."""

    @property
    def role(self) -> str:
        """Role of the message, used for serialization."""
        return "chat"


class UserMessage(BaseMessage):
    """Type of message that is spoken by the user."""

    @property
    def role(self) -> str:
        """Role of the message, used for serialization."""
        return "user"


class AssistantMessage(BaseMessage):
    """Type of message that is spoken by the assistant."""

    @property
    def role(self) -> str:
        """Role of the message, used for serialization."""
        return "assistant"


class SystemMessage(BaseMessage):
    """Type of message that is a system message."""

    @property
    def role(self) -> str:
        """Role of the message, used for serialization."""
        return "system"


class FunctionMessage(BaseMessage):
    """Type of message that is a system message."""

    @property
    def role(self) -> str:
        """Role of the message, used for serialization."""
        return "function"


class SearchResult(BaseModel):
    """Search results from the API."""

    title: str
    content: str
