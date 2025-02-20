import ollama
import os
import numpy as np
from decouple import config

texts = ["Structured Video Knowledge Indexing","Multi-Modal Retrieval for Comprehensive Responses"]
ollama_client = ollama.Client(host=config("OLLAMA_EMBEDDING_HOST"))
data = ollama_client.embed(model=config("OLLAMA_EMBED_MODEL"), input=texts)
print(data["embeddings"])
np_array = np.array(data["embeddings"])
for e in data["embeddings"]:
    print(type(e))

#new = np.array([dp for dp in data["embeddings"])