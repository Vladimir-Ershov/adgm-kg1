# Knowledge Graph of ADGM Regulations
Regulatory Knowledge Graph built in collaboration with Abu Dhabi Global Market.

# Introduction

In order to automate compliance and RegTech process we've designed an approach aimed to convert human-readable 
regulations into Regulation-As-A-Code: executable rules parsed from texts with the 
help of transformer based LM trained on NER task and relation extraction task. 
This allows us to support the Open World Assumption and have an extendable ontology.
Rules are extracted as a subgraph with GNN thus supplement inference with causality 
reasoning as follows:    

>If an ‘ENT’ with this ‘PERM’ was doing this ‘ACT’ or ‘FS’ with ‘PROD’ using ‘TECH’ then to avoid this ‘RISK’ they should ‘MIT’.

The project status:
1. Design the approach and initial taxonomy for labeling :white_check_mark:
2. Train models to extract entities for graph nodes. :white_check_mark:
3. Train models to extract relations for graph edges.
4. Train GNN for rules extraction

# Models and technologies used to extract current version of the graph  

[NeuralCoref](https://github.com/huggingface/neuralcoref) is used for coreference resolution. 

[Spacy](https://spacy.io) To train NER models for nodes creation and custom `lemmatizer`:

Bert-based NER                                    | Labeled Docs FPR 
---------------------------------------- |:-----------------:
ACT-FS-PROD           | 98.57/98.92/98.23 
TECH |  93.87/94/93.73  
RISK-MIT             | 51.71/47.02/57.43 
PERM   |   93.64/91.01/96.43 
ENT | 99.45/99.34/99.56

POS-Regexp based models                                    | Size | Source
---------------------------------------- |:----:| :----------------:
DEF           | 370  | COBS labeled

There is a stub for relation extraction which is based on the combination of `Spacy` and `NetworkX`

[Neo4J](https://neo4j.com) is used for graph storage, cypher exectution and visualisations


# What has been released in this repository?

# FAQ
TBD

# Disclaimer

# Contact information

