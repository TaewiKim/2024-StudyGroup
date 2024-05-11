import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.get_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if operation in operations:
        if operation == 'GET':
            # Construct the Key and TableName from queryStringParameters
            key = json.loads(event['queryStringParameters']['Key'])
            table_name = event['queryStringParameters']['TableName']
            payload = {'TableName': table_name, 'Key': key}
        else:
            payload = json.loads(event['body'])
        
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError(f'Unsupported method "{operation}"'))
