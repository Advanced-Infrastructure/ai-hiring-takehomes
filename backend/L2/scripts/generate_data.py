import json
import csv
import os
from datetime import datetime, timedelta
from faker import Faker
import random
import numpy as np

fake = Faker()

def generate_metadata(num_vehicles=50):
    """Generate vehicle metadata."""
    metadata = {}
    regions = ['NYC', 'LA', 'CHI', 'MIA', 'SEA']
    
    for i in range(num_vehicles):
        vehicle_id = f"VH_{str(i+1).zfill(3)}"
        metadata[vehicle_id] = {
            "max_speed": random.randint(80, 120),
            "service_region": random.choice(regions),
            "depot_lat": round(random.uniform(25.0, 45.0), 4),
            "depot_lon": round(random.uniform(-125.0, -65.0), 4)
        }
    
    return metadata

def generate_telemetry(metadata, num_records=100):
    """Generate telemetry data for vehicles."""
    records = []
    vehicle_ids = list(metadata.keys())
    
    # Generate timestamps for the last 24 hours
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    for _ in range(num_records):
        vehicle_id = random.choice(vehicle_ids)
        vehicle_meta = metadata[vehicle_id]
        
        # Generate timestamp
        timestamp = fake.date_time_between(start_date=start_time, end_date=end_time)
        
        # Generate coordinates around depot with some randomness
        lat = vehicle_meta['depot_lat'] + random.uniform(-0.1, 0.1)
        lon = vehicle_meta['depot_lon'] + random.uniform(-0.1, 0.1)
        
        # Generate speed (sometimes exceeding max_speed for testing)
        speed = random.uniform(0, vehicle_meta['max_speed'] * 1.2)
        
        # Generate engine status
        engine_status = 'moving' if speed > 0 else 'idle'
        
        # Generate fuel level
        fuel_level = random.randint(0, 100)
        
        record = {
            'vehicle_id': vehicle_id,
            'timestamp': timestamp.isoformat(),
            'lat': round(lat, 6),
            'lon': round(lon, 6),
            'speed_kmh': round(speed, 2),
            'engine_status': engine_status,
            'fuel_level': fuel_level
        }
        
        records.append(record)
    
    return records

def save_metadata(metadata, output_dir='data'):
    """Save metadata to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'metadata_api.json')
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Saved metadata to {output_path}")

def save_telemetry(records, output_dir='data', chunk_size=20):
    """Save telemetry data to CSV files in chunks."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Split records into chunks
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        output_path = os.path.join(output_dir, f'telemetry_data_{i//chunk_size + 1}.csv')
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=chunk[0].keys())
            writer.writeheader()
            writer.writerows(chunk)
        
        print(f"Saved telemetry chunk to {output_path}")

def main():
    print("Generating synthetic data...")
    
    # Generate metadata
    metadata = generate_metadata()
    save_metadata(metadata)
    
    # Generate telemetry data
    records = generate_telemetry(metadata)
    save_telemetry(records)
    
    print("Data generation complete!")

if __name__ == "__main__":
    main() 