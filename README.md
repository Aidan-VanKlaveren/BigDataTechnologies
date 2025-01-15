# Tweets Dataset Processing and Big Data Integration Project

This repository contains assignments and projects focused on cleaning a large dataset of tweets, creating a graph database using Neo4j, running graph algorithms, and integrating big data workflows with Google BigQuery using Apache Airflow DAGs.

---

## 📂 Project Structure

### **1. Tweets Dataset and Neo4j Integration**
- **`10000tweets1`**: Dataset of 10,000 tweets used for graph database creation.
- **Neo4j Scripts:**
  - **`Assignment2Part2Imports.py`**: Imports the cleaned tweets dataset into Neo4j.
  - **`Assignment2Part3Queries.py`**: Contains Cypher queries to analyze and explore the graph database.
  - **`Assignment2bigdatatechnologies.py`**: Implements various graph algorithms, such as PageRank and community detection, using Neo4j.

### **2. DAG Creation and BigQuery Integration**
- **`bigquery_operator_dag.py`**: An Apache Airflow Directed Acyclic Graph (DAG) script to connect and interact with Google BigQuery for data processing and storage.

### **3. Documentation**
- **`Assignment3Queries.docx`**: Detailed documentation of the Cypher queries and their results, including insights gained from the graph database.
- **`youtube link.txt`**: Link to a demonstration video or walkthrough of the project.

### **4. Compressed Files**
- **`Assignment2AidanVanKlaveren.rar`**: Contains supplementary files or backup resources for Assignment 2.

---

## 🚀 Features

### **Neo4j Graph Database**
- Import and clean a tweets dataset.
- Create nodes and relationships for meaningful graph representation.
- Execute graph algorithms such as:
  - **PageRank:** Analyze influence within the network.
  - **Community Detection:** Identify clusters of related tweets or users.

### **Google BigQuery and DAG Integration**
- Define a workflow using Apache Airflow to interact with Google BigQuery.
- Process and analyze data efficiently using DAGs.
- Integrate with cloud-based solutions for scalable data management.

---

## 🛠️ Tools and Technologies

- **Graph Database:** Neo4j, Cypher Query Language
- **Big Data Integration:** Google BigQuery, Apache Airflow
- **Programming Language:** Python
- **Other Tools:** Jupyter Notebooks, Text Editors, and BigQuery Console

---

## 🔍 Use Cases

1. **Graph Database Exploration:**
   - Represent and analyze relationships between tweets, users, and hashtags.
   - Use graph algorithms to gain insights into network structure and influential entities.

2. **Big Data Processing:**
   - Create scalable workflows for analyzing and storing large datasets.
   - Integrate with cloud-based data platforms for advanced analytics.

---

## 📜 Getting Started

1. **Neo4j Setup:**
   - Download and install Neo4j Desktop or set up a Neo4j Aura instance.
   - Run the scripts in `Assignment2Part2Imports.py` and `Assignment2Part3Queries.py` to set up the graph and execute queries.

2. **BigQuery Integration:**
   - Set up Apache Airflow and Google Cloud credentials.
   - Deploy the `bigquery_operator_dag.py` script to define and execute your workflow.

3. **Dependencies:**
   Install the required Python libraries:
   ```bash
   pip install neo4j airflow google-cloud-bigquery
