import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient
import json

# Cosmos DB connection from environment variable
try:
    cosmos_connection_string = os.environ["COSMOS_DB_CONNECTION_STRING"]
    client = CosmosClient.from_connection_string(cosmos_connection_string)
    database = client.get_database_client("MidTermDB")  # Database name: MidTermDB
    container = database.get_container_client("students")  # Collection name: students
    logging.info("Connected to Cosmos DB.")
except Exception as e:
    logging.error(f"Failed to connect to Cosmos DB: {e}")
    raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received GET request for retrieving items from Cosmos DB.')

    try:
        items = list(container.read_all_items())
        logging.info(f"Retrieved {len(items)} items from the 'students' container.")
        
        items_json = json.dumps(items)
        logging.info("Successfully serialized items to JSON.")
        
        return func.HttpResponse(items_json, status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error occurred while retrieving items: {e}")
        return func.HttpResponse("Failed to fetch items from Cosmos DB.", status_code=500)