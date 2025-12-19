import os
import json
import psycopg2
from confluent_kafka import Consumer

# 1. Configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'redpanda:9092')
DB_HOST = "timescaledb"  # This matches the service name in docker-compose
DB_NAME = os.getenv('POSTGRES_DB', 'sentient_alpha')
DB_USER = os.getenv('POSTGRES_USER', 'admin')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'secretpassword')
DB_PORT = "5432"

# 2. Database Connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

# 3. Kafka Consumer Setup
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'db_writer_group',
    'auto.offset.reset': 'earliest'
}
print(f"🔌 Connecting to Kafka at {KAFKA_BROKER}...")
consumer = Consumer(conf)
consumer.subscribe(['market_trades'])

def main():
    print("💾 DB Writer Started...")
    
    # Connect to DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        print("✅ Connected to Database!")
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    try:
        while True:
            # Poll for message (wait 1 second max)
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # 4. Parse Data
            try:
                data = json.loads(msg.value().decode('utf-8'))
                
                # 5. Insert into TimescaleDB
                # We handle both 'quote' and 'trade' types
                query = """
                    INSERT INTO market_candles (time, symbol, price, volume, type)
                    VALUES (%s, %s, %s, 0, %s);
                """
                
                cur.execute(query, (
                    data['time'], 
                    data['symbol'], 
                    data['price'], 
                    data['type']
                ))
                conn.commit()
                
                print(f"💾 Saved: {data['symbol']} @ {data['price']}")
                
            except Exception as e:
                print(f"❌ Insert Error: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        cur.close()
        conn.close()
        consumer.close()

if __name__ == "__main__":
    main()