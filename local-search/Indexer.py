from sentence_transformers import SentenceTransformer
from FileParser import FileParser

class Indexer():
    sanitize_key_value = "__meaw__woof__"

    def __init__(self, file_path, model_name = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.file_path = file_path
        self.model_name = model_name

    @staticmethod
    def sanitize_key(key):
        return key.replace("/", Indexer.sanitize_key_value)

    @staticmethod
    def desanitize_key(key):
        return key.replace(Indexer.sanitize_key_value, "/")

    def embed(self, content):
        model = SentenceTransformer(self.model_name)
        embedding = model.encode(content)
        return embedding
    
    def index(self, db):
        content = FileParser(self.file_path).parse()
        embedding = self.embed(content)
        model_name_sanitized = Indexer.sanitize_key(self.model_name)
        sample_document = {"location": self.file_path, model_name_sanitized: embedding.tolist()}
        db.insert_document(sample_document)