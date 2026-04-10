
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed text
def embed(text):
    return model.encode(text)

# Simulated pgvector search
def search_pgvector(query, vectors):
    q = embed(query)
    sims = [np.dot(q, v) for v in vectors]
    return np.argmax(sims)

# Simulated Pinecone search
def search_pinecone(query, index_vectors):
    q = embed(query)
    sims = [(i, np.dot(q, v)) for i, v in enumerate(index_vectors)]
    sims.sort(key=lambda x: x[1], reverse=True)
    return sims[:5]
