import requests

# Define TMDB API endpoint and parameters
url = 'https://api.themoviedb.org/3/search/movie'
params = {
    'api_key': '79313ab3de3abf8b796b2e7e8a890c6b',  # Replace with your actual TMDB API key
    'query': 'Avengers',        # Example movie search query
}

# Make a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response content (JSON data)
    print(response.json())
else:
    print('Error:', response.status_code)
