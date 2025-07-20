# Serverless REST API with AWS Lambda, API Gateway, and DynamoDB

## Project Overview
This project implements a serverless REST API for managing tasks (to-do items) using AWS services.  
The API supports CRUD operations: create, read, update, and delete tasks.

## Architecture
- **API Gateway**: Exposes REST endpoints for clients to interact with the API.  
- **AWS Lambda**: Contains the business logic to handle API requests and perform operations on the database.  
- **Amazon DynamoDB**: NoSQL database used to store task data.  
- **IAM Roles**: Secure permissions for Lambda functions to access DynamoDB.  

![Architecture Diagram](./architecture-diagram.png)

## Features
- Create a task (POST /tasks)  
- Retrieve all tasks (GET /tasks)  
- Update a task (PUT /tasks/{id})  
- Delete a task (DELETE /tasks/{id})

## How to Deploy
1. Create a DynamoDB table named `Tasks` with primary key `id` (String).  
2. Deploy the Lambda function with the provided code and attach an IAM role with permissions to access DynamoDB.  
3. Set up API Gateway with the `/tasks` and `/tasks/{id}` resources and link the HTTP methods to the Lambda function.  
4. Enable CORS on API Gateway if you plan to call from a web frontend.

## How to Test
Use tools like Postman or curl to test the API endpoints. Example:

```bash
# Create a task
curl -X POST https://your-api-endpoint/tasks -d '{"title": "Finish AWS project"}'

# Get all tasks
curl https://your-api-endpoint/tasks

# Update a task
curl -X PUT https://your-api-endpoint/tasks/{id} -d '{"title": "Updated task title"}'

# Delete a task
curl -X DELETE https://your-api-endpoint/tasks/{id}
