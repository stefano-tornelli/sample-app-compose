from pywebio.input import input, textarea, input_group, TEXT, TEXTAREA
from pywebio.output import (
    put_text,
    put_error,
    put_buttons,
    put_markdown,
    use_scope,
    put_scope,
    clear,
)
from pywebio import start_server
import requests
import json

# Define the base URL of your Flask API
BASE_URL = "http://flask-backend:5000"


# Functions for each endpoint
def list_databases():
    with use_scope("list_databases_output", clear=True):
        request_dummy = f"{BASE_URL}/list_dbs"
        put_text(request_dummy)


def list_collections():
    with use_scope("list_collections_output", clear=True):
        request_dummy = f"{BASE_URL}/list_collections"
        put_text(request_dummy)


def list_documents(data):
    with use_scope("list_documents_output", clear=True):
        request_dummy = f"{BASE_URL}/list_documents"
        put_text(request_dummy)


def create_collection(data):
    with use_scope("create_collection_output", clear=True):
        request_dummy = f"{BASE_URL}/create_collection"
        put_text(request_dummy)


def insert_document(data):
    try:
        document_json = json.loads(data["document"])  # Validate and parse JSON
        payload = {
            "db_name": data["db_name"],
            "collection_name": data["collection_name"],
            "document": document_json,
        }
        with use_scope("insert_document_output", clear=True):
            request_dummy = f"{BASE_URL}/insert_document {payload}"
            put_text(request_dummy)
    except requests.exceptions.RequestException as e:
        put_error(f"Request failed: {e}")
    except ValueError as e:
        put_error(f"Invalid JSON format: {e}")


def delete_collection(data):
    with use_scope("delete_collection_output", clear=True):
        request_dummy = f"{BASE_URL}/delete_collection"
        put_text(request_dummy)


def delete_database(data):
    with use_scope("delete_database_output", clear=True):
        request_dummy = f"{BASE_URL}/delete_db"
        put_text(request_dummy)


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
            {"label": "Database", "name": "db_name", "type": TEXT, "value": ""},
            {
                "label": "Collection",
                "name": "collection_name",
                "type": TEXT,
                "value": "",
            },
        ],
    },
    {
        "title": "Create a New Collection",
        "action": create_collection,
        "inputs": [
            {"label": "Database Name", "name": "db_name", "type": TEXT, "value": ""},
            {
                "label": "Collection Name",
                "name": "collection_name",
                "type": TEXT,
                "value": "",
            },
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
                "type": TEXTAREA,
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


def create_section(section):
    # Section title
    put_text(section["title"])

    print(f"Creating section {section['title']}")

    # Separator
    put_markdown("---")

    # Input form
    inputs = section["inputs"]
    print(f"Inputs {section['inputs']}")

    if inputs:
        input_list = [
            input(
                input_item["label"],
                name=input_item["name"],
                type=input_item.get("type", TEXT),
                value=input_item.get("value", ""),
            )
            for input_item in inputs
        ]
    else:
        input_list = []

    # Output scope for this section
    scope_id = f"output_{section['title'].replace(' ', '_')}"
    put_scope(scope_id)

    # Callable function for the send button
    def send():
        input_values = {}
        if input_list:
            input_values = input_group(f"{section['title']} Inputs", input_list)

        clear(scope_id)  # Clear the previous output
        result_text = section["action"](**input_values)
        put_text(result_text, scope=scope_id)

    # Send button
    put_buttons(
        [dict(label="Send", value="send", color="primary")], onclick=lambda _: send()
    )


def main():
    for section in sections:
        create_section(section)


if __name__ == "__main__":
    start_server(main, port=8089, debug=True)
