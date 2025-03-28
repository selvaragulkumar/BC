# SplitChain Blockchain Storage Simulation

This repository contains a Python implementation of a distributed blockchain storage system based on the SplitChain framework. The code utilizes Neo4j to create a clustered network for data distribution with twin and checksum relationships.

## Features
- Connects to a Neo4j database to manage blockchain data distribution.
- Creates clusters and nodes representing storage units.
- Implements twin and checksum cluster relationships.
- Distributes block data across the network efficiently.

## Requirements
- Python 3.8+
- Neo4j database
- Neo4j Python driver

## Installation
1. Install dependencies:
   ```bash
   pip install neo4j
   ```
2. Ensure Neo4j is running and update the connection credentials in the script:
   ```python
   URI = "bolt://localhost:7687"
   AUTH = ("neo4j", "your_password")
   ```
3. Run the script:
   ```bash
   python script.py
   ```

## Code Overview
### 1. `clear_database()`
Deletes all existing nodes and relationships in the Neo4j database.

### 2. `create_network()`
Creates:
- 4 clusters with 3 nodes each.
- Twin clusters for redundancy.
- Checksum clusters for verification.

### 3. `distribute_block()`
- Assigns full block data to twin clusters.
- Stores checksums in designated clusters.
- Splits block data into segments for other clusters.

## Output
After execution, the script prints `Distribution OK`, indicating successful data distribution.

## Future Enhancements
- Implement data retrieval and verification.
- Add fault tolerance mechanisms.
- Optimize data segmentation logic.

## Authors
Dr. Gunasekeran Raja
Pronoy
Selva Ragul

## License
This project is yet to be published

