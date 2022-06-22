# Neo4j dump

The simplest way to setup the knowledge graph is to restore it from the `kg2_release.dump` with [Neo4j](https://neo4j.com/)
Just add the dump file in the Files section and select the `Create new DBMS from dump` option.

# Raw cypher queries

`Raw` folder contains pickled cypher queries which were used to construct the graph. 
The ```src/upload_pkl_to_neo4j.py``` contains example on how to use them directly. 