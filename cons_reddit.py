from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from datetime import datetime
import json

# Kafka consumer configuration
bootstrap_servers = '192.168.1.22:9093'  # Replace with your Kafka broker address
topic = 'reddit'  # Replace with the topic you want to consume from

# Cassandra configuration
cassandra_contact_points = ['127.0.0.1']  # Replace with your Cassandra contact points
cassandra_keyspace = 'stock_market2'  # Replace with your desired keyspace name
cassandra_table = 'coins_reddit2'  # Replace with your desired table name

# Connect to the Cassandra cluster
cluster = Cluster(cassandra_contact_points)
session = cluster.connect()

# Create keyspace if it doesn't exist
session.execute(f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}")

# Switch to the keyspace
session.set_keyspace(cassandra_keyspace)

# Create table if it doesn't exist
session.execute(
    f"CREATE TABLE IF NOT EXISTS {cassandra_table} ("
    "id UUID PRIMARY KEY,"
    "symbol TEXT,"
    "text TEXT,"
    "score DOUBLE,"
    "timestamp TIMESTAMP"
    ")"
)

# Create Kafka consumer instance
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

# Prepare Cassandra insert query
query = session.prepare(
    f"INSERT INTO {cassandra_table} (id, symbol, text, score, timestamp) "
    "VALUES (uuid(), ?, ?, ?, ?)"
)

# Start consuming messages
for message in consumer:
    # Parse the received message as JSON
    data = json.loads(message.value.decode())

    # Convert timestamp string to datetime object
    timestamp = datetime.strptime(data['Timestamp'], '%Y-%m-%d %H:%M:%S')

    # Insert data into Cassandra
    session.execute(
        query,
        (data['symbol'], data['Text'], data['Score'], timestamp)
    )
    print("Sending:", data)

# Close the Kafka consumer, Cassandra session, and cluster connection
consumer.close()
session.shutdown()
cluster.shutdown()