from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle

# Load environment variables
load_dotenv()

app = FastAPI(title="RAG System API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for the RAG system
vectorizer = None
tfidf_matrix = None
documents = None
DOCUMENTS_COUNT = 0

# Define paths to the datasets
# The user mentioned the data is available, so we will use the paths from the VSCode preview
AIXPLAIN_RAG_SYSTEM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ai_governance_documents_path = os.path.join(AIXPLAIN_RAG_SYSTEM_DIR, "guidance_ow.csv")
# Using guidance_ow.csv as the main data source for simplicity based on the existing files.

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class DocumentResult(BaseModel):
    source: str
    content: str
    url: str

def load_and_prepare_data():
    global vectorizer, tfidf_matrix, documents, DOCUMENTS_COUNT
    print("Loading RAG Documents dataset...")
    
    try:
        # Load the data
        df = pd.read_csv(ai_governance_documents_path)
        
        # Assume the relevant columns are 'source', 'text' and 'url' based on the DocumentResult model
        # The CSV columns are 'Document Name', 'Description/Summary', and 'URL'.
        # We use 'Description/Summary' as the content ('text') to be indexed.
        df = df.dropna(subset=['Description/Summary', 'Document Name', 'URL'])
        
        # Rename columns to match the expected format in the rest of the code
        df = df.rename(columns={'Document Name': 'source', 'Description/Summary': 'text', 'URL': 'url'})
        documents = df.to_dict('records')
        DOCUMENTS_COUNT = len(documents)
        
        # Prepare content for TF-IDF
        corpus = [doc['text'] for doc in documents]
        
        # Initialize and fit TF-IDF Vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        print(f"Data loaded successfully. {DOCUMENTS_COUNT} documents indexed.")
        
    except FileNotFoundError:
        print(f"Data file not found at {ai_governance_documents_path}. Using dummy data.")
        # Fallback for demo if the data is not in the expected path
        documents = [
            {"source": "Dummy Source 1", "text": "This is a dummy document about AI governance.", "url": "http://dummy.url/1"},
            {"source": "Dummy Source 2", "text": "Another document on government regulations.", "url": "http://dummy.url/2"}
        ]
        DOCUMENTS_COUNT = 2
        corpus = [doc['text'] for doc in documents]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        # Initialize with empty data on failure
        documents = []
        DOCUMENTS_COUNT = 0
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([])

@app.on_event("startup")
async def startup_event():
    load_and_prepare_data()

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "documents_loaded": DOCUMENTS_COUNT}

@app.post("/api/search", response_model=list[DocumentResult])
async def search_documents(request: QueryRequest):
    if DOCUMENTS_COUNT == 0:
        raise HTTPException(status_code=503, detail="RAG system is not initialized. No documents loaded.")
    
    query_vector = vectorizer.transform([request.query])
    cosine_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Get the indices of the top_k most similar documents
    top_k_indices = np.argsort(cosine_scores)[-request.top_k:][::-1]
    
    results = []
    for i in top_k_indices:
        doc = documents[i]
        results.append(DocumentResult(
            source=doc['source'],
            content=doc['text'],
            url=doc['url']
        ))
        
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
