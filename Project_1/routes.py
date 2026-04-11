from flask import Flask, request, jsonify, render_template
import json
import requests
import math
import os

app = Flask(__name__)

# Load stops.json once at startup, not on every request
with open('static/stops.json') as f:
    STOPS_DATA = json.load(f)

# Load API key from environment variable
API_KEY = os.getenv("THEBUS_API_KEY", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def get_map():
    return render_template("map.html")

@app.route("/about")
def get_about():
    return render_template("about.html")

@app.route("/contact")
def get_contact():
    return render_template("contact.html")

@app.route("/address")
def get_address():
    return render_template("address.html")

@app.route("/models")
def get_models():
    return render_template("models.html")

@app.route('/clock')
def clock():
    return render_template('clock.html')

@app.route("/stops")
def get_stops():
    return render_template("stops.html")

@app.route("/save-userAddress", methods=['POST'])
def save_address():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({'error': 'Missing lat/lng'}), 400

    return jsonify({'status': 'success', 'userAddress': {'lat': lat, 'lng': lng}}), 200

@app.route('/delete-userAddress', methods=['DELETE'])
def delete_address():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({'error': 'Missing lat/lng'}), 400

    return jsonify({'status': 'deleted', 'lat': lat, 'lng': lng}), 200

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/routes', methods=["GET"])
def routes():
    try:
        user_lat = request.args.get('lat')
        user_lon = request.args.get('lng')

        if user_lat is None or user_lon is None:
            return jsonify({'error': 'Missing lat/lng parameters'}), 400

        user_lat = float(user_lat)
        user_lon = float(user_lon)

        stops_with_distance = []
        for stop in STOPS_DATA:
            stop_lat = float(stop['lat'])
            stop_lon = float(stop['lon'])
            distance = haversine(user_lat, user_lon, stop_lat, stop_lon)

            if distance <= 750:
                stops_with_distance.append({
                    "routeName": f"Stop ID {stop.get('id', 'Unknown')}",
                    "arrivalTime": "Unknown",
                    "stopLat": stop_lat,
                    "stopLng": stop_lon,
                    "stopID": stop.get('id', 'N/A'),
                    "distance": distance
                })

        stops_with_distance.sort(key=lambda x: x['distance'])
        return jsonify(stops_with_distance[:10])

    except ValueError:
        return jsonify({'error': 'Invalid lat/lng values'}), 400
    except Exception as e:
        print("Error inside /routes:", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/arrivals', methods=['GET'])
def get_bus_coords():
    if not API_KEY:
        return jsonify({'error': 'API key not configured'}), 500

    stop_ID = request.args.get('stop', 46)
    url = f"http://api.thebus.org/arrivalsJSON/?key={API_KEY}&stop={stop_ID}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        data["arrivals"] = [
            arrival for arrival in data.get("arrivals", [])
            if float(arrival["latitude"]) != 0 and float(arrival["longitude"]) != 0
        ]

        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'TheBus API timed out'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")