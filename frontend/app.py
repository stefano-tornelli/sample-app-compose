import streamlit as st
import requests
import json

# Define the base URL of your Flask API
BASE_URL = "http://flask-backend:5000"

st.title("MongoDB Flask API Tester")

# List DBs
st.header("List Databases")
if st.button("List Databases"):
    response = requests.get(f"{BASE_URL}/list_dbs")
    st.json(response.json())

# List Collections
st.header("List Collections")
if st.button("List Collections"):
    response = requests.get(f"{BASE_URL}/list_collections")
    st.json(response.json())

# List Documents
st.header("List Documents")
db_name_for_collection = st.text_input("Database")
collection_name = st.text_input("Collection")
if st.button("List Documents"):
    response = requests.get(
        f"{BASE_URL}/list_documents",
        json={"db_name": db_name_for_collection, "collection_name": collection_name},
    )
    st.json(response.json())

# Create a new database
st.header("Create a New Database")
db_name = st.text_input("Database Name")
if st.button("Create Database"):
    response = requests.post(f"{BASE_URL}/create_db", json={"db_name": db_name})
    st.json(response.json())

# Create a new collection
st.header("Create a New Collection")
db_name_for_collection = st.text_input("Database Name for Collection")
collection_name = st.text_input("Collection Name")
if st.button("Create Collection"):
    response = requests.post(
        f"{BASE_URL}/create_collection",
        json={"db_name": db_name_for_collection, "collection_name": collection_name},
    )
    st.json(response.json())

# Insert a new document
st.header("Insert a New Document")
db_name_for_insert = st.text_input("Database Name for Insert")
collection_name_for_insert = st.text_input("Collection Name for Insert")
document = st.text_area("Document (JSON format)", '{"name": "John Doe", "age": 30}')

document_json = json.loads(document)  # Validate and parse JSON

payload = dict(
    db_name=db_name_for_insert,
    collection_name=collection_name_for_insert,
    document=document_json,
)


if st.button("Insert Document"):
    try:
        response = requests.post(
            f"{BASE_URL}/insert_document",
            json=payload,
        )

        st.json(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except ValueError as e:
        st.error(f"Invalid JSON format: {e}")


# Delete a collection
st.header("Delete a Collection")
db_name_for_delete_collection = st.text_input("Database Name for Delete Collection")
collection_name_to_delete = st.text_input("Collection Name to Delete")
if st.button("Delete Collection"):
    response = requests.post(
        f"{BASE_URL}/delete_collection",
        json={
            "db_name": db_name_for_delete_collection,
            "collection_name": collection_name_to_delete,
        },
    )
    st.json(response.json())

# Delete a database
st.header("Delete a Database")
db_name_to_delete = st.text_input("Database Name to Delete")
if st.button("Delete Database"):
    response = requests.post(
        f"{BASE_URL}/delete_db", json={"db_name": db_name_to_delete}
    )
    st.json(response.json())
