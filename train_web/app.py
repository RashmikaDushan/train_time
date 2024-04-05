from flask import Flask, render_template, jsonify, request
import time
import geopy.distance

app = Flask(__name__, static_url_path='/static', static_folder='static')

arrival_time = 0
trainid = 0
latitude = 0
longitude = 0
speed = 0

station = (6.932832, 79.828001)

def googledistance(startingpoint,userlocation):
    if startingpoint == "Not -Yet startted":
        return {"hours":0,"minutes":0}
    origin = Locations.objects.get(name=startingpoint).geographic_location
    destination = userlocation
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&alternatives=false&avoid=tolls&key={key}"
    response = requests.request("GET", url, headers=headers, data=payload)
    jsoned_data = json.loads(response.text)
    duration =  jsoned_data["routes"][0]["legs"][0]["duration"]["text"]
    list_duration = duration.split(" ")
    if len(list_duration) == 2:
        hours = 0
        minutes = list_duration[0]
    elif len(list_duration) == 4:
        hours = list_duration[0]
        minutes = list_duration[2]
    return {"hours":hours,"minutes":minutes}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data is not None:
        global trainid
        global latitude
        global longitude
        global speed
        global arrival_time
        global station
        trainid = data.get('id')
        latitude = data.get('lat') 
        longitude = data.get('lng')
        speed = data.get('speed')
        train_location = (latitude, longitude)
        distance = geopy.distance.geodesic(train_location, station).km
        print(f"Distance: {distance}")
        arrival_time = distance / speed
        print(f"Received value: {trainid} , {latitude} , {longitude} , {speed} ")
        return jsonify({'message': 'Data received successfully'}), 200
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400

@app.route('/get_data')
def get_data():
    global arrival_time
    time.sleep(1)
    print(f"Sent value: {trainid} , {latitude} , {longitude} , {speed} , {arrival_time} ")
    return jsonify({'trainId': trainid , 'latitude': latitude , 'longitude':longitude , 'speed':speed , 'arrival_time':arrival_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
