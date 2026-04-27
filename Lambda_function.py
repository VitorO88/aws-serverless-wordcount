import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Get bucket name and file name from S3 event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key'],
            encoding='utf-8'
        )

        # Read SNS topic ARN from environment variables
        import os
        topic_arn = os.environ['SNS_TOPIC_ARN']

        # Get the uploaded file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')

        # Count words
        word_count = len(file_content.split())

        # Format message
        message = f"The word count in the {object_key} file is {word_count}."

        # Publish to SNS
        sns.publish(
            TopicArn=topic_arn,
            Subject="Word Count Result",
            Message=message
        )

        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }