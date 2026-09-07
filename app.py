import os
import time
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_ACTUAL_OPENWEATHER_API_KEY")

CACHE = {}
CACHE_DURATION = 300

def get_cached_data(cache_key):
    """5 dəqiqə ərzində saxlanılan keşi yoxlayır və qaytarır."""
    if cache_key in CACHE:
        cached_item = CACHE[cache_key]
        if time.time() - cached_item["timestamp"] < CACHE_DURATION:
            return cached_item["data"]
    return None

def set_cached_data(cache_key, data):
    """Məlumatı keşə yazır."""
    CACHE[cache_key] = {
        "timestamp": time.time(),
        "data": data
    }

def fetch_weather_by_coords(lat, lon, dt=None):
    """Enlik və uzunluq koordinatlarına görə hava məlumatını çəkir."""
    cache_key = f"{lat}_{lon}_{dt}" if dt else f"{lat}_{lon}_current"
    cached_res = get_cached_data(cache_key)
    if cached_res:
        return cached_res

    if dt:
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&units=metric&appid={API_KEY}"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            set_cached_data(cache_key, data)
            return data
    except requests.RequestException as e:
        print(f"API Sorğu Xətası: {e}")
    
    return None

def fetch_weather_by_city(city_name):
    """Şəhər adına görə geocoding və hava məlumatı çəkir."""
    cache_key = f"city_{city_name.lower().strip()}"
    cached_res = get_cached_data(cache_key)
    if cached_res:
        return cached_res

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    
    try:
        geo_res = requests.get(geo_url, timeout=10)
        if geo_res.status_code == 200 and len(geo_res.json()) > 0:
            location_data = geo_res.json()[0]
            lat = location_data["lat"]
            lon = location_data["lon"]
            name = f"{location_data.get('name')}, {location_data.get('country')}"
            
            weather_data = fetch_weather_by_coords(lat, lon)
            if weather_data:
                result = {"location_name": name, "weather": weather_data, "lat": lat, "lon": lon}
                set_cached_data(cache_key, result)
                return result
    except requests.RequestException as e:
        print(f"Geocoding Xətası: {e}")
        
    return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/weather", methods=["GET"])
def api_weather():
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    dt = request.args.get("dt")

    if city:
        data = fetch_weather_by_city(city)
        if data:
            return jsonify({"status": "success", "data": data})
        return jsonify({"status": "error", "message": "Şəhər tapılmadı"}), 404
    elif lat and lon:
        weather_data = fetch_weather_by_coords(lat, lon, dt)
        if weather_data:
            return jsonify({
                "status": "success", 
                "data": {
                    "location_name": f"{lat}, {lon}",
                    "weather": weather_data,
                    "lat": lat,
                    "lon": lon
                }
            })
        return jsonify({"status": "error", "message": "Hava məlumatı alına bilmədi"}), 400
    
    return jsonify({"status": "error", "message": "Parametrlər çatmır"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)