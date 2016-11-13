#include <ESP8266WiFi.h>
#include <aREST.h>

// Create aREST instance
aREST rest = aREST();

// WiFi parameters
const char* ssid = "wifi";
const char* password = "password";

// The port to listen for incoming TCP connections
#define LISTEN_PORT           80

// Create an instance of the server
WiFiServer server(LISTEN_PORT);

// Declare functions to be exposed to the API
int irControl(String command);

// Declare the pin for IR LED
int pin =  4;

void setup()   
{               
  // Start Serial 
  Serial.begin(115200);
  // Set the LED pin mode
  pinMode(pin, OUTPUT); 

  // Function to be exposed
  rest.function("relay", irControl);

  // Give name and ID to device
  rest.set_id("2");
  rest.set_name("tvSwitch");

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
 
void loop()                     
{
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

// Send the IR signal
int irControl(String command) {
  tvOnOff();
  return 1;
}
 
void pulseIR(long microsecs) {
  cli();
  while (microsecs > 0) {
   digitalWrite(pin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pin, LOW);
   delayMicroseconds(10); 
   microsecs -= 26;
  }
  sei();
}

void tvOnOff() {
  pulseIR(9220);
  delayMicroseconds(4660);
  pulseIR(580);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(600);
  pulseIR(540);
  delayMicroseconds(1740);
  pulseIR(580);
  delayMicroseconds(600);
  pulseIR(540);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(600);
  pulseIR(560);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(600);
  pulseIR(540);
  delayMicroseconds(1740);
  pulseIR(580);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(1760);
  pulseIR(560);
  delayMicroseconds(1760);
  pulseIR(560);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(1740);
  pulseIR(580);
  delayMicroseconds(620);
  pulseIR(520);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(640);
  pulseIR(520);
  delayMicroseconds(600);
  pulseIR(560);
  delayMicroseconds(600);
  pulseIR(560);
  delayMicroseconds(620);
  pulseIR(520);
  delayMicroseconds(1760);
  pulseIR(560);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(1760);
  pulseIR(560);
  delayMicroseconds(620);
  pulseIR(540);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(1740);
  pulseIR(580);
  delayMicroseconds(1740);
  pulseIR(560);
  delayMicroseconds(1760);
  pulseIR(560);
  delayMicroseconds(41300);
  pulseIR(9240);
  delayMicroseconds(2360);
  pulseIR(560);
  delayMicroseconds(33680);
  pulseIR(9240);
  delayMicroseconds(2340);
  pulseIR(560);
  delayMicroseconds(33660);
  pulseIR(9240);
  delayMicroseconds(2340);
  pulseIR(560);
  delayMicroseconds(33660);
  pulseIR(9220);
  delayMicroseconds(2360);
  pulseIR(560);
}

// Work in progress to dynamically send pulses from array
// Array automatically generated from remote capture sketch
/*void sendSignal(int signalArray[])
{
  for(int x = 0; x < sizeof(signalArray); x++)
  {
    if((x % 2) == 0) 
    {
      pulseIR(signalArray[x] * 10);
      Serial.println(signalArray[x] * 10);
    }
    else
    {
      delayMicroseconds(signalArray[x] * 10);
      Serial.println(signalArray[x] * 10);
    }
  }
}*/
