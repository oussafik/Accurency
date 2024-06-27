from cassandra.cluster import Cluster
import uuid
# Connect to the Cassandra cluster
cluster = Cluster(contact_points=['localhost'])  # Replace 'localhost' with your Cassandra cluster address
session = cluster.connect()

# Create a keyspace
session.execute("CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}")

# Create a table
session.execute("CREATE TABLE IF NOT EXISTS my_keyspace.my_table (id UUID PRIMARY KEY, name TEXT, age INT)")

# Insert data into the table
insert_query = session.prepare("INSERT INTO my_keyspace.my_table (id, name, age) VALUES (?, ?, ?)")

data = [
    {'id': uuid.uuid4(), 'name': 'John Doe', 'age': 25},
    {'id': uuid.uuid4(), 'name': 'Jane Smith', 'age': 30},
    {'id': uuid.uuid4(), 'name': 'Bob Johnson', 'age': 35}
]

for item in data:
    session.execute(insert_query, (item['id'], item['name'], item['age']))

# Close the session and cluster connection
session.shutdown()
cluster.shutdown()