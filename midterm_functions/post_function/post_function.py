import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient

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
    logging.info('Received POST request to add a new item to Cosmos DB.')

    try:
        item_data = req.get_json()
        logging.info(f"Received item data: {item_data}")

        if "id" not in item_data or not item_data["id"]:
            logging.warning("Received item data does not contain a valid 'id' field.")
            return func.HttpResponse("Item must contain an 'id' field.", status_code=400)
        
        container.create_item(body=item_data)
        logging.info("Item successfully added to Cosmos DB.")

        return func.HttpResponse("Item added successfully.", status_code=201)
    except ValueError:
        logging.error("Invalid JSON format received in the request.")
        return func.HttpResponse("Invalid JSON format.", status_code=400)
    except Exception as e:
        logging.error(f"Error occurred while adding item to Cosmos DB: {e}")
        return func.HttpResponse("Failed to add item to Cosmos DB.", status_code=500)