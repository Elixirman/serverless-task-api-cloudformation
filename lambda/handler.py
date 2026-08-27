import json
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def handler(event, context):
    method = event.get('httpMethod', '')

    try:
        if method == 'GET':
            return list_tasks()
        elif method == 'POST':
            return create_task(event)
        else:
            return response(400, {'error': f'Unsupported method: {method}'})
    except Exception as e:
        return response(500, {'error': str(e)})


def list_tasks():
    result = table.scan()
    return response(200, {'tasks': result.get('Items', [])})


def create_task(event):
    body = json.loads(event.get('body') or '{}')
    title = body.get('title')

    if not title:
        return response(400, {'error': 'title is required'})

    task = {
        'id': str(uuid.uuid4()),
        'title': title,
        'done': False
    }
    table.put_item(Item=task)
    return response(201, task)


def response(status_code, body_dict):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body_dict)
    }
