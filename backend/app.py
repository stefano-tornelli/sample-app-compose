import os
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from pymongo import MongoClient
from swagger.config import template

app = Flask(__name__)
Swagger(app, template=template)

# Configure MongoDB mongodb_client
# Use the MONGO_URI environment variable
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongodb_client = MongoClient(mongo_uri)


@app.route("/create_collection", methods=["POST"])
@swag_from(
    "swagger/create_collection.yml",
    validation=False,
    endpoint="create_collection",
    methods=["POST"],
)
def create_collection():
    db_name = request.json.get("db_name")
    collection_name = request.json.get("collection_name")
    if db_name and collection_name:
        db = mongodb_client[db_name]
        db.create_collection(collection_name)
        return (
            jsonify(
                message=f"Collection {collection_name} created in database {db_name}"
            ),
            200,
        )
    return jsonify(message="Database name and collection name are required"), 400


@app.route("/insert_document", methods=["POST"])
@swag_from(
    "swagger/insert_document.yml",
    validation=False,
    endpoint="insert_document",
    methods=["POST"],
)
def insert_document():
    db_name = request.json.get("db_name")
    collection_name = request.json.get("collection_name")
    document = request.json.get("document")
    if db_name and collection_name and document:
        db = mongodb_client[db_name]
        collection = db[collection_name]
        collection.insert_one(document)
        return jsonify(message="Document inserted successfully"), 200
    return (
        jsonify(message="Database name, collection name, and document are required"),
        400,
    )


@app.route("/list_dbs", methods=["GET"])
@swag_from(
    "swagger/list_dbs.yml",
    validation=False,
    endpoint="list_dbs",
    methods=["GET"],
)
def list_dbs():
    list_db_names = mongodb_client.list_database_names()
    return (
        jsonify(message=f"Existing Databases {list_db_names}"),
        400,
    )


@app.route("/list_collections", methods=["GET"])
@swag_from(
    "swagger/list_collections.yml",
    validation=False,
    endpoint="list_collections",
    methods=["GET"],
)
def list_collections():
    dict_collection_names = {
        db_name: mongodb_client[db_name].list_collection_names()
        for db_name in mongodb_client.list_database_names()
    }

    return (
        jsonify(message=f"Existing Collections {dict_collection_names}"),
        400,
    )


@app.route("/list_documents", methods=["GET"])
@swag_from(
    "swagger/list_documents.yml",
    validation=False,
    endpoint="list_documents",
    methods=["GET"],
)
def list_documents():
    db_name = request.json.get("db_name")
    collection_name = request.json.get("collection_name")

    # # Retrieve all documents from the collection
    # list_documents = [doc['_id'] for doc in mongodb_client[db_name][collection_name].find({}, {"_id": 1})]
    list_documents = list(mongodb_client[db_name][collection_name].find())

    return (
        jsonify(
            message=f"Existing Documents in DB {db_name} and Collection {collection_name}: \n {list_documents}"
        ),
        400,
    )


@app.route("/delete_collection", methods=["DELETE"])
@swag_from(
    "swagger/delete_collection.yml",
    validation=False,
    endpoint="delete_collection",
    methods=["DELETE"],
)
def delete_collection():
    db_name = request.json.get("db_name")
    collection_name = request.json.get("collection_name")
    if db_name and collection_name:
        db = mongodb_client[db_name]
        db.drop_collection(collection_name)
        return (
            jsonify(
                message=f"Collection {collection_name} deleted from database {db_name}"
            ),
            200,
        )
    return jsonify(message="Database name and collection name are required"), 400


@app.route("/delete_db", methods=["DELETE"])
@swag_from(
    "swagger/delete_db.yml", validation=False, endpoint="delete_db", methods=["DELETE"]
)
def delete_db():
    db_name = request.json.get("db_name")
    if db_name:
        mongodb_client.drop_database(db_name)
        return jsonify(message=f"Database {db_name} deleted successfully"), 200
    return jsonify(message="Database name is required"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
