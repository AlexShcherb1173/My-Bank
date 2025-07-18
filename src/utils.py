import json
import os

def read_json_file(filepath):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                return []
    except (json.JSONDecodeError, IOError):
        return []



if __name__ == '__main__':
    unittest.main()