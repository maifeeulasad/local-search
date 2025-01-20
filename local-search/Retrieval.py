from sentence_transformers import util
from Indexer import Indexer
import numpy as np

class Retrieval():
    def __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2", threshold=0.8, keep_attribute=["location"]):
        db_model_name = Indexer.sanitize_key(model_name)
        self.db_model_name = db_model_name
        self.threshold = threshold
        self.keep_attribute = keep_attribute

    def search(self, db, query_embedding, top_k=1000):
        documents = db.read_documents({self.db_model_name: {"$exists": True}})
        documents = list(documents)
        embeddings = np.array([doc[self.db_model_name] for doc in documents], dtype = np.float32)
        hits = util.semantic_search(query_embedding, embeddings, top_k=top_k)
        results = [{"location":doc["location"], "score":hit["score"]} for doc, hit in zip(documents, hits[0]) if hit["score"] > self.threshold]
        return results