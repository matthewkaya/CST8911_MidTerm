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
    logging.info('Received DELETE request to remove an item from Cosmos DB.')

    item_id = req.route_params.get('item_id')
    logging.info(f"Received item_id for deletion: {item_id}")

    if not item_id:
        logging.warning("No 'item_id' provided in the request.")
        return func.HttpResponse("Item ID is required for deletion.", status_code=400)
    
    try:
        container.delete_item(item=item_id, partition_key=item_id)
        logging.info(f"Item with ID '{item_id}' successfully deleted from Cosmos DB.")
        return func.HttpResponse("Item deleted successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Error occurred while deleting item with ID '{item_id}': {e}")
        return func.HttpResponse(f"Failed to delete item with ID '{item_id}'.", status_code=500)