from sentence_transformers import SentenceTransformer

class Indexer():
    def __init__(self, content, model_name):
        self.content = content
        self.model_name = model_name

    def index(self):
        model = SentenceTransformer(self.model_name)
        embeddings = model.encode(self.content, convert_to_tensor=True)
        return embeddings