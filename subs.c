#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "f8416f89ec1142c9b72d7b1070b0a0e9.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "bangke";
const char* mqtt_pass = "Bangke123";
const char* mqtt_topic = "esp32/bangke";

#define LED_PIN 2  // D2 pin

WiFiClientSecure espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
 String message = "";
 for (int i = 0; i < length; i++) {
   message += (char)payload[i];
 }
 if (message == "on") {
   digitalWrite(LED_PIN, HIGH);
 } else if (message == "off") {
   digitalWrite(LED_PIN, LOW);
 }
}

void reconnect() {
 while (!client.connected()) {
   Serial.print("Connecting MQTT...");
   if (client.connect("ESP32Client", mqtt_user, mqtt_pass)) {
     Serial.println("connected");
     client.subscribe(mqtt_topic);
   } else {
     Serial.print("failed, rc=");
     Serial.print(client.state());
     delay(5000);
   }
 }
}

void setup() {
 pinMode(LED_PIN, OUTPUT);
 Serial.begin(115200);
 WiFi.begin(ssid, password);

 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.print(".");
 }

 espClient.setInsecure();
 client.setServer(mqtt_server, mqtt_port);
 client.setCallback(callback);
}

void loop() {
 if (!client.connected()) {
   reconnect();
 }
 client.loop();
}
