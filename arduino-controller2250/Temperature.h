#ifndef Temperature_h
#define Temperature_h

//#define DEBUG

#include "Debug.h"
#include "Arduino.h"
#include "Temperature.h"

class Temperature
{
  public:
    Temperature(int sensorPin);
    void setup();
    float read();

  private:
    int *sensorPin;
};

#endif
