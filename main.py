from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time

app = FastAPI()

# Landing page so Render root URL works
@app.get("/")
def root():
    return {"message": "Nelavista AGENT is running. Use POST /agent to execute tasks."}

# Simulated AWS services
SIMULATED_RESOURCES = ["Lambda Function", "API Gateway Endpoint", "S3 Bucket"]

class TaskRequest(BaseModel):
    text: str

class StoryRequest(BaseModel):
    task: str
    infra: Dict[str, Any]
    execution: Dict[str, Any]

@app.post("/agent")
def run_agent(req: TaskRequest):
    task = req.text

    reasoning = f"Analyzed task: '{task}' and created an execution plan."

    infra_plan = {
        "service": "Lambda + API Gateway",
        "task_summary": f"Scaffolded infrastructure for: {task}",
        "resources": SIMULATED_RESOURCES
    }

    executed_resources = []
    for res in SIMULATED_RESOURCES:
        time.sleep(0.3)
        executed_resources.append(res)

    execution = {
        "status": "success",
        "executed_resources": executed_resources,
        "message": f"Deployed {len(executed_resources)} resources successfully."
    }

    return {
        "result": {
            "task": task,
            "reasoning": reasoning,
            "infra_plan": infra_plan,
            "execution": execution
        }
    }

@app.post("/generate_story")
def generate_story(req: StoryRequest):
    task = req.task
    infra = req.infra
    execution = req.execution

    story = (
        f"The task '{task}' was executed successfully.\n"
        f"Infrastructure used: {', '.join(infra['resources'])}.\n"
        f"Execution summary: {execution['message']}.\n"
        "Lambda handled logic, API Gateway exposed the endpoint, and S3 provided storage.\n"
        "This architecture ensures scalability and smooth operations."
    )
    return {"story": story}
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time

app = FastAPI()

# Landing page so Render root URL works
@app.get("/")
def root():
    return {"message": "Nelavista AGENT is running. Use POST /agent to execute tasks."}

# Simulated AWS services
SIMULATED_RESOURCES = ["Lambda Function", "API Gateway Endpoint", "S3 Bucket"]

class TaskRequest(BaseModel):
    text: str

class StoryRequest(BaseModel):
    task: str
    infra: Dict[str, Any]
    execution: Dict[str, Any]

@app.post("/agent")
def run_agent(req: TaskRequest):
    task = req.text

    reasoning = f"Analyzed task: '{task}' and created an execution plan."

    infra_plan = {
        "service": "Lambda + API Gateway",
        "task_summary": f"Scaffolded infrastructure for: {task}",
        "resources": SIMULATED_RESOURCES
    }

    executed_resources = []
    for res in SIMULATED_RESOURCES:
        time.sleep(0.3)
        executed_resources.append(res)

    execution = {
        "status": "success",
        "executed_resources": executed_resources,
        "message": f"Deployed {len(executed_resources)} resources successfully."
    }

    return {
        "result": {
            "task": task,
            "reasoning": reasoning,
            "infra_plan": infra_plan,
            "execution": execution
        }
    }

@app.post("/generate_story")
def generate_story(req: StoryRequest):
    task = req.task
    infra = req.infra
    execution = req.execution

    story = (
        f"The task '{task}' was executed successfully.\n"
        f"Infrastructure used: {', '.join(infra['resources'])}.\n"
        f"Execution summary: {execution['message']}.\n"
        "Lambda handled logic, API Gateway exposed the endpoint, and S3 provided storage.\n"
        "This architecture ensures scalability and smooth operations."
    )
    return {"story": story}
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time

app = FastAPI()

# Landing page so Render root URL works
@app.get("/")
def root():
    return {"message": "Nelavista AGENT is running. Use POST /agent to execute tasks."}

# Simulated AWS services
SIMULATED_RESOURCES = ["Lambda Function", "API Gateway Endpoint", "S3 Bucket"]

class TaskRequest(BaseModel):
    text: str

class StoryRequest(BaseModel):
    task: str
    infra: Dict[str, Any]
    execution: Dict[str, Any]

@app.post("/agent")
def run_agent(req: TaskRequest):
    task = req.text

    reasoning = f"Analyzed task: '{task}' and created an execution plan."

    infra_plan = {
        "service": "Lambda + API Gateway",
        "task_summary": f"Scaffolded infrastructure for: {task}",
        "resources": SIMULATED_RESOURCES
    }

    executed_resources = []
    for res in SIMULATED_RESOURCES:
        time.sleep(0.3)
        executed_resources.append(res)

    execution = {
        "status": "success",
        "executed_resources": executed_resources,
        "message": f"Deployed {len(executed_resources)} resources successfully."
    }

    return {
        "result": {
            "task": task,
            "reasoning": reasoning,
            "infra_plan": infra_plan,
            "execution": execution
        }
    }

@app.post("/generate_story")
def generate_story(req: StoryRequest):
    task = req.task
    infra = req.infra
    execution = req.execution

    story = (
        f"The task '{task}' was executed successfully.\n"
        f"Infrastructure used: {', '.join(infra['resources'])}.\n"
        f"Execution summary: {execution['message']}.\n"
        "Lambda handled logic, API Gateway exposed the endpoint, and S3 provided storage.\n"
        "This architecture ensures scalability and smooth operations."
    )
    return {"story": story}
