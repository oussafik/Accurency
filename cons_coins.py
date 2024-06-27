from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from datetime import datetime
import json

# Kafka consumer configuration
bootstrap_servers = '192.168.1.22:9093'  # Replace with your Kafka broker address
topic = 'coins'  # Replace with the topic you want to consume from

# Cassandra configuration
cassandra_contact_points = ['127.0.0.1']  # Replace with your Cassandra contact points
cassandra_keyspace = 'stock_market'  # Replace with your desired keyspace name
cassandra_table = 'coins_prices2'  # Replace with your desired table name

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
    "c DOUBLE,"
    "d DOUBLE,"
    "dp DOUBLE,"
    "h DOUBLE,"
    "l DOUBLE,"
    "o DOUBLE,"
    "pc DOUBLE,"
    "t TIMESTAMP"  # Change the type to TIMESTAMP
    ")"
)

# Create Kafka consumer instance
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

# Prepare Cassandra insert query
query = session.prepare(
    f"INSERT INTO {cassandra_table} (id, symbol, c, d, dp, h, l, o, pc, t) "
    "VALUES (uuid(), :symbol, :c, :d, :dp, :h, :l, :o, :pc, :t)"
)

# Start consuming messages
for message in consumer:
    # Parse the received message as JSON
    data = eval(message.value.decode())

    # Convert 't' field to datetime object
    timestamp = datetime.fromtimestamp(data['t'] / 1000.0)

    # Insert data into Cassandra
    session.execute(
        query,
        {
            'symbol': data['symbol'],
            'c': data['c'],
            'd': data['d'],
            'dp': data['dp'],
            'h': data['h'],
            'l': data['l'],
            'o': data['o'],
            'pc': data['pc'],
            't': timestamp
        }
    )
    print("Sending:", data)

# Close the Kafka consumer, Cassandra session, and cluster connection
consumer.close()
session.shutdown()
cluster.shutdown()