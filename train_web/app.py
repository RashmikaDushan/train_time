from flask import Flask, render_template, jsonify, request
import serial

app = Flask(__name__)

distance_speed = [0,0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    try:
        arduino = serial.Serial('/dev/cu.usbmodem11301', 9600)  # Update the port as needed
        data = arduino.readline().decode().strip()
        arduino.close()
    except serial.SerialException:
        data = -1 # Enable to get data from arduino
    return jsonify({'value': data})

@app.route('/send_data', methods=['POST'])
def send_data():
    distance_speed[0] = request.json['distance']
    distance_speed[1] = request.json['speed']
    print('Distance to the station: ', distance_speed[0] , " | Velocity of the train: ", distance_speed[1])  # Print the received data on the Python console
    # try:
    #     arduino = serial.Serial('/dev/cu.usbmodem11301', 9600)  # Update the port as needed
    #     distance_speed[0],distance_speed[1] = float(distance_speed[0]),float(distance_speed[1])
    #     arduino.write(distance_speed.encode())
    #     arduino.close()
    #     print('Data sent successfully')
    #     return 'Data sent successfully'
    # except serial.SerialException:
    #     print(serial.SerialException.__name__) 
    #     return str(serial.SerialException.__name__)

if __name__ == '__main__':
    app.run(debug=True)
