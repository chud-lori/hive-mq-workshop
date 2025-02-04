import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
   print(f"Connected with result code {rc}")


value = sys.argv[1]
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set('bangke', 'Bangke123')
mqtt_client.tls_set()
mqtt_client.connect("f8416f89ec1142c9b72d7b1070b0a0e9.s1.eu.hivemq.cloud", 8883)

mqtt_client.loop_start()
mqtt_client.publish("esp32/bangke", value, 2)
mqtt_client.loop_stop()
mqtt_client.disconnect()

