#!/usr/bin/python3

import signal
import sys
import paho.mqtt.client as mqtt
import json

def signal_handler(signum, frame):
    mqttc.disconnect()
    mqttc.loop_stop()
    sys.exit()

def on_connect(client, obj, flags, reason_code, properties):
    print("mqtt-connect, reason_code: " + str(reason_code))

def on_message(client, obj, msg):
    data = json.loads(msg.payload)
    print("mqtt-on-data: " + str(data))

def on_subscribe(client, obj, mid, reason_code_list, properties):
    print("mqtt-subscribe: " + str(mid) + " " + str(reason_code_list))

signal.signal(signal.SIGINT, signal_handler)

# add your brick4u MQTT credentials here
broker = "YOUR_BROKER_INSTANCE.broker.brick4u.de"
port = 12010
username = "YOUR_MQTT_USERNAME"
password = "YOUR_MQTT_PASSWORD"

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311, transport="tcp")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.tls_set()
mqttc.tls_insecure_set(True)
mqttc.username_pw_set(username, password)
mqttc.connect(broker, port, 60)

# add iometer serial numbers here
# e.g. mqttc.subscribe("/00000006/json")
mqttc.subscribe("/YOUR_IOMETER_SERIAL_NUMBER/json")
mqttc.loop_forever()
