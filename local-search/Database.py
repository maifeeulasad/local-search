from pymongo import MongoClient

class Database():
    def __init__(self, mongo_uri, database_name, collection_name):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.collection_name = collection_name
        
    def insert_document(self, document):
        return self.collection.insert_one(document)

    def read_documents(self, query=None):
        return self.collection.find(query)

    def update_documents(self, query, update_values):
        return self.collection.update_many(query, {"$set": update_values})

    def delete_documents(self, query):
        return self.collection.delete_many(query)

    def close_connection(self):
        self.client.close()

    def connect_to_mongo(self, uri):
        try:
            client = MongoClient(uri)
            return client
        except Exception as e:
            return None

    def create_database_and_collection(self, client, db_name, collection_name):
        db = client[db_name]

        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)

        return db[collection_name]
    
    def __enter__(self):
        self.client = self.connect_to_mongo(self.mongo_uri)
        self.collection = self.create_database_and_collection(self.client, self.database_name, self.collection_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
        return True



'''
# Usage, don't delete this
if __name__ == "__main__":
    MONGO_URI = "mongodb://mongodbusername:mongodbpassword@localhost:27017"
    DATABASE_NAME = "local-search"
    COLLECTION_NAME = "embedding"
    
    with Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME) as db:

        # 1. Create
        print("Inserting a document:")
        sample_document = {"name": "Alice", "age": 30, "city": "Wonderland"}
        print(db.insert_document(sample_document))

        # 2. Read
        print("\nReading all documents:")
        print(db.read_documents())

        # 3. Update
        print("\nUpdating documents:")
        update_query = {"name": "Alice"}
        update_values = {"age": 35}
        print(db.update_documents(update_query, update_values))

        # Verify the update
        print("\nReading updated documents:")
        print(db.read_documents({"name": "Alice"}))

        # 4. Delete
        print("\nDeleting documents:")
        delete_query = {"name": "Alice"}
        print(db.delete_documents(delete_query))

        # Verify deletion
        print("\nReading all documents after deletion:")
        print(db.read_documents())
'''