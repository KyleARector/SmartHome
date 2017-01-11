// Uses SoftwareSerial with my revisions on GitHub
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Initialize motor shield
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Use M4 on motor shield
Adafruit_DCMotor *curtainMotor = AFMS.getMotor(4);

// Declare software serial connection on pins 2 and 3
SoftwareSerial SerialComm(3,2);

// Declare runMotor function
void runMotor(char dir);

void setup() {
  // Start serial connection
  Serial.begin(9600);
  SerialComm.begin(9600);
  // Start the motor shield
  AFMS.begin();
  // Set motor default speed to highest possible
  curtainMotor->setSpeed(255);
}

void loop() {
  // If serial is available from Node
  if (SerialComm.available() > 0){
    // Read the character
    char dir = SerialComm.read();
    // Run the motor
    runMotor(dir);
  }
}

void runMotor(char dir) {
  if (dir == 'O') {
    curtainMotor->run(FORWARD);
    delay(3000);
  }
  else if (dir == 'C'){
    curtainMotor->run(BACKWARD);
    delay(4250);
  }
  curtainMotor->run(RELEASE);
}
