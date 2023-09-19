# Chatbot Automation

This repo is to demonstrate how to use Langchain with custom tools on a chatbot interface to automat tasks for a given user.

## To Start

- Clone Repo
- Create a virtual environment
  - Run `python3 -m venv .venv`

### Setting up PGVector

- Run `docker-compose up -d` in root directory
- Connect to `langchain` database with username and password from `docker-compose.yml`
- Run `create extension if not exists vector;` to enable vector extension

### To run server

Navigate to `src/server`

- Run `pip install -r requirements.txt`
- Run `uvicorn main:app --reload`

### To run UI

Nagivate to `src/frontend`

- Run `npm install`
- Run `npm run dev`
- Navigate to `http://localhost:5173`

### To allow email tool to work

- Must enabled Google API for Gmail
- Create OAuth 2.0 Client ID
- Give scope to read and send emails
- Download credentials.json
