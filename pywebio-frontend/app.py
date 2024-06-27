from pywebio.input import input, textarea, input_group
from pywebio.output import (
    put_text,
    put_error,
    put_code,
    put_buttons,
    put_markdown,
    use_scope,
)
from pywebio import start_server
import requests
import json

# Define the base URL of your Flask API
BASE_URL = "http://flask-backend:5000"


# Functions for each endpoint
def list_databases():
    with use_scope("list_databases_output", clear=True):
        response = requests.get(f"{BASE_URL}/list_dbs")
        put_code(response.json(), "json")


def list_collections():
    with use_scope("list_collections_output", clear=True):
        response = requests.get(f"{BASE_URL}/list_collections")
        put_code(response.json(), "json")


def list_documents(data):
    with use_scope("list_documents_output", clear=True):
        response = requests.get(f"{BASE_URL}/list_documents", json=data)
        put_code(response.json(), "json")


def create_collection(data):
    with use_scope("create_collection_output", clear=True):
        response = requests.post(f"{BASE_URL}/create_collection", json=data)
        put_code(response.json(), "json")


def insert_document(data):
    try:
        document_json = json.loads(data["document"])  # Validate and parse JSON
        payload = {
            "db_name": data["db_name"],
            "collection_name": data["collection_name"],
            "document": document_json,
        }
        with use_scope("insert_document_output", clear=True):
            response = requests.post(f"{BASE_URL}/insert_document", json=payload)
            put_code(response.json(), "json")
    except requests.exceptions.RequestException as e:
        put_error(f"Request failed: {e}")
    except ValueError as e:
        put_error(f"Invalid JSON format: {e}")


def delete_collection(data):
    with use_scope("delete_collection_output", clear=True):
        response = requests.delete(f"{BASE_URL}/delete_collection", json=data)
        put_code(response.json(), "json")


def delete_database(data):
    with use_scope("delete_database_output", clear=True):
        response = requests.delete(
            f"{BASE_URL}/delete_db", json={"db_name": data["db_name"]}
        )
        put_code(response.json(), "json")


# Configuration dictionary for each section
sections = [
    {
        "title": "List Databases",
        "action": list_databases,
        "inputs": [],
    },
    {
        "title": "List Collections",
        "action": list_collections,
        "inputs": [],
    },
    {
        "title": "List Documents",
        "action": list_documents,
        "inputs": [
            {"label": "Database", "name": "db_name"},
            {"label": "Collection", "name": "collection_name"},
        ],
    },
    {
        "title": "Create a New Collection",
        "action": create_collection,
        "inputs": [
            {"label": "Database Name", "name": "db_name"},
            {"label": "Collection Name", "name": "collection_name"},
        ],
    },
    {
        "title": "Insert a New Document",
        "action": insert_document,
        "inputs": [
            {"label": "Database Name", "name": "db_name"},
            {"label": "Collection Name", "name": "collection_name"},
            {
                "label": "Document (JSON format)",
                "name": "document",
                "type": textarea,
                "value": '{"name": "John Doe", "age": 30}',
            },
        ],
    },
    {
        "title": "Delete a Collection",
        "action": delete_collection,
        "inputs": [
            {"label": "Database Name", "name": "db_name"},
            {"label": "Collection Name", "name": "collection_name"},
        ],
    },
    {
        "title": "Delete a Database",
        "action": delete_database,
        "inputs": [
            {"label": "Database Name to Delete", "name": "db_name"},
        ],
    },
]


def render_section(section):
    put_markdown(f"### {section['title']}")

    if section["inputs"]:
        inputs = [input(**inp) for inp in section["inputs"]]
        data = input_group(section["title"], inputs)
        put_buttons(["Send"], onclick=[lambda d=data: section["action"](d)])
    else:
        put_buttons(["Send"], onclick=[section["action"]])

    with use_scope(f"{section['title'].replace(' ', '_').lower()}_output"):
        pass
    put_markdown("---")


def main():
    put_text("MongoDB Flask API Tester")

    for section in sections:
        render_section(section)


if __name__ == "__main__":
    start_server(main, port=8081)
