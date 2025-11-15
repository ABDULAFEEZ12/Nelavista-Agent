
class QDeveloper:
    def generate_infra(self, task: str):
        """
        Simulate generating AWS infrastructure spec from a task.
        """
        return {
            "service": "Lambda + API Gateway",
            "task_summary": f"Scaffolded infrastructure for: {task}",
            "resources": ["Lambda Function", "API Gateway Endpoint", "S3 Bucket"]
        }
