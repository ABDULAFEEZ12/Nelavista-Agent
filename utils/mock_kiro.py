class Kiro:
    def run_tasks(self, infra_plan: dict):
        """
        Simulate executing tasks in AWS/Kiro.
        """
        return {
            "status": "success",
            "executed_resources": infra_plan.get("resources", []),
            "message": f"Deployed {len(infra_plan.get('resources', []))} resources successfully."
        }

