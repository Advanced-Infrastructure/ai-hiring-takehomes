import json
import os
import boto3
import logging
from datetime import datetime, timedelta
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client with VPC endpoint
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def decimal_default(obj):
    """Convert Decimal to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def process_record(record):
    """Process a single SQS record and write to DynamoDB."""
    try:
        # Parse the message body
        message = json.loads(record['body'])
        
        # Convert numeric values to Decimal for DynamoDB
        message['speed_kmh'] = Decimal(str(message['speed_kmh']))
        message['lat'] = Decimal(str(message['lat']))
        message['lon'] = Decimal(str(message['lon']))
        message['distance_from_depot'] = Decimal(str(message['distance_from_depot']))
        
        # Add TTL timestamp (30 days from now)
        message['ttl'] = int((datetime.now() + timedelta(days=30)).timestamp())
        
        # Write to DynamoDB
        table.put_item(Item=message)
        
        logger.info(f"Successfully processed record for vehicle {message['vehicle_id']}")
        return True
        
    except Exception as e:
        logger.error(f"Error processing record: {str(e)}")
        return False

def lambda_handler(event, context):
    """Process SQS messages and write to DynamoDB."""
    try:
        logger.info(f"Processing {len(event['Records'])} records")
        
        processed = 0
        failed = 0
        
        for record in event['Records']:
            if process_record(record):
                processed += 1
            else:
                failed += 1
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'processed': processed,
                'failed': failed
            }, default=decimal_default)
        }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        raise 