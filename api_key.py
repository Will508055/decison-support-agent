def get_api_key() -> str:
    key_path = 'api_key.txt'
    with open(key_path, 'r') as file:
        api_key = file.read()
    return api_key