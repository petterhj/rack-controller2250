#ifndef Fan_h
#define Fan_h

//#define DEBUG

#include "Debug.h"
#include "Arduino.h"


class Fan
{
  public:
    Fan(int fanPwmPin, int fanRpmPin);
    void setup();

    int setSpeedLevel(int percent);
    int getSpeedLevel();
    int getFanSpeed();
    
  private:
    int fanPwmPin;
    int fanRpmPin;
    int currentSpeedLevel;
};

#endif
