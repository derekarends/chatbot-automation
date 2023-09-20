from agent import Agent
from schema import (
    ConversationRequest,
    ConversationResponse
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import os


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
    agent = Agent()
    resp = agent.run(request.message.text)
    print(resp)
    return ConversationResponse(response=resp)
