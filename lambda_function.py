import json
import boto3
import uuid

# Initialize DynamoDB resource and specify the table name
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')  # Make sure this matches your DynamoDB table name

def lambda_handler(event, context):
    try:
        http_method = event.get('httpMethod')

        if http_method == 'POST':
            # Create a new task
            body = json.loads(event.get('body', '{}'))
            title = body.get('title', '').strip()
            if not title:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Title is required'})
                }

            task_id = str(uuid.uuid4())
            table.put_item(Item={
                'id': task_id,
                'title': title
            })

            return {
                'statusCode': 201,
                'body': json.dumps({'message': 'Task created successfully', 'id': task_id})
            }

        elif http_method == 'GET':
            # Retrieve all tasks
            response = table.scan()
            tasks = response.get('Items', [])
            return {
                'statusCode': 200,
                'body': json.dumps(tasks)
            }

        elif http_method == 'PUT':
            # Update an existing task by ID
            path_params = event.get('pathParameters') or {}
            task_id = path_params.get('id')
            if not task_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Task ID is required in the path parameters'})
                }

            body = json.loads(event.get('body', '{}'))
            title = body.get('title', '').strip()
            if not title:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Title is required'})
                }

            # Update the item in DynamoDB
            table.update_item(
                Key={'id': task_id},
                UpdateExpression='SET title = :t',
                ExpressionAttributeValues={':t': title},
                ConditionExpression='attribute_exists(id)'  # Ensure the item exists before updating
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Task updated successfully'})
            }

        elif http_method == 'DELETE':
            # Delete a task by ID
            path_params = event.get('pathParameters') or {}
            task_id = path_params.get('id')
            if not task_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Task ID is required in the path parameters'})
                }

            # Delete the item from DynamoDB
            table.delete_item(
                Key={'id': task_id},
                ConditionExpression='attribute_exists(id)'  # Ensure the item exists before deleting
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Task deleted successfully'})
            }

        else:
            # Unsupported HTTP method
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method Not Allowed'})
            }

    except boto3.client('dynamodb').exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Task not found'})
        }

    except Exception as e:
        # General exception handler for unexpected errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
