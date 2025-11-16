from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any
import time

# Initialize FastAPI app
app = FastAPI()

# Templates folder for HTML
templates = Jinja2Templates(directory="templates")

# Simulated AWS resources
SIMULATED_RESOURCES = ["Lambda Function", "API Gateway Endpoint", "S3 Bucket"]

# Request models
class TaskRequest(BaseModel):
    text: str

class StoryRequest(BaseModel):
    task: str
    infra: Dict[str, Any]
    execution: Dict[str, Any]

# Landing page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to run agent
@app.post("/agent")
async def run_agent(req: TaskRequest):
    task = req.text

    # Simulate reasoning
    reasoning = f"Analyzed task: '{task}' and created an execution plan."

    # Simulate infrastructure plan
    infra_plan = {
        "service": "Lambda + API Gateway",
        "task_summary": f"Scaffolded infrastructure for: {task}",
        "resources": SIMULATED_RESOURCES
    }

    # Simulate execution
    executed_resources = []
    for res in SIMULATED_RESOURCES:
        time.sleep(0.3)
        executed_resources.append(res)

    execution = {
        "status": "success",
        "executed_resources": executed_resources,
        "message": f"Deployed {len(executed_resources)} resources successfully."
    }

    return JSONResponse(
        {"result": {"task": task, "reasoning": reasoning, "infra_plan": infra_plan, "execution": execution}}
    )

# Endpoint to generate story from task and infra
@app.post("/generate_story")
async def generate_story(req: StoryRequest):
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

    return JSONResponse({"story": story})
