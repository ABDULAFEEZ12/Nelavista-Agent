import boto3
import json
import zipfile
import os
import io
from datetime import datetime

AWS_REGION = "us-east-1"

# Initialize clients
lambda_client = boto3.client("lambda", region_name=AWS_REGION)
s3_client = boto3.client("s3", region_name=AWS_REGION)
apigateway_client = boto3.client("apigateway", region_name=AWS_REGION)

def create_s3_bucket(bucket_name):
    """Create S3 bucket"""
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
        )
        return {"status": "success", "bucket": bucket_name}
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        return {"status": "exists", "bucket": bucket_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_lambda_function(function_name, role_arn="arn:aws:iam::246290151348:role/service-role/lambda_basic_execution"):
    """Create a Lambda function with a basic hello world"""
    # Create a simple zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr("lambda_function.py", """
def lambda_handler(event, context):
    return {"statusCode": 200, "body": "Hello from Nelavista AGENT!"}
""")
    zip_buffer.seek(0)
    
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.11",
            Role=role_arn,
            Handler="lambda_function.lambda_handler",
            Code={"ZipFile": zip_buffer.read()},
            Timeout=10,
            MemorySize=128,
            Publish=True,
        )
        return {"status": "success", "lambda_arn": response["FunctionArn"]}
    except lambda_client.exceptions.ResourceConflictException:
        return {"status": "exists", "function_name": function_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_api_gateway(api_name, lambda_arn):
    """Create REST API Gateway and link to Lambda"""
    try:
        # create REST API
        api = apigateway_client.create_rest_api(
            name=api_name,
            description="Nelavista AGENT Demo API",
        )
        api_id = api["id"]
        
        # get root resource id
        resources = apigateway_client.get_resources(restApiId=api_id)
        root_id = next(r["id"] for r in resources["items"] if r["path"] == "/")
        
        # create resource
        resource = apigateway_client.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart="invoke"
        )
        resource_id = resource["id"]
        
        # create POST method
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="POST",
            authorizationType="NONE"
        )
        
        # link Lambda
        apigateway_client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="POST",
            type="AWS_PROXY",
            integrationHttpMethod="POST",
            uri=f"arn:aws:apigateway:{AWS_REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
        )
        
        # deploy API
        deployment = apigateway_client.create_deployment(
            restApiId=api_id,
            stageName="prod"
        )
        return {"status": "success", "api_id": api_id, "endpoint": f"https://{api_id}.execute-api.{AWS_REGION}.amazonaws.com/prod/invoke"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def deploy_task(task_name):
    """Full deployment sequence"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    bucket_name = f"nelavista-agent-{timestamp}"
    lambda_name = f"NelavistaAgentLambda_{timestamp}"
    api_name = f"NelavistaAgentAPI_{timestamp}"
    
    s3_res = create_s3_bucket(bucket_name)
    lambda_res = create_lambda_function(lambda_name)
    api_res = {}
    if "lambda_arn" in lambda_res:
        api_res = create_api_gateway(api_name, lambda_res["lambda_arn"])
    
    return {
        "task_summary": task_name,
        "resources": ["S3 Bucket", "Lambda Function", "API Gateway Endpoint"],
        "execution": {
            "s3": s3_res,
            "lambda": lambda_res,
            "api_gateway": api_res
        }
    }
