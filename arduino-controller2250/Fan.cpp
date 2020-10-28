#include "Fan.h"

// ===============================================================
//  Fan
// ===============================================================
Fan::Fan(int fanPwmPin, int fanRpmPin) {
    this->fanPwmPin = fanPwmPin;
    this->fanRpmPin = fanRpmPin;
    this->currentSpeedLevel = 0;
}

// Setup
void Fan::setup() {
    pinMode(this->fanRpmPin, INPUT_PULLUP);

    this->setSpeedLevel(30);
}

// Set fan speed level
int Fan::setSpeedLevel(int percent) {
    if (percent != this->currentSpeedLevel) {
        if (percent >= 0 && percent <= 100) {
            DEBUG_print(F("[FAN] Setting fan speed level="));
            DEBUG_print(percent);
    
            int pwm = ((percent * 255) / 100);
    
            analogWrite(this->fanPwmPin, pwm);
    
            this->currentSpeedLevel = percent;
    
            DEBUG_print(F(", pwm="));
            DEBUG_println(pwm);
        } else {
            DEBUG_println(F("Invalid fan speed (range 0-100)"));
        }
    }
}

// Get fan speed
int Fan::getSpeedLevel() {
    return this->currentSpeedLevel;
}

// Get fan speed in percent of max RPM
int Fan::getFanSpeed() {
    DEBUG_print(F("[FAN] "));

    long pulseDuration = pulseIn(this->fanRpmPin, LOW);
    double frequency = 1000000 / pulseDuration;
    
    int rpm = 0;
    
    if (pulseDuration > 0) {
        rpm = (frequency / 2 * 60 / 2);
    }

    DEBUG_print(F("Pulse duration="));
    DEBUG_print(pulseDuration);
    DEBUG_print(F(", frequency="));
    DEBUG_print(frequency);
    DEBUG_print(F(", level="));
    DEBUG_print(this->currentSpeedLevel);
    DEBUG_print(F(", rpm="));
    DEBUG_print(rpm);

    int prc = round((rpm / 2200.0) * 100);
    
    DEBUG_print(F(", prc="));
    DEBUG_println(prc);
  
    if (prc >= 0 && prc <= 100) { return prc; } 
    else if (prc > 100) { return 100; }
    else { return 0; }
}
