import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain.prompts import PromptTemplate

from schema import (
    ConversationRequest,
    ConversationResponse,
    SearchResult,
    BaseMessage,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    LoadRequest
)


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/conversation", response_model=ConversationResponse, status_code=200)
def conversation(request: ConversationRequest):
    search_results: list[SearchResult] = search(
        request.message.text, request.collection_name)

    conversation: list[BaseMessage] = [
        SystemMessage(content="You are a helpful assistant.")
    ]

    for prev_message in request.history:
        prev_text = prev_message.text or ""
        if prev_message.is_chat_owner:
            conversation.append(UserMessage(content=prev_text))
        else:
            conversation.append(AssistantMessage(content=prev_text))

    conversation.append(UserMessage(
        content=create_prompt(request.message, search_results)))

    print(conversation)
    return ConversationResponse(response=request.message.text, tool="test")


def search(message: str, collection_name: str) -> list[str]:
    return ["This is a search result"]


def create_prompt(message: str, context: list[str]) -> str:
    template = """
      Answer the question, first consider the information after --- or the chat history.

      QUESTION:
      {message}

      ---
      {context}
      """

    prompt_template = PromptTemplate(
        input_variables=["message", "context"],
        template=template
    )
    return prompt_template.format(message=message, context="\n".join(context))
