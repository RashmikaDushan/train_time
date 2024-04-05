#include <WiFi.h>
#include <HTTPClient.h>
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>
#include <ArduinoJson.h> 

#define RXD2 16
#define TXD2 17
#define GPS_BAUD 9600

TinyGPSPlus gps;

struct GPSData {
  double latitude;
  double longitude;
  float speed;
  bool isValid;
};

const char* ssid = "Galaxy";  // Your wifi SSID
const char* password = "HelloWorld";  // Your wifi password
const char* serverIp = "192.168.222.36"; // Replace with your laptop's IP address
const int port = 5001; // Port number of your Flask backend

const char* trainiId = "1234";  // Train ID

String jsonData;

boolean newData;

HardwareSerial neogps(1);


void setup() {
  Serial.begin(115200);
  neogps.begin(9600, SERIAL_8N1, RXD2, TXD2);
  delay(1000);
  setup_wifi();
}

void loop() {
  jsonData = getGPSDataJSON();
  http_send(jsonData);
  delay(2000);
}

void setup_wifi() {
  delay(10);
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to WiFi with IP: ");
  Serial.println(WiFi.localIP());
}

void http_send(String jsonData){
  WiFiClient client;
  HTTPClient http;
 
  Serial.print("Sending data: ");
  Serial.println(jsonData);

  http.begin(client, "http://" + String(serverIp) + ":" + String(port) + "/data");
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonData);

  if (httpResponseCode > 0) {
    Serial.print("POST response: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.print("Error sending data: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

String getGPSDataJSON() {

  DynamicJsonDocument doc(64);

  doc["id"] = trainiId;

  newData = false;
  
  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (neogps.available())
    {
      if (gps.encode(neogps.read()))
      {
        newData = true;
      }
    }
  }
  if(newData == true)
  {
    newData = false;
    Serial.print(gps.location.lat());
    Serial.print(" , ");
    Serial.print(gps.location.lng());
    Serial.print(" , ");
    Serial.println(gps.speed.kmph());
    doc["lat"] = gps.location.lat();
    doc["lng"] = gps.location.lng();
    doc["speed"] = gps.speed.kmph();
  }
  else
  {
    Serial.println("Invalid");
    doc["error"] = "No valid GPS data available";
  }

  String jsonString;
  serializeJson(doc, jsonString);
  return jsonString;
}

