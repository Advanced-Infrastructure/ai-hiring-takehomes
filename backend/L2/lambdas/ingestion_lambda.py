import csv
import io
import json
import os
import boto3
import redis
from haversine import haversine
import logging
import tracemalloc
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
from io import StringIO

# Environment variables
SQS_MOVING_QUEUE_URL = os.environ.get("HIGH_PRIORITY_QUEUE_URL")
SQS_IDLE_QUEUE_URL = os.environ.get("LOW_PRIORITY_QUEUE_URL")
REDIS_ENDPOINT = os.environ.get("REDIS_ENDPOINT")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
METADATA_CACHE_KEY = "metadata_api"
METADATA_TTL = 3600  # seconds

# Initialize AWS clients and Redis
s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')
redis_client = redis.Redis(host=REDIS_ENDPOINT, port=REDIS_PORT, decode_responses=True)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def validate_coordinates(lat, lon):
    """Validate if coordinates are within valid ranges."""
    try:
        lat = float(lat)
        lon = float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, TypeError):
        return False

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    try:
        # Validate coordinates
        if not all(validate_coordinates(lat, lon) for lat, lon in [(lat1, lon1), (lat2, lon2)]):
            logger.error(f"Invalid coordinates: ({lat1}, {lon1}) or ({lat2}, {lon2})")
            return None

        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        logger.info(f"Calculated distance: {round(distance, 2)} km between ({lat1}, {lon1}) and ({lat2}, {lon2})")
        return round(distance, 2)
    except Exception as e:
        logger.error(f"Error calculating distance: {str(e)}")
        return None

def get_metadata_from_cache(vehicle_id):
    """Get vehicle metadata from Redis cache."""
    try:
        metadata = redis_client.get(vehicle_id)
        if metadata:
            return json.loads(metadata)
        
        # Use default values if not found
        default_metadata = {
            'max_speed': 120,  # Default max speed 120 km/h
            'depot_lat': 12.9716,  # Default Bangalore coordinates
            'depot_lon': 77.5946,
            'service_region': 'default'
        }
        
        # Cache the default values
        redis_client.setex(
            vehicle_id,
            timedelta(hours=1),
            json.dumps(default_metadata)
        )
        return default_metadata
        
    except Exception as e:
        logger.error(f"Error getting metadata: {str(e)}")
        # Return default values even on error
        return {
            'max_speed': 120,
            'depot_lat': 12.9716,
            'depot_lon': 77.5946,
            'service_region': 'default'
        }

def process_csv_file(bucket, key):
    """Process CSV file in streaming mode."""
    try:
        # Start memory tracking
        tracemalloc.start()
        current, peak = tracemalloc.get_traced_memory()
        logger.info(f"Initial memory usage: {current / 10**6}MB")
        
        # Get the file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        lines = StringIO(response['Body'].read().decode('utf-8'))
        
        # Create CSV reader
        reader = csv.DictReader(lines)
        
        # Process each row
        for row in reader:
            try:
                # Get metadata
                metadata = get_metadata_from_cache(row['vehicle_id'])
                if not metadata:
                    logger.warning(f"No metadata found for vehicle {row['vehicle_id']}")
                    continue
                
                # Validate speed
                speed = float(row['speed_kmh'])
                if speed > metadata['max_speed']:
                    logger.info(f"Skipping row: Speed {speed} exceeds max ({metadata['max_speed']}) for vehicle {row['vehicle_id']}")
                    continue
                
                # Calculate distance from depot
                distance = calculate_distance(
                    float(row['lat']),
                    float(row['lon']),
                    metadata['depot_lat'],
                    metadata['depot_lon']
                )
                
                if distance is None:
                    logger.warning(f"Could not calculate distance for vehicle {row['vehicle_id']}, skipping row")
                    continue
                
                # Prepare message
                message = {
                    **row,
                    'distance_from_depot': distance,
                    'service_region': metadata['service_region'],
                    'processed_at': datetime.now().isoformat()
                }
                
                # Choose queue based on engine status
                queue_url = SQS_MOVING_QUEUE_URL if row['engine_status'] == 'moving' else SQS_IDLE_QUEUE_URL
                
                # Send to SQS
                response = sqs_client.send_message(
                    QueueUrl=queue_url,
                    MessageBody=json.dumps(message)
                )
                
                logger.info(f"Message sent to SQS ({queue_url}) with MessageId: {response['MessageId']}")
                
            except Exception as e:
                logger.error(f"Error processing row: {str(e)}")
                continue
        
        # Log memory usage
        current, peak = tracemalloc.get_traced_memory()
        logger.info(f"Peak memory usage: {peak / 10**6}MB")
        tracemalloc.stop()
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise

def lambda_handler(event, context):
    """Process S3 events and send data to SQS."""
    try:
        logger.info(f"Lambda triggered with event: {json.dumps(event)}")
        
        # Get metadata from Redis
        logger.info("Metadata retrieved from Redis cache.")
        
        # Process each record (S3 file)
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            logger.info(f"Processing file: s3://{bucket}/{key}")
            process_csv_file(bucket, key)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Processing complete')
        }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        raise 