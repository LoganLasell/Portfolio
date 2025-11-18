from flask import Flask, request, jsonify, render_template
import json
import requests # type: ignore
import math

app = Flask(__name__)

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

@app.route("/save-userAddress", methods=['POST'])
def save_address():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({'error': 'Missing lat/lng'}), 400

    print(f"User address received: lat={lat}, lng={lng}")
    # Save to database or in-memory list as object { lat: x, lng: y }

    return jsonify({'status': 'success', 'userAddress': {'lat': lat, 'lng': lng}}), 200


@app.route('/delete-userAddress', methods=['DELETE'])
def delete_address():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({'error': 'Missing lat/lng'}), 400

    # perform deletion logic here...

    return jsonify({'status': 'deleted', 'lat': lat, 'lng': lng}), 200


    





# Haversine formula to calculate distance between two lat/lng points
def haversine(lat1, lon1, lat2, lon2):
    import math
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

@app.route('/routes', methods = ["GET"])
def routes():
    try:

        # Load stops.json
        with open('static/stops.json') as f:
            stops_data = json.load(f)


        user_lat = float(request.args.get('lat'))
        user_lon = float(request.args.get('lng'))


        stops_with_distance = []
        for stop in stops_data:
            stop_lat = float(stop['lat'])
            stop_lon = float(stop['lon'])
            distance = haversine(user_lat, user_lon, stop_lat, stop_lon)

            # Only add if within 750 meters (0.75 km)
            if distance <= 750:
                stops_with_distance.append({
                    "routeName": f"Stop ID {stop.get('id', 'Unknown')}",
                    "arrivalTime": "Unknown",
                    "stopLat": stop_lat,
                    "stopLng": stop_lon,
                    "stopID": stop.get('id', 'N/A'),
                    "distance": distance
                })

        # Sort by distance
        stops_with_distance.sort(key=lambda x: x['distance'])

        # Get the 10 closest
        closest_stops = stops_with_distance[:10]

        return jsonify(closest_stops)

    except Exception as e:
        print("Error inside /routes:", str(e))
        return jsonify({'error': str(e)}), 500



@app.route("/models")
def get_models():
    return render_template("models.html")

@app.route('/clock')
def clock():
    return render_template('clock.html')
@app.route("/stops")
def get_stops():
    return render_template("stops.html")

@app.route('/arrivals', methods=['GET'])
def get_bus_coords():
    API_KEY = "F02CFCAC-3067-45DB-835E-A102C773D6F2"
    stop_ID = request.args.get('stop', 46)  

    url = f"http://api.thebus.org/arrivalsJSON/?key={API_KEY}&stop={stop_ID}"
    
    """
format:

data = {
        "arrivals" : [
            { ...,
              ...,
              ... 
            },

            { ...,
              ...,
              ...
            }
        ],
        "stop_ID" = __,
        "timestamp" = ____
    }
    """
    try:
        response = requests.get(url)

        data = response.json()

        data["arrivals"] = [arrival for arrival in data["arrivals"] 
                    if float(arrival["latitude"]) != 0 and float(arrival["longitude"]) != 0]
                
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    

    

# @app.route('/arrivals', methods=['GET'])
# def get_user_coords():
#     API_KEY = "F02CFCAC-3067-45DB-835E-A102C773D6F2"
#     stop_ID = request.args.get('stop', )  

#     url = f"http://api.thebus.org/arrivalsJSON/?key={API_KEY}&stop={stop_ID}"
    
#     try:
#         response = requests.get(url)

#         data = response.json()

#         data["arrivals"] = [arrival for arrival in data["arrivals"] 
#                     if float(arrival["latitude"]) != 0 and float(arrival["longitude"]) != 0]
        
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)