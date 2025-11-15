import boto3

s3 = boto3.client('s3')
def lambda_handler(event, context):
    s3.put_object(Bucket='YOUR_BUCKET_NAME', Key='demo.txt', Body='Nelavista AGENT Live Deployment')
    return {'status': 'success', 'message': 'Deployed live on AWS!'}
