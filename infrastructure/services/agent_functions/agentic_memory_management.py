import json
import time
import os
from config import DATA_DIR

remember_file = os.path.join(DATA_DIR, 'remember.json')

async def function_router(name:str, arguments:dict):
    # which function to use
    #TODO: need to add a script to summarize and group memories in the short term memories and store them as long term memories
    output = None
    if 'add' in name.lower():
        output = add_thought_to_json(arguments)
    elif 'read' in name.lower():
        output = f'remember_list: {_read_remember_list()}'
    return output

def _read_remember_list():
    data = []
    try:
        with open(remember_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        print("Error reading JSON file. The file may be corrupted.")
    return data

def add_thought_to_json(arguments):
    # if given json arg append dict to json file
    data = _read_remember_list()
    arg_dict = arguments
    arg_dict.update(dateString = time.strftime('%a, %d %b %Y %I:%M:%S %p CST', time.localtime()), entryDate=time.time())
    data.append(arguments)
    with open(remember_file, 'w') as file:
        json.dump(data, file, indent=4)
    return f'success: memory recorded, data: {data}'


# test = json.loads("{\n  \"status\": \"success\",\n  \"message\": \"Tool has been called successfully.\",\n  \"tool_name\": \"call_tool\",\n  \"user_command\": \"call tool\"\n}")
# function_router(name="remember", arguments= test)