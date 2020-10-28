// Libraries
/*#include "Wire.h"
#include "Adafruit_GFX.h"
#include "Fonts/TomThumb.h"
#include "PushButton.h"*/

//#define DEBUG

#include "Debug.h"
#include "Temperature.h"
#include "Fan.h"
#include "Screen.h"

#define SERIAL_BAUD_RATE        115200
#define THERMISTOR_PIN          A0
#define POWER_LED_PIN           2
#define BUTTON_1_PIN            4
#define BUTTON_2_PIN            5
#define BUTTON_3_PIN            6
#define FAN_SENSE_PIN           7
#define FAN_PWM_PIN             10
#define FANTEMP_CHECK_INTERVAL  3000
#define SERIAL_CONNECT_TIMEOUT  3000
#define LED_BLINK_INTERVAL      5000

Temperature temp = Temperature(THERMISTOR_PIN);
Fan fan = Fan(FAN_PWM_PIN, FAN_SENSE_PIN);
Screen screen = Screen();

unsigned long currentMillis = 0;
unsigned long previousFanTempCheck = 0;
unsigned long previousSerialMsg = millis();
unsigned long previousLedBlink = 0;
bool serialConnected = false;
bool ledOn = true;

/*
PushButton button1(BUTTON_1_PIN);
PushButton button2(BUTTON_2_PIN);
PushButton button3(BUTTON_3_PIN);
*/

// Setup
//====================================
void setup() {
    Serial.begin(SERIAL_BAUD_RATE);
    DEBUG_println("Initializing...");
  
    pinMode(POWER_LED_PIN, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(BUTTON_1_PIN, INPUT_PULLUP);
    pinMode(BUTTON_2_PIN, INPUT_PULLUP);
    pinMode(BUTTON_3_PIN, INPUT_PULLUP);

    digitalWrite(POWER_LED_PIN, HIGH);

    // Setup modules
    screen.setup();
    temp.setup();
    fan.setup();

    // Read initial values
    screen.values[0] = temp.read();
    screen.values[1] = fan.getFanSpeed();

    screen.showSensorDisplay(false);
}

void loop() {
  currentMillis = millis();
  
  // Update temperature and fan speed
  if (currentMillis - previousFanTempCheck > FANTEMP_CHECK_INTERVAL) {
      screen.values[0] = temp.read();
      screen.values[1] = fan.getFanSpeed();

      screen.showSensorDisplay(serialConnected);
      
      previousFanTempCheck = millis();
  }

  // Serial connection timeout
  if (currentMillis - previousSerialMsg > SERIAL_CONNECT_TIMEOUT) {
      serialConnected = false;
      //screen.clearScreen();
      /*
      if (currentMillis - previousLedBlink > LED_BLINK_INTERVAL) {
          digitalWrite(POWER_LED_PIN, LOW);
          delay(500);
          digitalWrite(POWER_LED_PIN, HIGH);
          //ledOn = !ledOn;
          previousLedBlink = millis();
      }*/
  }
  
  // Serial interface
  while(Serial.available()) {
      String cmd = Serial.readStringUntil('=');
      
      if (cmd == "VAL") {
          Serial.println("OK:VAL");
          for (int i = 2; i < 6; i++){
              screen.values[i] = Serial.readStringUntil(',').toInt();
          }
          Serial.readStringUntil('\n');
          screen.showSensorDisplay();
      }
      else if (cmd == "STR") {
          Serial.println("OK:STR");
          String str = Serial.readStringUntil('\n');//Until('|');
          screen.showBigString(str);
      }

      previousSerialMsg = millis();
      serialConnected = true;
      digitalWrite(POWER_LED_PIN, HIGH);
  }

  // Set fanspeed (based on ambient temperature)
  int temp = screen.values[0];
  //fan.setSpeedLevel(50);
  
  if (temp < 20) {
      fan.setSpeedLevel(15);
  } else if (temp >= 15 && temp < 30) {
      fan.setSpeedLevel(25);
  } else if (temp >= 30 && temp < 40) {
      fan.setSpeedLevel(65);
  } else if (temp >= 40) {
      fan.setSpeedLevel(100);
  }
}
