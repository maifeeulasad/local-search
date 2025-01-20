from flask import Flask, request, jsonify
from flask_cors import CORS
from Database import Database
from Indexer import Indexer
from Retrieval import Retrieval

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb://mongodbusername:mongodbpassword@localhost:27017"
DATABASE_NAME = "local-search"
COLLECTION_NAME = "embedding"

model_path = "sentence-transformers/all-MiniLM-L6-v2"

# curl -X POST -H "Content-Type: application/json" -d '{"file_paths": ["../assets/a.txt", "../assets/b.txt", "../assets/c.txt"]}' http://localhost:5000/index
@app.route('/index', methods=['POST'])
def index_files():
    file_paths = request.json.get('file_paths', [])
    with Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME) as db:
        for file_path in file_paths:
            Indexer(file_path, model_path).index(db)
    return jsonify({"message": "Files indexed successfully"}), 200

# curl -X POST -H "Content-Type: application/json" -d '{"query": "I am a cat", "threshold": 0.1}' http://localhost:5000/search
@app.route('/search', methods=['POST'])
def search_query():
    query = request.json.get('query', '')
    threshold = request.json.get('threshold', 0.0)
    query_embedded = Indexer.embed(query)
    with Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME) as db:
        results = Retrieval(threshold=threshold).search(db, query_embedded)
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')