from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class MongoDBHandler:
    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB connection."""
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """Establish connection to MongoDB."""
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

    def close(self):
        """Close the connection to MongoDB."""
        if self.client:
            self.client.close()

    def get_all_documents(self, collection_name: str):
        """Fetch all documents and their count from the specified collection."""
        try:
            collection = self.db[collection_name]
            documents = list(collection.find())  # Fetch all documents
            count = collection.count_documents({})  # Get the count of documents
            
            return documents, count
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            return [], 0
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return [], 0

    def update_document(self, collection_name: str, filter_criteria: dict, update_values: dict):
        """Update a document in the specified collection based on filter criteria."""
        try:
            collection = self.db[collection_name]
            result = collection.update_one(filter_criteria, {"$set": update_values})
            return result.modified_count  # Return the number of modified documents
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            return 0
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return 0

mongo_uri="YOUR_KEY"
db_name= "theory_of_change_db"
collection_name= "toc_data"

# Function to use MongoDBHandler to get all documents
def fetch_all_documents():
    mongo_handler = MongoDBHandler(mongo_uri, db_name)
    mongo_handler.connect()
    documents, count = mongo_handler.get_all_documents(collection_name)
    mongo_handler.close()
    return documents

# Function to use MongoDBHandler to update a document
def insert_data_to_database(data):
    mongo_uri = "YOUR_KEY"
    db_name = "theory_of_change_db"
    
    # Create a MongoDB client and connect to the database
    mongo_handler = MongoDBHandler(mongo_uri, db_name)
    mongo_handler.connect()

    # Get the collection (make sure 'toc_data' is the correct collection name)
    collection = mongo_handler.db.toc_data  # Assuming mongo_handler has a db attribute

    # Insert the data into the collection
    collection.insert_one(data)

    # Close the MongoDB connection
    mongo_handler.close()
def create_mongo_vectordb():
    documents=fetch_all_documents()
    text=""
    for document in documents:
        dq=" question:"+document['query']
        da=" answer:"+document['response']
        text+=dq+da
    return text

