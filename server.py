from flask import Flask, jsonify
from flask_cors import CORS
import serial

app = Flask(__name__)
CORS(app)

try:
    # Change COM9 if necessary
    arduino = serial.Serial('COM9', 9600, timeout=1)
except Exception as e:
    print("❌ Could not open serial port:", e)
    arduino = None

@app.route('/sensor')
def get_sensor_data():
    if not arduino:
        return jsonify({"error": "Serial port not connected"}), 500

    try:
        line = arduino.readline().decode('utf-8').strip()
        print("Received from Arduino:", line)

        if "Temperature:" in line and "Humidity:" in line:
            parts = line.split("|")
            temp_part = parts[2].split(":")[1].strip().replace("°C", "")
            humidity_part = parts[3].split(":")[1].strip().replace("%", "")
            return jsonify({
                "temperature": float(temp_part),
                "humidity": float(humidity_part)
            })
        else:
            return jsonify({"error": "Waiting for sensor data..."}), 400

    except Exception as e:
        print("❌ Error parsing serial:", e)
        return jsonify({"error": "Failed to parse data"}), 500

if __name__ == '__main__':
    app.run(debug=False)
