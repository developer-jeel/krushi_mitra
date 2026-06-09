import requests

def crop_price(city):
    api_key = "579b464db66ec23bdd0000012bddf55026c442586adb6f1fa0b82807"
    resource_id = "9ef84268-d588-465a-a308-a864a43d0070"
    
    # Build URL correctly using an f-string
    url = f"https://api.data.gov.in/resource/{resource_id}?api-key={api_key}&format=json&filters[state]=Gujarat&filters[district]={city}&limit=1000"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    crops = ["Cotton", "Wheat", "Rice"]
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()          # Raise error for 4xx/5xx status codes
        
        # Debug: print status and raw response for inspection
        print(f"Status: {response.status_code}")
        
        # Only parse JSON if response is not empty
        if not response.text.strip():
            print("Empty response from API")
            return []
        
        data = response.json()
        records = data.get("records", [])
        
        prices = []
        for crop in crops:
            crop_data = None
            for item in records:
                commodity = item.get("commodity")
                if not commodity:
                    continue
                comm_lower = commodity.lower()
                crop_lower = crop.lower()
                
                # Direct match
                if crop_lower == comm_lower:
                    crop_data = item
                    break
                # Special alias matching (Rice is listed as Paddy(Common) in many Mandis)
                elif crop_lower == "rice" and "paddy" in comm_lower:
                    crop_data = item
                    break
                # Substring/reverse substring match
                elif crop_lower in comm_lower or comm_lower in crop_lower:
                    crop_data = item
                    break
            
            if crop_data:
                prices.append({
                    "crop": crop,
                    "price": crop_data.get("modal_price"),
                })
        return prices
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except ValueError as e:
        print(f"JSON decode error: {e}")
        print("Raw response (first 500 chars):", response.text[:500])
        return []

# Test
print(crop_price("Ahmedabad"))