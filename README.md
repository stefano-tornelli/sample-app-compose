# Docker Compose Example: MongoDB, Flask API, and Streamlit Frontend

This repository contains an example of using Docker Compose to spin up a three-service application. The services include a MongoDB server, a Flask backend API for MongoDB operations, and a Streamlit frontend to interact with the API.

## Services

1. **MongoDB Server**: An official MongoDB Docker image.
2. **Flask API**: A backend API built with Flask that provides endpoints for basic MongoDB operations using PyMongo. The API documentation is available through Swagger.
3. **Streamlit Frontend**: A frontend interface built with Streamlit that allows users to test the backend endpoints through buttons and text input fields.

## Getting Started

### Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/docker-compose-example.git
    cd docker-compose-example
    ```

2. Build and start the services using Docker Compose:

    ```bash
    docker-compose up --build
    ```

### Accessing the Services

- **MongoDB Server**: Accessible at `mongodb://mongo:27017` from within the Docker network.
- **Flask API**: Accessible at `http://localhost:5000`. Swagger documentation is available at `http://localhost:5000/apidocs`.
- **Streamlit Frontend**: Accessible at `http://localhost:8080`.

## Usage

### Flask API Endpoints

- **List Databases**: `GET /list_dbs`
- **List Collections**: `GET /list_collections`
- **List Documents**: `GET /list_documents`
- **Create Collection**: `POST /create_collection`
- **Insert Document**: `POST /insert_document`
- **Delete Collection**: `DELETE /delete_collection`
- **Delete Database**: `DELETE /delete_db`

Refer to the Swagger documentation at `http://localhost:5000/apidocs` for detailed information on request parameters and responses.

### Streamlit Frontend

The Streamlit frontend provides a simple interface to test the backend API endpoints. Use the buttons and text input fields to interact with the API and view the responses on the screen.

## Docker Compose Configuration

The `docker-compose.yml` file defines the three services:

```yaml
version: '3'

services:
  flask-backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - mongodb-database
    environment:
      - MONGO_URI=mongodb://mongodb-database:27017

  streamlit-frontend:
    build: ./frontend
    ports:
      - "8080:8080"
    depends_on:
      - flask-backend
      - mongodb-database

  mongodb-database:
    image: mongo
    ports:
      - "27017:27017"