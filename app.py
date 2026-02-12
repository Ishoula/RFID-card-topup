from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Configuration ---
TEAM_ID = "livora27" # [cite: 57]
MQTT_BROKER = "157.173.101.159" # [cite: 12]
TOPIC_STATUS = f"rfid/{TEAM_ID}/card/status" # [cite: 61]
TOPIC_TOPUP = f"rfid/{TEAM_ID}/card/topup" # [cite: 68]
TOPIC_BALANCE = f"rfid/{TEAM_ID}/card/balance" # [cite: 76]

# --- MQTT Setup ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {rc}")
    client.subscribe(TOPIC_STATUS) # [cite: 48]
    client.subscribe(TOPIC_BALANCE)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(f"Received MQTT: {payload}")
    # Push update to Dashboard via WebSocket [cite: 49, 97]
    socketio.emit('update_dashboard', payload)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60) # [cite: 17]
mqtt_client.loop_start()

# --- Routes ---
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/topup', methods=['POST']) # [cite: 93]
def handle_topup():
    data = request.json
    # Send command to ESP8266 via MQTT [cite: 48, 67]
    mqtt_client.publish(TOPIC_TOPUP, json.dumps(data))
    return jsonify({"status": "Command sent to device"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2727)