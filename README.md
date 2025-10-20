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

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/omar-qasem/AIxplain-RAG-System.git
    cd AIxplain-RAG-System
    ```

2.  **Install Required Packages**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Datasets**:

    *   **AI Governance Documents Data**: This dataset needs to be downloaded manually from Kaggle.
        1.  Go to the Kaggle dataset page: [AI Governance Documents Data](https://www.kaggle.com/datasets/umerhaddii/ai-governance-documents-data)
        2.  Download the `documents.csv` file.
        3.  Create the following directory structure within your `AIxplain-RAG-System` folder:
            `data/ai-governance-documents-data/agora/`
        4.  Place the downloaded `documents.csv` file into the `agora` folder.

    *   **EPA Guidance Documents**: The `guidance_ow.csv` file is already included in the repository.

### 🔑 API Key Setup

1.  Get your aiXplain API key from [aixplain.com](https://aixplain.com)
2.  Create a `.env` file in the project root by copying the example:

    ```bash
    cp .env.example .env
    ```

3.  Open the newly created `.env` file and paste your actual aiXplain API key:

    ```env
    AIXPLAIN_API_KEY=your_actual_key_here
    ```

    **Note**: Replace `your_actual_key_here` with the key you obtained from aiXplain. This file is ignored by Git to keep your key secure.

### Usage

To run the CLI for the RAG agent, execute the following command:

```bash
python cli_rag_agent.py
# OR (if 'python' doesn't work)
py cli_rag_agent.py
```

Once the agent is initialized, you can type your query and press Enter. To exit the agent, type `exit`.

## Project Structure

```
AIxplain-RAG-System/
├── data/
│   └── ai-governance-documents-data/
│       └── agora/
│           └── documents.csv
├── .env.example
├── .gitignore
├── cli_rag_agent.py
├── download_ai_governance_dataset.py
├── download_dataset.py
├── guidance_ow.csv
├── inspect_kaggle_csv.py
├── rag_system.py
├── README.md
└── requirements.txt
```

*   `cli_rag_agent.py`: The main script for the command-line interface.
*   `rag_system.py`: The core logic for the RAG system, including data loading, vector store creation, and document retrieval.
*   `download_ai_governance_dataset.py`: A script to download the AI Governance dataset from Kaggle.
*   `download_dataset.py`: A script to download the initial (problematic) Kaggle dataset.
*   `guidance_ow.csv`: The EPA guidance documents.
*   `inspect_kaggle_csv.py`: A script used for debugging the initial Kaggle dataset.
*   `README.md`: This file.

