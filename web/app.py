from flask import Flask, request, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

# EMQX MQTT broker details
MQTT_BROKER = "f8416f89ec1142c9b72d7b1070b0a0e9.s1.eu.hivemq.cloud"  # EMQX Cloud or public broker address
MQTT_PORT = 8883
MQTT_TOPIC = "esp32/bangke"

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set('bangke', 'Bangke123')
mqtt_client.tls_set()
mqtt_client.connect(MQTT_BROKER, 8883)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    action = request.form.get('action')
    if action not in ['on', 'off']:
        return "Invalid action", 400

    # Publish the action to the MQTT topic
    res = mqtt_client.publish(MQTT_TOPIC, action, 1)
    print(f"PUBL: {res.is_published()}")
    if not res.is_published():
        print(res)
        print("MESSAGE not published")
    return f"Sent '{action}' command to ESP32"

if __name__ == '__main__':
    mqtt_client.loop_start()
    app.run(debug=True, host='0.0.0.0')

