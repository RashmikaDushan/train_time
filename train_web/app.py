from flask import Flask, render_template, jsonify
import serial
import time

arrival_time = 0

app = Flask(__name__)

def read_serial_data(serial_port):
    data_buffer = b''
    while not data_buffer.endswith(b'\n'):
        data_buffer += serial_port.read()
    return data_buffer.decode().strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    try:
        arduino = serial.Serial('/dev/cu.usbmodem11101', 9600)  # Update the port as needed
        time.sleep(1)  # Add a delay to match the Arduino's data transmission rate
        data = read_serial_data(arduino)
        arduino.close()
        elements = data.split(',') # Split the data into two elements using the ',' separator
        print(elements)
        if len(elements) == 2:
            distance = float(elements[0])
            speed = float(elements[1])
            arrival_time = distance/speed
            arrival_time = "{:.2f}".format(arrival_time)  # Format to 2 decimal places
            return jsonify({'value': arrival_time})
        else:
            return jsonify({'error': 'Invalid data format from Arduino'})
    except serial.SerialException as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
