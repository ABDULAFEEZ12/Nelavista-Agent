from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time

app = FastAPI()

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
    # Simulate reasoning
    reasoning = f"Analyzed task: '{task}' and created an execution plan."
    
    # Simulate infrastructure plan
    infra_plan = {
        "service": "Lambda + API Gateway",
        "task_summary": f"Scaffolded infrastructure for: {task}",
        "resources": SIMULATED_RESOURCES
    }
    
    # Simulate execution with delay
    executed_resources = []
    for res in SIMULATED_RESOURCES:
        time.sleep(0.3)
        executed_resources.append(res)
    
    execution = {
        "status": "success",
        "executed_resources": executed_resources,
        "message": f"Deployed {len(executed_resources)} resources successfully."
    }
    
    return {"result": {"task": task, "reasoning": reasoning, "infra_plan": infra_plan, "execution": execution}}

@app.post("/generate_story")
def generate_story(req: StoryRequest):
    task = req.task
    infra = req.infra
    execution = req.execution
    # Simple story generation
    story = (
        f"The task '{task}' was executed successfully.\n"
        f"The following infrastructure was used: {', '.join(infra['resources'])}.\n"
        f"Execution summary: {execution['message']}.\n"
        "Each component plays a crucial role: "
        "Lambda handles backend logic, API Gateway exposes endpoints, and S3 stores data securely.\n"
        "This setup ensures scalability and smooth operation for future expansions."
    )
    return {"story": story}
