import machine
import time
import network
import ujson
from umqtt.simple import MQTTClient
from mfrc522 import MFRC522

# ==============================
# CONFIGURATION
# ==============================

WIFI_SSID = "EdNet"
WIFI_PASSWORD = "Huawei@123"
MQTT_SERVER = "157.173.101.159"

TEAM_ID = "livora27"

TOPIC_STATUS = f"rfid/{TEAM_ID}/card/status"
TOPIC_TOPUP = f"rfid/{TEAM_ID}/card/topup"
TOPIC_BALANCE = f"rfid/{TEAM_ID}/card/balance"

# ==============================
# GLOBAL STATE
# ==============================

card_balances = {}  

# ==============================
# WIFI CONNECTION
# ==============================

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_wifi():
    if not wlan.isconnected():
        print("[DEBUG] Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
        print("[DEBUG] WiFi Connected.")

connect_wifi()

# ==============================
# RFID SETUP
# ==============================

reader = MFRC522(sck=14, mosi=13, miso=12, rst=4, cs=5)

# ==============================
# MQTT SETUP
# ==============================

client = MQTTClient(TEAM_ID, MQTT_SERVER, port=1883)

def on_message(topic, msg):
    global card_balances

    print("\n[DEBUG] Top-up command received")

    try:
        data = ujson.loads(msg)
        uid = data.get("uid")
        topup_amount = data.get("amount")

        if not uid or not isinstance(topup_amount, int):
            print("[DEBUG] Invalid top-up payload")
            return

        if uid not in card_balances:
            card_balances[uid] = 0

        card_balances[uid] += topup_amount

        print(f"[DEBUG] New Balance for {uid}: {card_balances[uid]}")

        response = {
            "uid": uid,
            "new_balance": card_balances[uid]
        }

        client.publish(TOPIC_BALANCE, ujson.dumps(response))
        print("[DEBUG] Confirmation published.")

    except Exception as e:
        print(f"[DEBUG] Error processing message: {e}")

def connect_mqtt():
    while True:
        try:
            print("[DEBUG] Connecting to MQTT...")
            client.connect()
            client.set_callback(on_message)
            client.subscribe(TOPIC_TOPUP)
            print(f"[DEBUG] Subscribed to {TOPIC_TOPUP}")
            break
        except Exception as e:
            print("[DEBUG] MQTT connection failed, retrying...")
            time.sleep(2)

connect_mqtt()

# ==============================
# MAIN LOOP
# ==============================

last_uid = None

while True:
    try:
        if not wlan.isconnected():
            connect_wifi()

        client.check_msg()

        (stat, tag_type) = reader.request(reader.REQIDL)

        if stat == reader.OK:
            (stat, raw_uid) = reader.anticoll()

            if stat == reader.OK:
                uid_str = "%02X%02X%02X%02X" % (
                    raw_uid[0],
                    raw_uid[1],
                    raw_uid[2],
                    raw_uid[3]
                )

                if uid_str != last_uid:
                    print(f"\n[DEBUG] Card Tapped: {uid_str}")

                    if uid_str not in card_balances:
                        card_balances[uid_str] = 0

                    payload = {
                        "uid": uid_str,
                        "balance": card_balances[uid_str]
                    }

                    client.publish(TOPIC_STATUS, ujson.dumps(payload))
                    print("[DEBUG] Status published.")

                    last_uid = uid_str
        else:
            last_uid = None

        time.sleep(0.2)

    except Exception as e:
        print(f"[DEBUG] Main loop error: {e}")

        try:
            connect_mqtt()
        except:
            pass

        time.sleep(2)
