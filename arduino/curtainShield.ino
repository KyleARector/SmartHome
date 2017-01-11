#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <aREST.h>

// Declare second serial connection on pins 4 and 5
SoftwareSerial SerialComm(4,5);

// Create aREST instance
aREST rest = aREST();

// Set WiFi credentials
const char* ssid     = "wifi";
const char* password = "password";

// The port to listen for incoming TCP connections
#define LISTEN_PORT           80

// Create an instance of the server
WiFiServer server(LISTEN_PORT);

// Declare functions to be exposed to the API
int curtainControl(String command);

void setup(void)
{
  // Start Serial
  Serial.begin(115200);
  SerialComm.begin(9600);

  // Function to be exposed
  rest.function("curtains", curtainControl);
  // Give name and ID to device
  rest.set_id("1");
  rest.set_name("Curtains");
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  // Start the server
  server.begin();
  Serial.println("Server started");
  // Print the IP address
  Serial.println(WiFi.localIP());
  // Do not broadcast AP
  WiFi.mode(WIFI_STA);
}

void loop() {
  // Handle REST calls
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  while(!client.available()){
    delay(1);
  }
  rest.handle(client);
}

// Send the received command to the base Arduino over serial
int curtainControl(String command) {
  Serial.println(command);
  SerialComm.println(command);
  return 1;
}
