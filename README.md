AWS S3 and Lambda Data Fetching Pipeline
This project demonstrates how to interact with AWS S3 using Python and how to deploy a Python script to AWS Lambda that automatically triggers on an S3 file upload.

Table of Contents
Prerequisites

Staying within the AWS Free Tier

Step 1: Setting up your AWS Environment

Step 2: Python Script for S3 Operations

Step 3: Deploying the Lambda Function

Step 4: Testing the Setup

Step 5: Cleaning Up Resources (Important!)

Prerequisites
An AWS Account. If you don't have one, you can create one for free.

Python 3.8 or later installed on your local machine.

An AWS IAM User with programmatic access (Access Key ID and Secret Access Key).

AWS CLI installed and configured on your local machine.

Staying within the AWS Free Tier
The services used in this project (IAM, S3, Lambda, CloudWatch) are all eligible for the AWS Free Tier. For the small scale of this project, you are highly unlikely to exceed the free limits.

AWS Lambda: 1 million free requests per month.

Amazon S3: 5 GB of standard storage.

Amazon CloudWatch: 5 GB of log data ingestion.

AWS IAM: Free to use.

To be extra safe, it's a best practice to set up a billing alarm to notify you if your estimated charges exceed a certain amount (e.g., $1). You can do this in the AWS Billing & Cost Management console.

Important Note on Free Tier Changes: AWS Free Tier policies can be updated. Before starting, it is always best to check the official AWS Free Tier page for the most current details. The core services used in this guide have historically maintained a generous free tier for new accounts, but verifying is a crucial step. Regardless of the current free tier, the most effective way to prevent unexpected charges is to set a billing alarm and diligently follow the cleanup steps when you are finished.

Step 1: Setting up your AWS Environment
1.1. Create an S3 Bucket
Navigate to the S3 service in the AWS Console.

Click Create bucket.

Give your bucket a unique name (e.g., my-unique-data-bucket-123).

Choose an AWS Region.

Keep the default settings for now and click Create bucket.

1.2. Create an IAM User for Programmatic Access
Navigate to the IAM service in the AWS Console.

Go to Users and click Add users.

Enter a User name (e.g., s3-lambda-user).

Select Access key - Programmatic access for the credential type.

Click Next: Permissions.

Select Attach existing policies directly.

Search for and select AmazonS3FullAccess and AWSLambda_FullAccess.

Click Next: Tags, Next: Review, and then Create user.

IMPORTANT: Download the .csv file containing the Access key ID and Secret access key. You will not be able to see the secret key again.

1.3. Configure AWS CLI
Open your terminal or command prompt and configure the AWS CLI with the credentials you just downloaded:

aws configure

You will be prompted to enter your Access Key ID, Secret Access Key, default region, and default output format.

Step 2: Python Script for S3 Operations
This script allows you to manage files in your S3 bucket from your local machine.

2.1. Install Dependencies
pip install -r requirements.txt

2.2. Running the script
Update the s3_operations.py script with your bucket name.

Create a sample file to upload, e.g., sample.txt.

To upload a file:

python s3_operations.py upload sample.txt

To list files:

python s3_operations.py list

To download a file:

python s3_operations.py download sample.txt downloaded_sample.txt

Step 3: Deploying the Lambda Function
This Lambda function will be triggered whenever a new file is uploaded to your S3 bucket.

3.1. Create the Lambda Execution Role
In the IAM console, go to Roles and click Create role.

Select AWS service as the trusted entity, and choose Lambda as the use case.

Add the following policies:

AmazonS3FullAccess

AWSLambdaBasicExecutionRole (for logging to CloudWatch)

Give the role a name (e.g., lambda-s3-execution-role) and create it.

3.2. Create the Lambda Function
Navigate to the Lambda service in the AWS Console.

Click Create function.

Select Author from scratch.

Function name: fetchApiDataOnS3Upload

Runtime: Python 3.9

Architecture: x86_64

Permissions: Choose Use an existing role and select the lambda-s3-execution-role you created.

Click Create function.

3.3. Configure the Lambda Function
In the function's page, scroll down to the Code source editor.

Copy the code from lambda_function.py and paste it into the lambda_function.py file in the editor.

Click the Deploy button to save your code.

3.4. Add the S3 Trigger
In the function's page, click Add trigger.

Select S3 from the list of services.

Bucket: Choose the S3 bucket you created earlier.

Event type: All object create events.

Acknowledge the recursive invocation warning and click Add.

Step 4: Testing the Setup
Upload any file to your S3 bucket using the AWS console or the s3_operations.py script.

Navigate to the CloudWatch service in the AWS Console.

Go to Log groups and find the log group for your Lambda function (e.g., /aws/lambda/fetchApiDataOnS3Upload).

Click on the latest log stream to see the output from your function, which should include the fetched data from the public API.

Step 5: Cleaning Up Resources (Important!)
To avoid any potential charges after you are done experimenting, follow these steps in order to delete all the AWS resources you created.

5.1. Empty and Delete the S3 Bucket
You must empty an S3 bucket before you can delete it.

Navigate to the S3 console.

Click on your bucket name.

Select all the files inside and click Delete.

Type permanently delete to confirm and click Delete objects.

Go back to the S3 buckets list, select your bucket, and click Delete.

Enter your bucket name to confirm and click Delete bucket.

5.2. Delete the Lambda Function
Deleting the function also removes the S3 trigger automatically.

Navigate to the Lambda console.

Select your function (fetchApiDataOnS3Upload).

Click Actions, then Delete.

Confirm the deletion by typing delete in the prompt.

5.3. Delete the CloudWatch Log Group
The Lambda function automatically creates a log group. It's good practice to delete it.

Navigate to the CloudWatch console.

In the left menu, go to Logs -> Log groups.

Find the log group for your function (it will be named /aws/lambda/fetchApiDataOnS3Upload).

Select the checkbox next to it.

Click Actions, then Delete log group(s).

Confirm the deletion.

5.4. Delete the IAM Role and User
Finally, delete the permissions and the user you created.

Navigate to the IAM console.

Go to Roles on the left menu.

Find and select the role you created (lambda-s3-execution-role).

Click Delete, and confirm.

Go to Users on the left menu.

Find and select the user you created (s3-lambda-user).

Click Delete, and confirm.