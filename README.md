# Chatbot Automation

This repo is to demonstrate how to use Langchain with custom tools on a chatbot interface to automat tasks for a given user.

## To Start

- Clone Repo
- Create a virtual environment
  - Run `python3 -m venv .venv`

### To run server

Navigate to `src/server`

- Run `pip install -r requirements.txt`
- Run `uvicorn main:app --reload`

### To run UI

Nagivate to `src/frontend`

- Run `npm install`
- Run `npm run dev`
- Navigate to `http://localhost:5173`
