'''
# Agentic RAG System for Government Regulations

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about government regulations, using data from Kaggle and the EPA. The system is designed to be a simple, yet effective, tool for searching and retrieving relevant information from a combined corpus of documents.

## Project Overview

The core of this project is a RAG agent that leverages a TF-IDF vector store to find documents relevant to a user's query. The agent then presents snippets of these documents to the user, along with the source and a URL for further reading.

### Data Sources

*   **AI Governance Documents Data:** A Kaggle dataset containing a collection of documents related to AI governance.
*   **EPA Guidance Documents:** A CSV file of guidance documents from the U.S. Environmental Protection Agency (EPA).

### Key Features

*   **Data Ingestion:** Loads and combines data from multiple sources.
*   **Vector Store:** Creates a TF-IDF vector store for efficient document retrieval.
*   **Document Retrieval:** Retrieves the most relevant documents based on a user's query.
*   **Command-Line Interface (CLI):** Provides a simple CLI for interacting with the RAG agent.

## Getting Started

### Prerequisites

*   Python 3.11
*   pip

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

To run the CLI for the RAG agent, execute the following command:

```bash
python3.11 cli_rag_agent.py
```

Once the agent is initialized, you can type your query and press Enter. To exit the agent, type `exit`.

## Project Structure

```
.aixplain_rag_project/
├── cli_rag_agent.py
├── download_ai_governance_dataset.py
├── download_dataset.py
├── guidance_ow.csv
├── inspect_kaggle_csv.py
├── rag_system.py
└── README.md
```

*   `cli_rag_agent.py`: The main script for the command-line interface.
*   `rag_system.py`: The core logic for the RAG system, including data loading, vector store creation, and document retrieval.
*   `download_ai_governance_dataset.py`: A script to download the AI Governance dataset from Kaggle.
*   `download_dataset.py`: A script to download the initial (problematic) Kaggle dataset.
*   `guidance_ow.csv`: The EPA guidance documents.
*   `inspect_kaggle_csv.py`: A script used for debugging the initial Kaggle dataset.
*   `README.md`: This file.

'''
