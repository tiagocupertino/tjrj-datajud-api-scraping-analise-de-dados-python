import requests
import base64

# Define the API endpoint and your API key
API_ENDPOINT = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
API_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

# Decode the API key
decoded_api_key = base64.b64decode(API_KEY).decode("utf-8")

# Prepare headers with your decoded API key
headers = {
    "Authorization": f"Bearer {decoded_api_key}",
    "Content-Type": "application/json"  # Adjust content type based on API requirements
}

# Make a GET request to the API endpoint
response = requests.get(API_ENDPOINT, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Process the response data
    data = response.json()
    print("Response data:", data)
else:
    print("Error:", response.text)
