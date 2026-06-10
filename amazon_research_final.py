import requests
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERPAPI_KEY = "your api key"
GOOGLE_SHEET_ID = "your google sheet id "
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def search_products(category, min_price, max_price, min_reviews, min_rating):
    url = "https://serpapi.com/search"
    params = {
    "engine": "amazon",
    "k": category,
    "amazon_domain": "amazon.com",
    "api_key": SERPAPI_KEY
}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None

def filter_products(raw_data, min_price, max_price, min_reviews, min_rating):
    if not raw_data:
        return []
    
    results = raw_data.get("organic_results", [])
    filtered = []
    
    for product in results:
        try:
            price_str = str(product.get("price", "0")).replace("$", "").replace(",", "")
            price = float(price_str)
            rating = float(product.get("rating", 0))
            reviews = int(product.get("reviews", 0))
            
            if (min_price <= price <= max_price and 
                rating >= min_rating and 
                reviews >= min_reviews):
                filtered.append({
                    "name": product.get("title", "N/A"),
                    "asin": product.get("asin", "N/A"),
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "url": product.get("link", ""),
                    "timestamp": datetime.now().isoformat()
                })
        except (ValueError, TypeError):
            continue
    
    return filtered

def append_to_sheet(products, sheet_id):
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    
    values = [[p["name"], p["asin"], p["price"], p["rating"], p["reviews"], p["url"], p["timestamp"]] for p in products]
    
    body = {"values": values}
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range="Sheet1!A:G",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

def run_research(category, min_price, max_price, min_reviews, min_rating):
    print(f"Searching: {category} (${min_price}-${max_price}, {min_reviews}+ reviews, {min_rating}+ rating)")
    
    raw = search_products(category, min_price, max_price, min_reviews, min_rating)
    filtered = filter_products(raw, min_price, max_price, min_reviews, min_rating)
    
    if filtered:
        append_to_sheet(filtered, GOOGLE_SHEET_ID)
        print(f"Added {len(filtered)} products to sheet")
    else:
        print("No products matched criteria")
    
    return filtered

if __name__ == "__main__":
    results = run_research(
        category="Kitchen gadgets",
        min_price=15,
        max_price=50,
        min_reviews=500,
        min_rating=4.0
    )
    print(json.dumps(results, indent=2))
