#include <math.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>
#include <aREST.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define LISTEN_PORT           80

// Define LCD Screen
LiquidCrystal_I2C lcd(0x27, 16, 2);

OneWire oneWire(12);
DallasTemperature sensors(&oneWire);

DeviceAddress insideTemp = { hexAddress1 };
DeviceAddress outsideTemp = { hexAddress2 };

// Define REST server
aREST rest = aREST();

// WiFi parameters
const char* ssid = "wifi";
const char* password = "password";

// Instantiate server
WiFiServer server(LISTEN_PORT);

// Set up REST variables
int inTempInt = 0;
int outTempInt = 0;

// Set display refresh delay
int tempDelay = 5000;

void setup()
{
  Serial.begin(9600);
  Serial.print("Starting LCD");
  // Initialize LCD  
  lcd.init();
  lcd.backlight();
  
  // Rest set up
  rest.set_id("2");
  rest.set_name("tempSensor");
  rest.variable("inTempInt",&inTempInt);
  rest.variable("outTempInt",&outTempInt);
  
  WiFi.begin(ssid, password);
  lcd.setCursor(0, 0);
  lcd.print(" Connecting...  ");
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }
  // Start server
  server.begin();
  
  // Start sensors
  sensors.begin();
  sensors.setResolution(insideTemp, 10);
  sensors.setResolution(outsideTemp, 10);
  lcd.clear();
  lcd.setCursor(0, 0);
}

void loop()
{
  if (tempDelay == 5000)
  {
    displayTemp();
    tempDelay = 0;
  }
  Serial.print(tempDelay);
  Serial.print("\n");
  tempDelay++;
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  while(!client.available()){
    delay(1);
  }
  rest.handle(client);
}

void displayTemp()
{
  // Request temperatures from sensors
  sensors.requestTemperatures();
  float inTemp = DallasTemperature::toFahrenheit(sensors.getTempC(insideTemp));
  float outTemp = DallasTemperature::toFahrenheit(sensors.getTempC(outsideTemp));
  
  // Display temperatures to LCD screen
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(" Out: " + String(outTemp) + " Deg ");
  lcd.setCursor(0, 1);
  lcd.print("  In: " + String(inTemp) + " Deg  ");
  
  // Round to int for aREST variable
  inTempInt = round(inTemp);
  outTempInt = round(outTemp);
}
