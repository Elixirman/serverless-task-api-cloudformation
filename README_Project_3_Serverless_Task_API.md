# Project 3 — Serverless Task API
## Complete Line-by-Line Breakdown

## 1. Overview

This project creates a serverless REST API using:

```text
Client
  |
  | HTTPS
  v
API Gateway
  |
  | AWS_PROXY
  v
Lambda (Python 3.12)
  |
  | IAM permissions
  v
DynamoDB
```

CloudFormation defines the infrastructure as code.

There are no EC2 servers to patch or manage.

---

## 2. What "Serverless" Means

Serverless does not mean there are no servers.

AWS manages the underlying servers for you.

You manage mainly:

- Application code
- Configuration
- IAM permissions
- Infrastructure definition

AWS handles:

- Provisioning
- Scaling
- Operating systems
- Patching
- Much of the infrastructure management

The application can scale automatically with demand.

---

## 3. Architecture

```text
                         CLIENT
                           |
                           | HTTPS
                           v
                  +-------------------+
                  |   API Gateway     |
                  |    REST API       |
                  |      /tasks       |
                  +---------+---------+
                            |
                            | AWS_PROXY
                            v
                  +-------------------+
                  |      Lambda       |
                  |   Python 3.12     |
                  +---------+---------+
                            |
                            | IAM
                            v
                  +-------------------+
                  |    DynamoDB       |
                  |   Tasks Table     |
                  +-------------------+
```

Request flow:

```text
Client
  |
  | HTTPS
  v
API Gateway
  |
  | Invoke
  v
Lambda
  |
  | Read / Write
  v
DynamoDB
```

---

# 4. API Gateway

API Gateway is the public entry point.

Think of it as the front door of the application.

```text
Internet
   |
   v
API Gateway
   |
   v
Lambda
```

It receives HTTP requests and routes them to Lambda.

---

# 5. Lambda

Lambda runs the application code.

This project uses:

```text
Python 3.12
```

Lambda executes when API Gateway invokes it.

Instead of keeping an EC2 server running continuously:

```text
EC2
 |
 +-- Server running 24/7
```

Lambda works like:

```text
Request
   |
   v
Lambda executes
   |
   v
Response
```

---

# 6. DynamoDB

DynamoDB is the database.

It stores the tasks.

Example:

```json
{
  "id": "123",
  "title": "Learn CloudFormation"
}
```

The overall relationship is:

```text
Lambda
   |
   v
DynamoDB
   |
   +-- Task 1
   +-- Task 2
   +-- Task 3
```

---

# 7. Pay-Per-Request

The DynamoDB table uses pay-per-request billing.

This means you do not have to manually plan fixed read/write capacity for this project.

It is useful for:

- Portfolio projects
- Development
- Low or unpredictable traffic
- Small applications

---

# 8. API Endpoints

The API exposes:

```text
/tasks
```

Methods:

| Method | Path | Purpose |
|---|---|---|
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |

---

# 9. GET /tasks

```http
GET /tasks
```

Purpose:

> Retrieve tasks from DynamoDB.

Flow:

```text
Client
  |
  | GET /tasks
  v
API Gateway
  |
  v
Lambda
  |
  | Scan
  v
DynamoDB
  |
  v
Tasks
```

---

# 10. POST /tasks

```http
POST /tasks
```

Request body:

```json
{
  "title": "Learn CloudFormation"
}
```

Flow:

```text
Client
  |
  | POST /tasks
  | JSON body
  v
API Gateway
  |
  v
Lambda
  |
  | PutItem
  v
DynamoDB
```

---

# 11. CloudFormation

The infrastructure is defined in:

```text
template.yaml
```

CloudFormation reads the template and creates the AWS resources.

Conceptually:

```text
template.yaml
      |
      v
CloudFormation
      |
      +-- API Gateway
      +-- Lambda
      +-- DynamoDB
      +-- IAM
```

---

# 12. Stack Resources

The project contains:

```text
TasksTable
LambdaExecutionRole
TasksFunction
TasksApi
TasksResource
GetTasksMethod
PostTasksMethod
LambdaApiPermission
ApiDeployment
ApiStage
```

Each resource has a specific purpose.

---

# 13. TasksTable

```text
TasksTable
```

Creates the DynamoDB table.

Purpose:

> Store application tasks.

Conceptually:

```text
TasksTable
|
+-- Task 1
+-- Task 2
+-- Task 3
```

---

# 14. LambdaExecutionRole

```text
LambdaExecutionRole
```

Creates the IAM role used by Lambda.

The role controls what Lambda is allowed to access.

```text
Lambda
   |
   v
IAM Role
   |
   +-- DynamoDB permissions
   +-- CloudWatch Logs permissions
```

---

# 15. Least Privilege

The Lambda role should only contain the permissions the application needs.

Typical DynamoDB actions in this project are:

```text
dynamodb:GetItem
dynamodb:PutItem
dynamodb:Scan
```

These permissions are scoped to the application's table.

This is the principle of:

> Least privilege.

Meaning:

> Give a service only the permissions it actually needs.

---

# 16. GetItem

```text
dynamodb:GetItem
```

Allows Lambda to retrieve a specific item using its key.

```text
Lambda
 |
 | GetItem
 v
Specific DynamoDB item
```

---

# 17. PutItem

```text
dynamodb:PutItem
```

Allows Lambda to create or replace an item.

Example:

```json
{
  "id": "123",
  "title": "Learn AWS"
}
```

---

# 18. Scan

```text
dynamodb:Scan
```

Allows Lambda to read items across the table.

This can be used to implement:

```text
GET /tasks
```

Important:

> Scan reads across the table and is not ideal for very large production datasets.

For a small portfolio project, it is fine.

---

# 19. CloudWatch Logs

Lambda execution logs can be sent to CloudWatch Logs.

This allows you to inspect:

```text
Execution messages
Errors
Debug information
Request information
```

This is important when troubleshooting Lambda.

---

# 20. TasksFunction

```text
TasksFunction
```

Creates the Lambda function containing the API logic.

Conceptually:

```text
API Gateway
      |
      v
TasksFunction
      |
      +-- GET  -> DynamoDB
      |
      +-- POST -> DynamoDB
```

---

# 21. Python 3.12

The Lambda runtime is:

```text
python3.12
```

This tells AWS to execute the function using Python 3.12.

---

# 22. Lambda Handler

The code normally contains a handler such as:

```python
def lambda_handler(event, context):
    ...
```

Lambda calls this function when it receives an invocation.

```text
API Gateway
     |
     v
Lambda runtime
     |
     v
lambda_handler()
```

---

# 23. TasksApi

```text
TasksApi
```

Creates the API Gateway REST API.

It provides the public HTTP interface.

A resulting URL has a structure similar to:

```text
https://xxxxx.execute-api.region.amazonaws.com/prod/tasks
```

---

# 24. TasksResource

```text
TasksResource
```

Creates the:

```text
/tasks
```

resource.

So:

```text
API Gateway
    |
    +-- /tasks
```

---

# 25. GetTasksMethod

```text
GetTasksMethod
```

Creates:

```http
GET /tasks
```

Purpose:

> Return tasks.

---

# 26. PostTasksMethod

```text
PostTasksMethod
```

Creates:

```http
POST /tasks
```

Purpose:

> Create a new task.

---

# 27. AWS_PROXY Integration

The API methods use:

```text
AWS_PROXY
```

integration.

This means API Gateway passes the incoming request information to Lambda.

Conceptually:

```text
HTTP Request
     |
     v
API Gateway
     |
     | Proxy event
     v
Lambda
     |
     | Response
     v
API Gateway
     |
     v
Client
```

Lambda is responsible for interpreting the event and generating the response.

---

# 28. LambdaApiPermission

```text
LambdaApiPermission
```

This explicitly allows API Gateway to invoke the Lambda function.

Relationship:

```text
API Gateway
      |
      | InvokeFunction
      v
Lambda
```

This permission is required.

---

# 29. IAM Role vs Lambda Permission

This distinction is very important.

### Lambda Execution Role

Controls:

> What Lambda can access.

Example:

```text
Lambda
  |
  | IAM Role
  v
DynamoDB
```

### Lambda Resource Permission

Controls:

> Who can invoke Lambda.

Example:

```text
API Gateway
  |
  | Invoke
  v
Lambda
```

Remember:

```text
Execution Role
= What Lambda can do

Lambda Permission
= Who can invoke Lambda
```

---

# 30. ApiDeployment

```text
ApiDeployment
```

Publishes the configured API methods.

Conceptually:

```text
API configuration
       |
       v
Deployment
       |
       v
Published API
```

---

# 31. ApiStage

```text
ApiStage
```

Creates the API stage.

The project uses:

```text
prod
```

Therefore the API URL contains:

```text
/prod
```

Example:

```text
https://xxxxx.execute-api.region.amazonaws.com/prod/tasks
```

---

# 32. GET Request Flow

```text
GET /prod/tasks
       |
       v
API Gateway
       |
       | AWS_PROXY
       v
Lambda
       |
       | Scan
       v
DynamoDB
       |
       v
Lambda response
       |
       v
API Gateway
       |
       v
Client
```

---

# 33. POST Request Flow

```text
POST /prod/tasks
       |
       | JSON
       v
API Gateway
       |
       v
Lambda
       |
       | PutItem
       v
DynamoDB
       |
       v
Lambda response
       |
       v
API Gateway
       |
       v
Client
```

---

# 34. Lambda Deployment Package

The Lambda code is packaged as:

```text
function.zip
```

For this project:

```text
function.zip
└── handler.py
```

The ZIP is uploaded to S3.

```text
handler.py
    |
    v
function.zip
    |
    v
S3
    |
    v
Lambda
```

---

# 35. Why S3 Stores the ZIP

S3 acts as the deployment artifact location.

This separates:

```text
Application code
```

from:

```text
Infrastructure definition
```

So:

```text
template.yaml
     |
     v
CloudFormation

function.zip
     |
     v
S3 -> Lambda
```

---

# 36. Deployment Step 1 — Enter Lambda Directory

```bash
cd lambda
```

Moves into the Lambda source directory.

---

# 37. Create the ZIP

```bash
zip function.zip handler.py
```

Creates:

```text
function.zip
```

containing:

```text
handler.py
```

---

# 38. Return to Project Directory

```bash
cd ..
```

Moves back to the project directory.

---

# 39. Create Deployment Bucket

```bash
aws s3 mb s3://your-lambda-deployments-bucket
```

`mb` means:

```text
make bucket
```

This creates the S3 bucket used to store the Lambda package.

Remember:

> S3 bucket names must be globally unique.

---

# 40. Upload Lambda Package

```bash
aws s3 cp lambda/function.zip s3://your-lambda-deployments-bucket/function.zip
```

This uploads:

```text
lambda/function.zip
```

to S3.

---

# 41. Deploy CloudFormation Stack

```bash
aws cloudformation create-stack   --stack-name project3-serverless-api   --template-body file://template.yaml   --capabilities CAPABILITY_IAM   --parameters ParameterKey=LambdaCodeBucket,ParameterValue=your-lambda-deployments-bucket
```

This command tells AWS to create the CloudFormation stack.

---

# 42. `create-stack`

```bash
aws cloudformation create-stack
```

Means:

> Create a new CloudFormation stack.

---

# 43. Stack Name

```bash
--stack-name project3-serverless-api
```

Names the stack:

```text
project3-serverless-api
```

---

# 44. Template Body

```bash
--template-body file://template.yaml
```

Tells the AWS CLI to read the CloudFormation template from the local file:

```text
template.yaml
```

---

# 45. CAPABILITY_IAM

```bash
--capabilities CAPABILITY_IAM
```

The template creates IAM resources.

AWS requires acknowledgement that the stack is allowed to create IAM resources.

---

# 46. LambdaCodeBucket Parameter

```bash
--parameters ParameterKey=LambdaCodeBucket,ParameterValue=your-lambda-deployments-bucket
```

Passes the deployment bucket name into CloudFormation.

The parameter is:

```text
LambdaCodeBucket
```

The supplied value is:

```text
your-lambda-deployments-bucket
```

---

# 47. Get the API URL

```bash
aws cloudformation describe-stacks   --stack-name project3-serverless-api   --query "Stacks[0].Outputs"
```

This asks CloudFormation to display the stack outputs.

The outputs can include the API URL.

---

# 48. Test GET

```bash
curl https://<api-url>/prod/tasks
```

This sends:

```http
GET /prod/tasks
```

Flow:

```text
curl
 |
 v
API Gateway
 |
 v
Lambda
 |
 v
DynamoDB
```

---

# 49. Test POST

```bash
curl -X POST https://<api-url>/prod/tasks   -H "Content-Type: application/json"   -d '{"title": "Learn CloudFormation"}'
```

Breakdown:

```text
-X POST
```

means:

> Use POST.

```text
-H "Content-Type: application/json"
```

means:

> The body is JSON.

```text
-d '{"title": "Learn CloudFormation"}'
```

means:

> Send this task data.

---

# 50. Updating Lambda Code

When `handler.py` changes, create a new ZIP.

```bash
cd lambda
zip function.zip handler.py
cd ..
```

Then upload it:

```bash
aws s3 cp lambda/function.zip s3://your-lambda-deployments-bucket/function.zip
```

Then update Lambda:

```bash
aws lambda update-function-code   --function-name tasks-api-handler   --s3-bucket your-lambda-deployments-bucket   --s3-key function.zip
```

This tells Lambda to use the updated package.

---

# 51. Infrastructure vs Application Code

There are two separate parts.

### Infrastructure

```text
template.yaml
     |
     v
CloudFormation
```

### Application code

```text
handler.py
     |
     v
function.zip
     |
     v
S3
     |
     v
Lambda
```

This separation is an important cloud engineering concept.

---

# 52. Delete the Stack

```bash
aws cloudformation delete-stack   --stack-name project3-serverless-api
```

This asks CloudFormation to delete the stack resources.

Conceptually:

```text
CloudFormation
 |
 +-- API Gateway
 +-- Lambda
 +-- IAM Role
 +-- DynamoDB
 |
 v
Deleted
```

---

# 53. Delete Deployment Bucket Contents

```bash
aws s3 rm s3://your-lambda-deployments-bucket --recursive
```

Removes objects from the deployment bucket.

`--recursive` means:

> Process everything under that location.

---

# 54. Delete the Bucket

```bash
aws s3 rb s3://your-lambda-deployments-bucket
```

`rb` means:

```text
remove bucket
```

The bucket normally needs to be empty first.

---

# 55. Cost Concept

This architecture is designed for very low-cost portfolio/demo traffic.

The key idea is that you are not maintaining an always-running EC2 server.

Instead:

```text
Request
   |
   v
Lambda executes
```

DynamoDB uses:

```text
Pay-per-request
```

Actual cost depends on AWS region, request volume, storage, data transfer, and other usage.

So "essentially free" should be understood as:

> Likely very inexpensive at small portfolio-demo traffic levels, not a guarantee of zero cost.

---

# 56. Scale-to-Zero Concept

With Lambda:

```text
No requests
     |
     v
No Lambda invocation
```

When traffic arrives:

```text
Request
   |
   v
Lambda invocation
```

This is one reason serverless architectures are attractive for applications with intermittent traffic.

---

# 57. EC2 vs Serverless

## Traditional EC2

```text
Internet
   |
   v
EC2
   |
   v
Database
```

You manage more of:

```text
Operating system
Patching
Server sizing
Scaling
Server availability
```

## Serverless

```text
Internet
   |
   v
API Gateway
   |
   v
Lambda
   |
   v
DynamoDB
```

AWS manages much more of the underlying infrastructure.

---

# 58. What This Project Demonstrates

This project demonstrates:

### Serverless Architecture

```text
API Gateway
     |
Lambda
     |
DynamoDB
```

### Infrastructure as Code

CloudFormation defines the infrastructure.

### Least-Privilege IAM

Lambda receives only required permissions.

### REST API Design

```text
GET /tasks
POST /tasks
```

### Event-Driven Compute

API Gateway triggers Lambda.

### Managed Database

DynamoDB is managed by AWS.

### AWS CLI

The project is deployed and tested through CLI commands.

---

# 59. Important Relationships

## API Gateway -> Lambda

```text
API Gateway
     |
     | permission to invoke
     v
Lambda
```

## Lambda -> DynamoDB

```text
Lambda
   |
   | IAM Role
   v
DynamoDB
```

## Lambda Code -> S3

```text
handler.py
    |
    v
function.zip
    |
    v
S3
    |
    v
Lambda
```

## CloudFormation -> Infrastructure

```text
CloudFormation
      |
      +-- API Gateway
      +-- Lambda
      +-- DynamoDB
      +-- IAM
```

---

# 60. Key AWS Concepts Cheat Sheet

| Concept | Simple Meaning |
|---|---|
| API Gateway | Front door for the API |
| REST API | HTTP-based API interface |
| Lambda | Runs code without managing servers |
| DynamoDB | Managed NoSQL database |
| IAM Role | Gives Lambda AWS permissions |
| Lambda Permission | Allows API Gateway to invoke Lambda |
| AWS_PROXY | Passes API requests to Lambda |
| CloudFormation | Defines infrastructure as code |
| S3 | Stores the Lambda ZIP package |
| CloudWatch Logs | Stores Lambda execution logs |
| Pay-per-request | DynamoDB capacity is handled based on usage |
| API Stage | Published API environment such as `prod` |

---

# 61. Exam Memory Trick

Remember the architecture as:

```text
CLIENT
  |
  v
API GATEWAY
  |
  v
LAMBDA
  |
  v
DYNAMODB
```

Remember IAM as:

```text
Lambda Execution Role
=
What Lambda can do
```

```text
Lambda Resource Permission
=
Who can invoke Lambda
```

Remember CloudFormation as:

```text
template.yaml
      |
      v
CloudFormation
      |
      +-- Creates infrastructure
```

Remember deployment as:

```text
handler.py
    |
    v
function.zip
    |
    v
S3
    |
    v
Lambda
```

---

# 62. Complete Mental Model

The entire project can be remembered as:

```text
                         CLIENT
                           |
                           | HTTPS
                           v
                  +-------------------+
                  |   API GATEWAY     |
                  |      /tasks       |
                  +---------+---------+
                            |
                            | AWS_PROXY
                            v
                  +-------------------+
                  |      LAMBDA       |
                  |     Python 3.12   |
                  +---------+---------+
                            |
                            | IAM Role
                            v
                  +-------------------+
                  |     DYNAMODB      |
                  |    TasksTable     |
                  +-------------------+

                         IAM
                          |
             +------------+------------+
             |                         |
             v                         v
     Lambda Execution Role     API Gateway Permission
             |                         |
             v                         v
       DynamoDB/Logs              Invoke Lambda
```

CloudFormation creates and manages the infrastructure above.

---

# 63. Portfolio Progression

If Project 2 was:

```text
VPC
Subnet
Internet Gateway
Route Table
Security Group
EC2
IAM
S3
```

Project 3 advances into:

```text
API Gateway
Lambda
DynamoDB
IAM
Serverless
REST APIs
Event-driven architecture
```

This demonstrates that you understand CloudFormation beyond EC2-based infrastructure.

---

# 64. Final One-Sentence Summary

> **Project 3 uses CloudFormation to create a serverless REST API where API Gateway receives HTTPS requests, Lambda executes Python code, DynamoDB stores tasks, and IAM controls exactly what Lambda can do.**

---

# 65. Portfolio Value

This project demonstrates:

```text
Infrastructure as Code
        +
Serverless Architecture
        +
REST APIs
        +
Event-Driven Compute
        +
NoSQL
        +
IAM Least Privilege
        +
AWS CLI
        +
CloudFormation
```

It is a strong progression from an EC2-based architecture into modern serverless AWS architecture.
