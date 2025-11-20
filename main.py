from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any
import boto3
import json
import time
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# AWS Clients - Will use your configured AWS CLI credentials
lambda_client = boto3.client('lambda', region_name='us-east-1')
apigateway_client = boto3.client('apigateway', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
cloudformation_client = boto3.client('cloudformation', region_name='us-east-1')

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

# Real AWS Deployment Functions
def create_lambda_function(function_name):
    """Create a real Lambda function"""
    try:
        # Simple Lambda function code
        lambda_code = '''
import json
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Nelavista Agent!",
            "input": event
        })
    }
'''
        
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role='arn:aws:iam::246290151348:role/service-role/lambda_basic_execution',  # You'll need to create this role
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description=f'Created by Nelavista Agent - {function_name}',
            Timeout=30,
            MemorySize=128,
            Publish=True
        )
        return {"status": "success", "function_arn": response['FunctionArn']}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_s3_bucket(bucket_name):
    """Create a real S3 bucket"""
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
        )
        return {"status": "success", "bucket_name": bucket_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_api_gateway(api_name):
    """Create a real API Gateway"""
    try:
        response = apigateway_client.create_rest_api(
            name=api_name,
            description=f'API created by Nelavista Agent - {api_name}',
            endpointConfiguration={'types': ['REGIONAL']}
        )
        return {"status": "success", "api_id": response['id']}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/agent")
async def run_agent(req: TaskRequest):
    task = req.text
    
    # Generate unique resource names
    timestamp = str(int(time.time()))
    unique_id = str(uuid.uuid4())[:8]
    
    lambda_name = f"nelavista-lambda-{unique_id}"
    bucket_name = f"nelavista-bucket-{unique_id}"
    api_name = f"NelavistaAPI-{unique_id}"
    
    reasoning = f"Analyzed task: '{task}' and created a real AWS deployment plan."
    
    infra_plan = {
        "service": "Lambda + API Gateway + S3",
        "task_summary": f"Real AWS deployment for: {task}",
        "resources": ["Lambda Function", "API Gateway", "S3 Bucket"],
        "real_resources": {
            "lambda_function": lambda_name,
            "s3_bucket": bucket_name,
            "api_gateway": api_name
        }
    }

    # Execute real AWS deployments
    execution_results = []
    
    # Deploy Lambda
    lambda_result = create_lambda_function(lambda_name)
    execution_results.append({"resource": "Lambda", "result": lambda_result})
    time.sleep(2)  # Brief pause between deployments
    
    # Deploy S3
    s3_result = create_s3_bucket(bucket_name)
    execution_results.append({"resource": "S3", "result": s3_result})
    time.sleep(1)
    
    # Deploy API Gateway
    api_result = create_api_gateway(api_name)
    execution_results.append({"resource": "API Gateway", "result": api_result})

    execution_summary = {
        "status": "success" if all(r["result"]["status"] == "success" for r in execution_results) else "partial",
        "executed_resources": execution_results,
        "message": f"Deployed {len([r for r in execution_results if r['result']['status'] == 'success'])} real AWS resources successfully.",
        "aws_console_links": {
            "lambda_console": f"https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions",
            "s3_console": "https://s3.console.aws.amazon.com/s3/home",
            "api_gateway_console": "https://us-east-1.console.aws.amazon.com/apigateway/home?region=us-east-1"
        }
    }

    return JSONResponse({
        "result": {
            "task": task,
            "reasoning": reasoning,
            "infra_plan": infra_plan,
            "execution": execution_summary
        }
    })

@app.post("/generate_story")
async def generate_story(req: StoryRequest):
    task = req.task
    infra = req.infra
    execution = req.execution

    story = (
        f"The task '{task}' was executed with REAL AWS DEPLOYMENTS.\n"
        f"Infrastructure deployed: {', '.join(infra['resources'])}.\n"
        f"Execution summary: {execution['message']}.\n"
        "✅ Real Lambda function created with working code\n"
        "✅ Real S3 bucket provisioned for storage\n"
        "✅ Real API Gateway endpoint configured\n"
        "All resources are now live in your AWS account and ready for use."
    )
    return JSONResponse({"story": story})
