import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define paths to the datasets
ai_governance_dataset_dir = "/home/ubuntu/.cache/kagglehub/datasets/umerhaddii/ai-governance-documents-data/versions/1/agora"
ai_governance_documents_path = os.path.join(ai_governance_dataset_dir, "documents.csv")
epa_dataset_path = "guidance_ow.csv"

def load_and_prepare_data():
    print("Attempting to load AI Governance Documents dataset...")
    ai_governance_df = pd.read_csv(ai_governance_documents_path,
                                   sep=",",
                                   quotechar='"',
                                   on_bad_lines='skip',
                                   encoding='utf-8-sig'
                                  )

    # Combine relevant text columns for AI Governance data
    ai_governance_df["content"] = ai_governance_df["Official name"].fillna("") + ". " + \
                                  ai_governance_df["Short summary"].fillna("") + ". " + \
                                  ai_governance_df["Long summary"].fillna("")
    ai_governance_df["source"] = "Kaggle AI Governance"
    ai_governance_df["URL"] = ai_governance_df["Link to document"]

    # Load EPA dataset
    epa_df = pd.read_csv(epa_dataset_path, on_bad_lines='skip')

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
    print("Initializing RAG agent...")
    documents = load_and_prepare_data()
    if documents.empty:
        print("No documents loaded. Exiting.")
    else:
        print(f"Total documents for RAG: {len(documents)}")
        vectorizer, tfidf_matrix = create_vector_store(documents)
        print("RAG agent ready. Type your query or 'exit' to quit.")

        while True:
            query = input("\nYour query: ")
            if query.lower() == 'exit':
                break

            retrieved_docs = retrieve_documents(query, vectorizer, tfidf_matrix, documents)

            print("\nRetrieved Documents:")
            if retrieved_docs.empty:
                print("No relevant documents found.")
            else:
                for index, row in retrieved_docs.iterrows():
                    print(f"Source: {row['source']}")
                    print(f"Content Snippet: {row['content'][:500]}...") # Limit snippet length
                    print(f"URL: {row['URL']}")
                    print("---")

