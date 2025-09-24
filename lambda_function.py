import json
import boto3
import requests  # This library is available in the Lambda environment

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    This function is triggered by an S3 event. It fetches data from a
    public API and logs it to CloudWatch.
    """
    print("Lambda function triggered by S3 event.")
    
    # 1. Get the bucket and object key from the S3 event
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_file_key = event['Records'][0]['s3']['object']['key']
        print(f"File '{s3_file_key}' was uploaded to bucket '{bucket_name}'.")
    except (KeyError, IndexError) as e:
        print(f"Error parsing S3 event: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Could not parse S3 event information.')
        }

    # 2. Fetch data from a public API
    api_url = "https://jsonplaceholder.typicode.com/posts/1"
    print(f"Fetching data from API: {api_url}")
    
    try:
        response = requests.get(api_url, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status() 
        
        api_data = response.json()
        print("Successfully fetched data from API.")
        print("API Response Data:")
        print(json.dumps(api_data, indent=2))
        
        # You could optionally do something with this data, like writing it to another S3 bucket.
        # For now, we just log it.

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error fetching data from API: {e}')
        }

    # 3. Return a success response
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 event and fetched API data.')
    }
