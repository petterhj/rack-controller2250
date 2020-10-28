#ifndef Screen_h
#define Screen_h

//#define DEBUG

#include "Debug.h"
#include "Arduino.h"
#include "Wire.h"
#include "Adafruit_GFX.h"
#include "TomThumbRC.h"
#include "OakOLED.h"

class Screen
{
  public:
    Screen();
    void setup();

    void showSensorDisplay(bool showAll = true);
    void showBigString(String string);
    void clearScreen();
    
    int values[6] = {-1, -1, -1, -1, -1, -1};
    
  private:
    void printTemp(int x, int y, int temp);
    void drawProgressBar(int x, int y, int prc);
      
    OakOLED* oled;
};

#endif
