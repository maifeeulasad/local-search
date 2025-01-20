from sentence_transformers import util
from Indexer import Indexer

class Retrieval():
    def __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2", threshold=0.8, keep_attribute=["location"]):
        db_model_name = Indexer.sanitize_key(model_name)
        self.db_model_name = db_model_name
        self.threshold = threshold
        self.keep_attribute = keep_attribute

    def search(self, db, query_embedding, top_k=None):
        # projection = {attribute: 1 for attribute in self.keep_attribute}
        # projection[self.db_model_name] = 1
        documents = db.read_documents({self.db_model_name: {"$exists": True}})#, projection)
        print(documents)
        for doc in documents:
            print(doc)
        print("---------------------------------------")
        embeddings = [doc[self.db_model_name] for doc in documents]
        hits = util.semantic_search(query_embedding, embeddings, top_k=top_k)
        results = [(doc["location"], hit["score"]) for doc, hit in zip(documents, hits[0])]
        return results