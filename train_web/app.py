from flask import Flask, render_template, jsonify, request
import time  # Import time for potential delays (optional)

app = Flask(__name__, static_url_path='/static', static_folder='static')

arrival_time = 0  # Initialize arrival_time outside of a function
trainid = 0
latitude = 0
longitude = 0
speed = 0


def create_vehicle_data(vehicle_id, gps_data):
  return {
      "name": f"Vehicle {vehicle_id + 1}",  # Add "Vehicle " and increment ID
      "latitude": gps_data[0],
      "longitude": gps_data[1],
      "speed": gps_data[2]
  }

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
        trainid = data.get('id')
        latitude = data.get('lat') 
        longitude = data.get('lng')
        speed = data.get('speed')
        arrival_time = data.get('speed')
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
