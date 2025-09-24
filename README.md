Project: Building a Data Pipeline with AWS S3, Lambda, and DynamoDB
Welcome! This guide will walk you through building a simple, event-driven data pipeline on AWS. It's designed for beginners and covers essential services for cloud computing and data engineering.

Part 1: You will learn how to set up an S3 bucket and an AWS Lambda function. The function will automatically run whenever a new file is uploaded to the bucket, fetching data from a public API.

Part 2: You will create a NoSQL database table using Amazon DynamoDB and use a Python script to perform basic database operations (writing, reading, and updating data).

By the end, you'll have hands-on experience with serverless computing, cloud storage, and managed databases.

Table of Contents
PART 1: S3 AND LAMBDA

Prerequisites

Important: Staying within the AWS Free Tier

Step 1: Setting up Your AWS Environment

Step 2: Script for Manual S3 Operations

Step 3: Deploying the Lambda Function

Step 4: Testing the Automated Workflow

PART 2: DYNAMODB OPERATIONS
7.  Step 5: Setting up DynamoDB
8.  Step 6: Script for Database Operations

PROJECT CLEANUP
9.  Step 7: Cleaning Up All Resources (Crucial!)

Prerequisites
Before you begin, ensure you have the following:

An AWS Account: If you don't have one, you can create one for free.

Python: Version 3.8 or later installed. You can check your version by running python --version in your terminal.

AWS IAM User: A user with programmatic access. We will create this in Step 1.

AWS CLI: The AWS Command Line Interface. Follow these instructions to install it.

Important: Staying within the AWS Free Tier
This project is designed to use services that are eligible for the AWS Free Tier, meaning you should not incur any costs if you are a new user.

AWS Lambda: 1 million free requests per month.

Amazon S3: 5 GB of standard storage.

Amazon DynamoDB: 25 GB of storage.

Amazon CloudWatch: 5 GB of log data ingestion.

Note on Free Tier Changes: AWS Free Tier policies can be updated. Before starting, always check the official AWS Free Tier page for the most current details. The best way to prevent unexpected charges is to diligently follow the cleanup steps at the end of this guide.

PART 1: S3 AND LAMBDA
Step 1: Setting up Your AWS Environment
1.1. Create an S3 Bucket
An S3 bucket is a cloud storage container. We'll use it as the starting point for our data pipeline.

In the AWS Management Console, search for and navigate to the S3 service.

Click Create bucket.

Give the bucket a globally unique name (e.g., my-data-pipeline-bucket- followed by your initials and the date).

Select an AWS Region (e.g., us-east-1).

Keep the default settings and click Create bucket.

1.2. Create an IAM User for Programmatic Access
This user will grant our local Python scripts the necessary permissions to interact with AWS services.

Navigate to the IAM service -> Users and click Add users.

Enter a User name (e.g., s3-lambda-user).

Select Access key - Programmatic access for the credential type.

Click Next: Permissions -> Attach existing policies directly.

Search for and select the following policies. These grant the necessary permissions for the entire project:

AmazonS3FullAccess

AWSLambda_FullAccess

AmazonDynamoDBFullAccess

Click through the remaining steps and Create user.

CRITICAL: On the final screen, download the .csv file. It contains the Access key ID and Secret access key. This is your only chance to save them.

1.3. Configure the AWS CLI
This step securely connects your local machine to your AWS account.

Open your terminal or command prompt.

Run the command: aws configure

You will be prompted to enter the credentials from the .csv file.

AWS Access Key ID: Copy and paste from your .csv file.

AWS Secret Access Key: Copy and paste from your .csv file.

Default region name: Enter the same region you chose for your S3 bucket (e.g., us-east-1).

Default output format: You can press Enter to leave this blank, or type json.

Step 2: Script for Manual S3 Operations
This utility script helps you test your S3 bucket by manually uploading, listing, and downloading files.

2.1. Install Dependencies
The requirements.txt file lists the Python libraries needed for this project.

pip install -r requirements.txt

2.2. Running the script
Open s3_operations.py and replace the placeholder bucket name with your actual S3 bucket name.

Create a local test file named sample.txt.

Run the following commands in your terminal:

# Upload sample.txt to your S3 bucket
python s3_operations.py upload sample.txt

# List all files in your bucket
python s3_operations.py list

# Download the file from S3 and save it as downloaded_sample.txt
python s3_operations.py download sample.txt downloaded_sample.txt

Step 3: Deploying the Lambda Function
Now we'll create the serverless function that runs automatically.

3.1. Create the Lambda Execution Role
This role gives our Lambda function permission to interact with other AWS services (like writing logs).

In IAM, go to Roles -> Create role.

Select AWS service as the trusted entity, and choose Lambda as the use case.

Add the policies: AmazonS3FullAccess and AWSLambdaBasicExecutionRole.

Give the role a name (e.g., lambda-s3-execution-role) and create it.

3.2. Create and Configure the Lambda Function
Navigate to the Lambda service and click Create function.

Select Author from scratch.

Name your function fetchApiDataOnS3Upload and choose Python 3.9 as the runtime.

Under Permissions, expand "Change default execution role" and select Use an existing role. Choose the lambda-s3-execution-role you just created.

Click Create function.

In the function's code editor, paste the entire content of lambda_function.py and click Deploy.

Now, let's link S3 to Lambda. Click Add trigger, select S3, choose your bucket, and ensure the event type is All object create events. Acknowledge the warning and click Add.

Step 4: Testing the Automated Workflow
Upload any file (e.g., sample.txt) to your S3 bucket using the AWS console or the s3_operations.py script.

This action will automatically trigger your Lambda function.

Navigate to CloudWatch -> Log groups.

Find the log group named /aws/lambda/fetchApiDataOnS3Upload. Inside, you will see the execution logs, including the data fetched from the public API.

PART 2: DYNAMODB OPERATIONS
Step 5: Setting up DynamoDB
DynamoDB is a fast and flexible NoSQL database. We'll create a table to store user information.

Navigate to the DynamoDB service.

Click Create table.

Table name: Users

Partition key: userId (Type: String). This is the unique identifier for each item in the table.

Leave all other settings as default and click Create table.

Step 6: Script for Database Operations
This script provides a command-line interface to interact with your Users table.

6.1. Running the script
Execute these commands from your terminal to manage items in the database.

To create a new user:

python dynamodb_operations.py put --userId "user001" --firstName "John" --lastName "Doe"

To retrieve that user's data:

python dynamodb_operations.py get --userId "user001"

To add or update an attribute (e.g., age):

python dynamodb_operations.py update --userId "user001" --age 30

PROJECT CLEANUP
Step 7: Cleaning Up All Resources (Crucial!)
To prevent any future costs, it is essential to delete all the resources you have created. Perform these steps in order.

7.1. Empty and Delete the S3 Bucket
Navigate to the S3 console, select your bucket, and click Empty.

Once empty, select the bucket again and click Delete.

7.2. Delete the Lambda Function
Navigate to the Lambda console.

Select your fetchApiDataOnS3Upload function and choose Actions -> Delete.

7.3. Delete the DynamoDB Table
Navigate to the DynamoDB console.

Select the Users table and click Delete.

7.4. Delete the CloudWatch Log Group
Navigate to the CloudWatch console -> Log groups.

Find /aws/lambda/fetchApiDataOnS3Upload, select it, and choose Actions -> Delete log group(s).

7.5. Delete the IAM Roles and User
Navigate to the IAM console.

Go to Roles, select lambda-s3-execution-role, and delete it.

Go to Users, select s3-lambda-user, and delete it.