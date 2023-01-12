import requests

# Make a request to the IPAPI service
response = requests.get('https://ipapi.co/json/')

# Parse the JSON data from the response
data = response.json()

# Print the location information
print(f'City: {data["city"]}')
print(f'Region: {data["region"]}')
print(f'Country: {data["country_name"]}')
print(f'Latitude: {data["latitude"]}')
print(f'Longitude: {data["longitude"]}')