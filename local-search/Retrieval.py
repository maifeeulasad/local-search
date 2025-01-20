from sentence_transformers import util
from Indexer import Indexer

class Retrieval():
    def __init__(self, db, model_name, threshold=0.8, keep_attribute=["location"]):
        self.db = db
        db_model_name = Indexer.desanitize_key(model_name)
        self.db_model_name = db_model_name
        self.threshold = threshold
        self.keep_attribute = keep_attribute

    def search(self, query_embedding, top_k=None):
        projection = {attribute: 1 for attribute in self.keep_attribute}
        documents = self.db.read_documents({self.db_model_name: {"$exists": True}}, projection)
        embeddings = [doc[self.db_model_name] for doc in documents]
        hits = util.semantic_search(query_embedding, embeddings, top_k=top_k)
        results = [(doc["location"], hit["score"]) for doc, hit in zip(documents, hits[0])]
        return results