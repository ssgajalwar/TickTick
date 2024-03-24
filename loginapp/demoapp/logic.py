import requests

def get_location(latitude, longitude):
    # Replace YOUR_API_KEY with your actual Google Maps API key
    api_key = "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"
    print(url)
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
            # Extracting address components
            location_info = data['results'][0]['formatted_address']
            return location_info
        else:
            return "Unable to retrieve location information"
    except Exception as e:
        print("Error:", e)
        return "Error occurred while fetching location information"