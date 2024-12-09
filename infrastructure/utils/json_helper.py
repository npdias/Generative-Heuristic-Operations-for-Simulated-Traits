import json
import logging
from typing import Any

def read_json(file_path: str) -> Any:
    """Read and return data from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logging.info("Successfully read JSON data from %s", file_path)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Failed to read JSON file %s: %s", file_path, e)
        return None

def write_json(file_path: str, data: Any) -> None:
    """Write data to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logging.info("Successfully wrote JSON data to %s", file_path)
    except IOError as e:
        logging.error("Failed to write JSON file %s: %s", file_path, e)