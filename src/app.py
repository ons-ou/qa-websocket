from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

import json
import os
from crewai import Crew
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq

from agents import agents
from tasks import tasks

load_dotenv(find_dotenv())

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm_8b = ChatGroq(model="groq/llama3-8b-8192", temperature=0)
llm_70b = ChatGroq(model="groq/llama3-70b-8192", temperature=0)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_feedback(url: str):

    llm_agents = agents(llm_8b, llm_70b)
    llm_tasks = await tasks(llm_8b, llm_70b, url)

    crew = Crew(
        agents=llm_agents,
        tasks=llm_tasks,
        verbose=1,
    )

    await crew.kickoff_async()

    message = {}
    for i, task in enumerate(llm_tasks):
        task_output = task.output.json_dict
        task_name = task.name
        print("TASK OUTPUT: ", task_output)
        message[task_name] = task_output

    print("OUTPUT: \n")
    print(message)
    return json.dumps(message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        json_data = await websocket.receive_json()
        print(json_data)
        response = await get_feedback(json_data.get("url"))
        await websocket.send_json(response)

