import time
import json
import random
import boto3
from faker import Faker
from datetime import datetime

# --- UPDATE THESE WITH YOUR NEW KEYS ---
AWS_ACCESS_KEY = 'Your Access Key'
AWS_SECRET_KEY = 'Your Secret Key'
REGION = 'ap-southeast-2' # Change to 'ap-south-1' if you chose Mumbai
BUCKET_NAME = 'your-bucket'     
# ---------------------------------------

fake = Faker()
s3 = boto3.client(
    's3',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def generate_transaction():
    user = fake.simple_profile()
    transaction = {
        'transaction_id': fake.uuid4(),
        'user_id': user['username'],
        'timestamp': datetime.now().isoformat(),
        'amount': round(random.uniform(10, 1000), 2),
        'currency': 'USD',
        'city': user['address'].split('\n')[1].split(',')[0], 
        'is_fraud_simulated': False
    }

    # Fraud Injection Logic (5% chance)
    if random.random() < 0.05: 
        fraud_burst = []
        is_high_value = random.choice([True, False])

        for _ in range(5):
            fraud_tx = transaction.copy()
            fraud_tx['transaction_id'] = fake.uuid4()
            fraud_tx['timestamp'] = datetime.now().isoformat()
            fraud_tx['is_fraud_simulated'] = True
            
            if is_high_value:
                # Type A: Big amount ($2000+)
                fraud_tx['amount'] = round(random.uniform(2000, 5000), 2)
            else:
                # Type B: Small amount ($10-$50) -> This triggers "Velocity Attack" in SQL
                fraud_tx['amount'] = round(random.uniform(10, 50), 2)
                
            fraud_burst.append(fraud_tx)
        
        return fraud_burst # <--- Returns the list of 5 fraud items
    
    return [transaction] # <--- CRITICAL: You were missing this line!

    # Fraud Injection Logic (5% chance)
    # Fraud Injection Logic (5% chance)
    if random.random() < 0.05: 
        fraud_burst = []
        # Randomly choose: Is this a "High Value" attack or a "Velocity" attack?
        is_high_value = random.choice([True, False])

        for _ in range(5):
            fraud_tx = transaction.copy()
            fraud_tx['transaction_id'] = fake.uuid4()
            fraud_tx['timestamp'] = datetime.now().isoformat()
            fraud_tx['is_fraud_simulated'] = True
            
            if is_high_value:
                # Type A: Big amount ($2000+)
                fraud_tx['amount'] = round(random.uniform(2000, 5000), 2)
            else:
                # Type B: Small amount ($10-$50) -> This triggers "Velocity Attack" in SQL
                fraud_tx['amount'] = round(random.uniform(10, 50), 2)
                
            fraud_burst.append(fraud_tx)
        return fraud_burst

print("🚀 Starting Cloud Stream to AWS S3...")
try:
    while True:
        data_batch = []
        for _ in range(50): 
            result = generate_transaction()
            data_batch.extend(result)
        
        filename = f"transactions_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        
        # CONVERT TO NEWLINE DELIMITED JSON (NDJSON)
        newline_json = '\n'.join([json.dumps(record) for record in data_batch])

        s3.put_object(
    Bucket=BUCKET_NAME,
    Key=f"stream-data/{filename}",
    Body=newline_json # <--- It MUST say newline_json here
)
            
        print(f"✅ Uploaded to S3: {filename}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n🛑 Stopped.")