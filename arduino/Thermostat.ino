#include <ESP8266WiFi.h>

#define sleepDelay 300  
#define upPin 14
#define downPin 12

const char* ssid = "wifi";
const char* password = "password";
const int httpPort = 80;

IPAddress server(0,0,0,0);

WiFiClient client;

void setup() {
  Serial.begin(115200);
  
  digitalWrite(upPin, HIGH);
  digitalWrite(downPin, HIGH);
  pinMode(upPin, OUTPUT);
  pinMode(downPin, OUTPUT);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void controlRelay(int pin, int quantity) {
  for(int x=0; x <= quantity; x++) {
    digitalWrite(pin, LOW);
    delay(700);
    digitalWrite(pin, HIGH);
    delay(700);
  }
}

void loop() {
  if (!client.connect(server, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  String url = "/thermostat";

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + server + "\r\n" + 
               "Connection: close\r\n\r\n");
  delay(500);

  String keepLine = "";
  while(client.available()){
    String line = client.readStringUntil('\r');
    if (line.charAt(1) == '{') {
      int startPos = line.indexOf(':') + 2;
      int endPos = line.indexOf('}');
      keepLine = line.substring(startPos, endPos);
    }
  }

  int tempChange = keepLine.toInt();
  
  if (tempChange > 0) {
    controlRelay(upPin, tempChange);
  }
  else if (tempChange < 0) {
    controlRelay(downPin, tempChange * -1);
  }
  
  delay(100);

  ESP.deepSleep(sleepDelay * 1000000, WAKE_RF_DEFAULT);
  delay(500);   // wait for deep sleep to happen
}

