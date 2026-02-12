🚀 Livora 27 – Real-Time RFID IoT Credit System

A production-ready RFID card top-up and monitoring system built with:

* Flask
* Flask-SocketIO
* MQTT (Mosquitto)
* ESP8266 (MicroPython)
* MFRC522 RFID Reader
* TailwindCSS Dashboard

---

📌 Project Overview

Livora 27 is a real-time IoT system that allows:

* RFID card scanning via ESP8266
* Live UID + balance streaming to a web dashboard
* Real-time top-up transactions from the browser
* Instant balance confirmation via MQTT

---

🏗 System Architecture

RFID Card  
↓  
ESP8266 + MFRC522  
↓ (MQTT Publish)  
MQTT Broker (VPS)  
↓  
Flask Backend (MQTT Subscriber)  
↓ (WebSocket Emit)  
Web Dashboard

---

📡 MQTT Topics

TEAM\_ID = livora27

* rfid/livora27/card/status → ESP → Server
* rfid/livora27/card/topup → Server → ESP
* rfid/livora27/card/balance → ESP → Server

---

📁 Project Structure

livora27/ ├── app.py ├── requirements.txt ├── templates/ │ └──
dashboard.html └── README.md

---

🛠 Local Development Setup

1\. Clone Repository

git clone https://github.com/Ishoula/RFID-card-topup
cd livora27

2\. Create Virtual Environment

python3 -m venv venv  
source venv/bin/activate  
# Windows: venv

3\. Install Dependencies

pip install -r requirements.txt

4\. Run Application

python app.py
Open in browser:
http://157.173.101.159:9233

---

🌍 VPS Deployment

Install Dependencies

pip install -r requirements.txt

Run with nohup
nohup python3 app.py > rfid.log 2>\&1 \&
Access URL: http://157.173.101.159:9233

---

👨‍💻 Author
Livora 27 Team