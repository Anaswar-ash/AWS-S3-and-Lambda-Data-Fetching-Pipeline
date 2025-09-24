import boto3
import argparse
import os
from botocore.exceptions import ClientError

# --- Configuration ---
# It's a good practice to externalize configuration.
# For this script, we'll keep it simple.
TABLE_NAME = "Users"

# It's recommended to use a boto3 session and explicitly specify the region.
# If your default region is configured in AWS CLI, this is not strictly necessary.
# os.environ['AWS_REGION'] = "us-east-1"
# session = boto3.Session()
# dynamodb = session.resource('dynamodb')

# For simplicity, we will use the default client initialization.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def put_user_item(user_id, first_name, last_name):
    """
    Writes a new item to the DynamoDB table.
    This will overwrite an existing item with the same userId.
    """
    try:
        response = table.put_item(
            Item={
                'userId': user_id,
                'firstName': first_name,
                'lastName': last_name
            }
        )
        print(f"Successfully added user '{first_name} {last_name}' with ID '{user_id}'.")
        return response
    except ClientError as e:
        print(f"Error putting item: {e.response['Error']['Message']}")
        return None

def get_user_item(user_id):
    """
    Reads an item from the DynamoDB table by its primary key.
    """
    try:
        response = table.get_item(
            Key={
                'userId': user_id
            }
        )
        item = response.get('Item')
        if item:
            print("Successfully retrieved item:")
            print(item)
        else:
            print(f"No item found with userId: {user_id}")
        return item
    except ClientError as e:
        print(f"Error getting item: {e.response['Error']['Message']}")
        return None

def update_user_item(user_id, age):
    """
    Updates an existing item in the DynamoDB table.
    Adds an 'age' attribute or updates it if it already exists.
    """
    try:
        response = table.update_item(
            Key={
                'userId': user_id
            },
            UpdateExpression="set age = :a",
            ExpressionAttributeValues={
                ':a': age
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Successfully updated userId '{user_id}' with age {age}.")
        print("Updated attributes:", response.get('Attributes'))
        return response
    except ClientError as e:
        print(f"Error updating item: {e.response['Error']['Message']}")
        return None

def main():
    """Main function to parse arguments and call the appropriate function."""
    parser = argparse.ArgumentParser(description="Perform DynamoDB operations on the 'Users' table.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Sub-parser for 'put' command ---
    parser_put = subparsers.add_parser("put", help="Write an item to the table.")
    parser_put.add_argument("--userId", required=True, help="The user ID (partition key).")
    parser_put.add_argument("--firstName", required=True, help="User's first name.")
    parser_put.add_argument("--lastName", required=True, help="User's last name.")

    # --- Sub-parser for 'get' command ---
    parser_get = subparsers.add_parser("get", help="Read an item from the table.")
    parser_get.add_argument("--userId", required=True, help="The user ID of the item to retrieve.")

    # --- Sub-parser for 'update' command ---
    parser_update = subparsers.add_parser("update", help="Update an item in the table.")
    parser_update.add_argument("--userId", required=True, help="The user ID of the item to update.")
    parser_update.add_argument("--age", required=True, type=int, help="The age to add or update for the user.")

    args = parser.parse_args()

    if args.command == "put":
        put_user_item(args.userId, args.firstName, args.lastName)
    elif args.command == "get":
        get_user_item(args.userId)
    elif args.command == "update":
        update_user_item(args.userId, args.age)

if __name__ == "__main__":
    main()
