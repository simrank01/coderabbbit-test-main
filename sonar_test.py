import os  # Issue: Unused import

# Issue: Hardcoded secret (Security Vulnerability)
API_KEY = "12345-ABCDE-67890-SECRET-KEY"

def process_data(data):
    # Issue: Using 'eval' is a huge security risk
    result = eval(data) 
    
    # Issue: Unreachable code
    return result
    print("This will never run!") 

def very_complex_function(a, b, c, d, e, f, g, h, i, j):
    # Issue: Too many arguments (Cognitive Complexity)
    if a > b:
        if b > c:
            if c > d:
                # Issue: Deeply nested 'if' statements
                print("Too deep!")
    return None

def database_query(user_id):
    # Issue: SQL Injection risk (Security Vulnerability)
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    print(f"Executing: {query}")

# Issue: Defining a variable but never using it
unused_variable = 42