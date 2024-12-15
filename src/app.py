from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect, WebSocket

import json
import os
from crewai import Crew
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq

from agents import agents
from utils.get_json import extract_json
from tasks import tasks

load_dotenv(find_dotenv())

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm_8b = ChatGroq(model="llama3-8b-8192", temperature=0)
llm_70b = ChatGroq(model="llama3-70b-8192", temperature=0)


app = FastAPI()
TASK_RESULTS = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def process_and_send_tasks(url: str):
    """
    Process tasks for the given URL and send their results via WebSocket.

    Args:
        url (str): The URL to evaluate.
    """

    llm_agents = agents(llm_8b, llm_70b)
    llm_tasks = tasks(llm_8b, llm_70b, url)

    crew = Crew(
        agents=llm_agents,
        tasks=llm_tasks,
        verbose=1,
    )

    crew.kickoff()
    message = {}
    for i, task in enumerate(llm_tasks):
        task_output = task.output.result
        task_name = task.name
        print("TASK OUTPUT: ", task_output)
        response = extract_json(task_output)
        print("TASK_OUTPUT_PARSED: ", response)
        message[task_name] = json.loads(response)

    print("OUTPUT: \n")
    print(message)
    return json.dumps(message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        json_data = await websocket.receive_json()
        print(json_data)
        response = await process_and_send_tasks(json_data.get("url"))
        await websocket.send_json(response)

