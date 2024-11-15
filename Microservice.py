import requests
from bs4 import BeautifulSoup
import argparse

def get_vivino_data(wine_name, min_price=None, max_price=None):
    url = f'https://www.vivino.com/api/1/search/wines?name={wine_name}'
    
    # Send the request to the Vivino website
    response = requests.get(url)
    
    # Print status code and raw response content for debugging
    print("HTTP Status Code:", response.status_code)  # Check if the request was successful (200)
    print("Raw Response Content:", response.text[:500])  # Print the first 500 characters of the raw response for inspection
    
    if response.status_code != 200:
        print("Error: Failed to retrieve data from Vivino.")
        return None

    # Parse the JSON response
    data = response.json()
    
    # Check if we received any wines in the response
    if not data.get("wines"):
        print("Error: No results found. Please provide a more specific wine name.")
        return None
    
    # Filter results based on the price if provided
    wines = data["wines"]
    if min_price or max_price:
        wines = [wine for wine in wines if 
                 (min_price is None or wine.get("price", 0) >= min_price) and
                 (max_price is None or wine.get("price", 0) <= max_price)]

    if not wines:
        print("Error: No wines found within the specified price range.")
        return None

    return wines

def main():
    parser = argparse.ArgumentParser(description='Vivino Wine Search')
    parser.add_argument('--name', type=str, required=True, help='Name of the wine to search for')
    parser.add_argument('--minPrice', type=int, help='Minimum price filter')
    parser.add_argument('--maxPrice', type=int, help='Maximum price filter')
    
    args = parser.parse_args()
    wine_name = args.name
    min_price = args.minPrice
    max_price = args.maxPrice
    
    print(f"Received wine name: {wine_name}")
    
    wines = get_vivino_data(wine_name, min_price, max_price)
    
    if wines:
        print(f"Found {len(wines)} wines:")
        for wine in wines:
            print(wine)  # Print each wine's details for debugging

if __name__ == "__main__":
    main()
