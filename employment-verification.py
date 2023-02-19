import requests
import sqlite3
from datetime import datetime, timedelta
from cachetools import TTLCache

# Create a cache that will expire after 1 hour
cache = TTLCache(maxsize=1000, ttl=3600)

# Connect to a SQLite database to store the employment verification results
conn = sqlite3.connect('employment_verification.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS employment_verification
             (name text, company text, is_employed integer, timestamp text)''')
conn.commit()

def employment_verification(name: str, company: str) -> str:
    # Check if the employment verification results are in the cache
    key = f'{name}:{company}'
    cached_result = cache.get(key)
    if cached_result:
        return cached_result

    # Check if the employment verification results are in the database
    c.execute("SELECT is_employed, timestamp FROM employment_verification WHERE name=? AND company=?", (name, company))
    db_result = c.fetchone()
    if db_result:
        is_employed, timestamp_str = db_result
        timestamp = datetime.fromisoformat(timestamp_str)
        age = datetime.now() - timestamp
        # If the result is less than 1 hour old, return it
        if age < timedelta(hours=1):
            result = f"{name} is {'currently employed' if is_employed else 'not currently employed'} at {company}."
            # Cache the result for future requests
            cache[key] = result
            return result

    # Perform the employment verification check
    url = 'https://api.example.com/employment_verification'
    payload = {'name': name, 'company': company}
    headers = {'content-type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an error if status code is 4xx or 5xx
        response_data = response.json()
        is_employed = response_data['is_employed']
        result = f"{name} is {'currently employed' if is_employed else 'not currently employed'} at {company}."
        # Cache the result for future requests
        cache[key] = result
        # Store the result in the database
        timestamp = datetime.now().isoformat()
        c.execute("INSERT INTO employment_verification VALUES (?, ?, ?, ?)", (name, company, is_employed, timestamp))
        conn.commit()
        return result
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Example
