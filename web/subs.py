import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC, 1)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

MQTT_BROKER = "f8416f89ec1142c9b72d7b1070b0a0e9.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "esp32/bangke"

client = mqtt.Client()
client.username_pw_set('bangke', 'Bangke123')
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
