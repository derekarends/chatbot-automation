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


class SearchResult(BaseModel):
    """Search results from the API."""

    title: str
    content: str
