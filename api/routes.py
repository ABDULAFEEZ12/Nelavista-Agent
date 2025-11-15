
from fastapi import APIRouter
from agent.core import NelavistaAgent

router = APIRouter()
agent = NelavistaAgent()

@router.post("/agent")
def run_agent(task: dict):
    """
    Expects JSON: {"text": "Your task description here"}
    """
    text = task.get("text", "")
    if not text:
        return {"error": "No task provided"}
    result = agent.execute_task(text)
    return {"result": result}
