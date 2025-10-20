import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
AIXPLAIN_API_KEY = os.getenv("AIXPLAIN_API_KEY")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define paths to the datasets
ai_governance_dataset_dir = "data/ai-governance-documents-data/agora"
ai_governance_documents_path = os.path.join(os.getcwd(), ai_governance_dataset_dir, "documents.csv")
epa_dataset_path = "guidance_ow.csv"

def load_and_prepare_data():
    print("Attempting to load AI Governance Documents dataset...")
    ai_governance_df = pd.read_csv(ai_governance_documents_path,
                                   sep=",",
                                   quotechar='"',
                                   on_bad_lines='skip',
                                   encoding='utf-8-sig'
                                  )

    print("\nAI Governance DataFrame columns after initial load:\n", ai_governance_df.columns.tolist())
    print("\nAI Governance DataFrame head after initial load:\n")
    print(ai_governance_df.head())

    # Load EPA dataset
    epa_df = pd.read_csv(epa_dataset_path, on_bad_lines='skip')

    # Combine relevant text columns for AI Governance data
    ai_governance_df["content"] = ai_governance_df["Official name"].fillna("") + ". " + \
                                  ai_governance_df["Short summary"].fillna("") + ". " + \
                                  ai_governance_df["Long summary"].fillna("")
    ai_governance_df["source"] = "Kaggle AI Governance"
    ai_governance_df["URL"] = ai_governance_df["Link to document"]

    # Combine relevant text columns for EPA data
    epa_df["content"] = epa_df["Document Name"].fillna("") + ". " + \
                        epa_df["Description/Summary"].fillna("")
    epa_df["source"] = "EPA Guidance"
    epa_df["URL"] = "N/A"

    # Select relevant columns and combine
    ai_governance_subset = ai_governance_df[["content", "source", "URL"]]
    epa_subset = epa_df[["content", "source", "URL"]]

    combined_df = pd.concat([ai_governance_subset, epa_subset], ignore_index=True)
    combined_df = combined_df.dropna(subset=["content"])
    print(f"Combined DataFrame created. Shape: {combined_df.shape}")

    return combined_df

def create_vector_store(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents["content"])
    return vectorizer, tfidf_matrix

def retrieve_documents(query, vectorizer, tfidf_matrix, documents, top_k=5):
    query_vec = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-top_k-1:-1]
    return documents.iloc[related_docs_indices]

if __name__ == "__main__":
    print("Loading and preparing data...")
    if not AIXPLAIN_API_KEY:
        print("AIXPLAIN_API_KEY not found. Please set it in a .env file.")
        exit()
    documents = load_and_prepare_data()
    if not documents.empty:
        print(f"Total documents for RAG: {len(documents)}")

        print("Creating TF-IDF vector store...")
        vectorizer, tfidf_matrix = create_vector_store(documents)
        print("Vector store created.")

        # Example usage
        query = "regulations on artificial intelligence ethics"
        print(f"\nSearching for documents related to: {query}")
        retrieved_docs = retrieve_documents(query, vectorizer, tfidf_matrix, documents)

        print("\nRetrieved Documents:")
        for index, row in retrieved_docs.iterrows():
            print(f"Source: {row['source']}")
            print(f"Content Snippet: {row['content'][:200]}...")
            print(f"URL: {row['URL']}")
            print("---")

        query = "water quality standards for PFAS"
        print(f"\nSearching for documents related to: {query}")
        retrieved_docs = retrieve_documents(query, vectorizer, tfidf_matrix, documents)

        print("\nRetrieved Documents:")
        for index, row in retrieved_docs.iterrows():
            print(f"Source: {row['source']}")
            print(f"Content Snippet: {row['content'][:200]}...")
            print(f"URL: {row['URL']}")
            print("---")
