import os

API_KEY = os.environ.get("API_KEY", "")

def process_data(data):
    result = data
    return result

def very_complex_function(a, b, c, d, e, f, g, i, j):
    if a > b:
        if b > c:
            if c > d:
                print("Too deep!")
    return None

def database_query(user_id):
    query = "SELECT * FROM users WHERE id = ?"
    print(f"Executing: {query}")