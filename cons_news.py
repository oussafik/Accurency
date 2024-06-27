from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import json
from datetime import datetime

# Kafka consumer configuration
bootstrap_servers = '192.168.1.22:9093'  # Replace with your Kafka broker address
topic = 'news'  # Replace with the topic you want to consume from

# Cassandra configuration
cassandra_contact_points = ['127.0.0.1']  # Replace with your Cassandra contact points
cassandra_keyspace = 'stock_market'  # Replace with your desired keyspace name
cassandra_table = 'coins_news2'  # Replace with your desired table name

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
    "headline TEXT,"
    "source TEXT,"
    "timestamp TIMESTAMP"
    ")"
)

# Create Kafka consumer instance
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

# Prepare Cassandra insert query
query = session.prepare(
    f"INSERT INTO {cassandra_table} (id, symbol, headline, source, timestamp) "
    "VALUES (uuid(), :symbol, :headline, :source, :timestamp)"
)

# Start consuming messages
for message in consumer:
    # Parse the received message as JSON
    data = json.loads(message.value.decode())

    # Convert the timestamp to the correct format
    timestamp = datetime.fromisoformat(data['Timestamp'])

    # Insert data into Cassandra
    session.execute(
        query,
        {
            'symbol': data['symbol'],
            'headline': data['Headline'],
            'source': data['Source'],
            'timestamp': timestamp
        }
    )
    print("Sending :", data)

# Close the Kafka consumer, Cassandra session, and cluster connection
consumer.close()
session.shutdown()
cluster.shutdown()