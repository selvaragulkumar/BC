from neo4j import GraphDatabase
import random

# Connect to Neo4j Database
URI = "bolt://localhost:7687"  # Update if needed
AUTH = ("neo4j", "root1234")  # Update with your credentials

driver = GraphDatabase.driver(URI, auth=AUTH)

def clear_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

def create_network():
    clusters = 4  # Updated to even number of clusters
    nodes_per_cluster = 3
    
    # Define twin and checksum clusters ensuring all are unique
    cluster_pairs = {0: 1, 1: 0, 2: 3, 3: 2}  # Twin clusters
    checksum_clusters = {0: 2, 1: 3, 2: 0, 3: 1}  # Checksum clusters
    
    with driver.session() as session:
        for c in range(clusters):
            session.run("CREATE (:Cluster {id: $id})", id=c)
            for n in range(nodes_per_cluster):
                session.run(
                    "MATCH (c:Cluster {id: $cluster_id}) "
                    "CREATE (n:Node {id: $node_id})-[:BELONGS_TO]->(c)",
                    cluster_id=c, node_id=f"{c}-{n}"
                )
        
        # Connect clusters based on twin and checksum relationships
        for c, twin in cluster_pairs.items():
            session.run("MATCH (a:Cluster {id: $c}), (b:Cluster {id: $twin}) CREATE (a)-[:TWIN]->(b)", c=c, twin=twin)
        for c, checksum in checksum_clusters.items():
            session.run("MATCH (a:Cluster {id: $c}), (b:Cluster {id: $checksum}) CREATE (a)-[:CHECKSUM]->(b)", c=c, checksum=checksum)
    
    return cluster_pairs, checksum_clusters

def distribute_block(cluster_pairs, checksum_clusters):
    block_data = "BLOCK_DATA"
    checksum_value = "CHECKSUM"
    clusters = list(cluster_pairs.keys())
    
    with driver.session() as session:
        # Send full block to twin clusters
        for c, twin in cluster_pairs.items():
            node = session.run(
                "MATCH (n:Node)-[:BELONGS_TO]->(c:Cluster {id: $cluster_id}) "
                "RETURN n.id ORDER BY rand() LIMIT 1",
                cluster_id=c
            ).single()["n.id"]
            session.run("MATCH (n:Node {id: $node_id}) SET n.data = $data", node_id=node, data=block_data)
        
        # Send checksum to checksum clusters
        for c, checksum in checksum_clusters.items():
            node = session.run(
                "MATCH (n:Node)-[:BELONGS_TO]->(c:Cluster {id: $cluster_id}) "
                "RETURN n.id ORDER BY rand() LIMIT 1",
                cluster_id=checksum
            ).single()["n.id"]
            session.run("MATCH (n:Node {id: $node_id}) SET n.data = $data", node_id=node, data=checksum_value)
        
        # Split data into segments for remaining clusters
        remaining_clusters = [c for c in clusters if c not in cluster_pairs and c not in checksum_clusters.values()]
        segment_size = len(block_data) // len(remaining_clusters) if remaining_clusters else len(block_data)
        for i, c in enumerate(remaining_clusters):
            segment = block_data[i * segment_size:(i + 1) * segment_size]
            node = session.run(
                "MATCH (n:Node)-[:BELONGS_TO]->(c:Cluster {id: $cluster_id}) "
                "RETURN n.id ORDER BY rand() LIMIT 1",
                cluster_id=c
            ).single()["n.id"]
            session.run("MATCH (n:Node {id: $node_id}) SET n.data = $data", node_id=node, data=segment)
    
    return "Distribution OK"

# Run the simulation
clear_database()
cluster_pairs, checksum_clusters = create_network()
result = distribute_block(cluster_pairs, checksum_clusters)
print(result)

driver.close()
