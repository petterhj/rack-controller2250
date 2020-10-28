#include "Screen.h"
#include "Wire.h"

#define X                       0
#define Y                       16
#define W                       117
#define H                       29

// Icons
const unsigned char ambIcon[44] PROGMEM = {
    0x00, 0x00, 0x1c, 0x80, 0x23, 0x40, 0x22, 0x80, 0x22, 0x00, 0x2a, 0x00, 0x2a, 0x00, 0x2a, 0x00,
    0x2a, 0x00, 0x2a, 0x00, 0x49, 0x00, 0x5d, 0x00, 0x49, 0x00, 0x22, 0x00, 0x1c, 0x00, 0x00, 0x00,
    0x7f, 0x80, 0x4a, 0x80, 0x7d, 0x80, 0x5a, 0x80, 0x7f, 0x80, 0x00, 0x00
};

const unsigned char cpuIcon[44] PROGMEM = {
    0x00, 0x00, 0x1c, 0x80, 0x23, 0x40, 0x22, 0x80, 0x22, 0x00, 0x2a, 0x00, 0x2a, 0x00, 0x2a, 0x00,
    0x2a, 0x00, 0x2a, 0x00, 0x49, 0x00, 0x5d, 0x00, 0x49, 0x00, 0x22, 0x00, 0x1c, 0x00, 0x00, 0x00,
    0x14, 0x00, 0x3e, 0x00, 0x14, 0x00, 0x3e, 0x00, 0x14, 0x00, 0x00, 0x00
};

const unsigned char powerIcon[28] PROGMEM = {
    0x01, 0xe0, 0x01, 0xe0, 0x07, 0x80, 0x07, 0x80, 0x1e, 0x00, 0x1e, 0x00, 0x7f, 0xe0, 0x7f, 0xe0, 
    0x07, 0x80, 0x07, 0x80, 0x1e, 0x00, 0x1e, 0x00, 0x78, 0x00, 0x78, 0x00
};

const char * degree = "\xB0"; // °C

// ===============================================================
//  Screen
// ===============================================================
Screen::Screen() {
    this->oled = new OakOLED();
}

// Setup
void Screen::setup() {
    Wire.begin(0x3C); //////
    delay(1000); //////
    
    this->oled->begin();
    this->oled->setFont(&TomThumbRC);
    
    this->showBigString(F("INIT"));
}

void Screen::printTemp(int x, int y, int temp) {
    if (temp < 10) {
      x = round((x + ((39-20)/2)));
    } else if (temp >= 10 && temp < 100) {
      x = round((x + ((39-28)/2)));
    } else if (temp >= 100) {
      x = round((x + ((39-34)/2)));
    } else {
      x = round((x + ((39-14)/2)));    
    }
    if (temp >= 0) {
      this->oled->setCursor((x + 2), y);
      this->oled->print(temp);
      this->oled->print(" C");
    } else {
      this->oled->setCursor((x + 4), y);
      this->oled->print("--");
    }
}

void Screen::drawProgressBar(int x, int y, int prc) {
    this->oled->drawRect(x, y, 35, 4, 0xFF);   // Fan speed
    if (prc > 0 && prc <= 100) {
      int calc_prc = round((prc * 0.33));
      this->oled->fillRect((x+1), y, calc_prc, 4, 0xFF);
      DEBUG_print(F(" > "));
      DEBUG_print(calc_prc);
    }
}

// Show sensor display
void Screen::showSensorDisplay(bool showAll) {
    this->oled->clearDisplay();

    // Iterate groups
    /*int label_x = (X+14);
    
    for (int i = 0; i < 3; i++) {
        // Label
        this->oled->setTextSize(1);
    }*/

    //this->oled->drawRect(X, Y, 39, 20, 0xFF);
    //this->oled->drawRect((X+39), Y, 39, 20, 0xFF);
    //this->oled->drawRect((X+78), Y, 39, 20, 0xFF);

    // Headers
    this->oled->setTextSize(1);

    this->oled->setCursor((X+14), (Y+8));
    this->oled->print(F("AMB"));

    if (showAll) {
      this->oled->setCursor(((X+39)+14), (Y+8));
      this->oled->print(F("CPU"));
  
      this->oled->setCursor(((X+78)+14), (Y+8));
      this->oled->print(F("GPU"));
    }

    // Temperatures
    DEBUG_print(F("[VAL][TEMP] amb="));
    DEBUG_print(this->values[0]);
    DEBUG_print(F(", cpu="));
    DEBUG_print(this->values[2]);
    DEBUG_print(F(", gpu="));
    DEBUG_println(this->values[4]);
        
    this->oled->setTextSize(2);
    
    this->printTemp((X), (Y+22), this->values[0]);
    if (showAll) {
      this->printTemp((X+39), (Y+22), this->values[2]);
      this->printTemp((X+78), (Y+22), this->values[4]);
    }

    // Load
    DEBUG_print(F("[VAL][LOAD] fan="));
    DEBUG_print(this->values[1]);
    this->drawProgressBar((X+2), (Y+26), this->values[1]);

    DEBUG_print(F(", cpu="));
    DEBUG_print(this->values[3]);
    if (showAll) {
        this->drawProgressBar((X+41), (Y+26), this->values[3]);
    }
    
    DEBUG_print(F(", gpu="));
    DEBUG_print(this->values[5]);
    if (showAll) {
        this->drawProgressBar((X+80), (Y+26), this->values[5]);
    }

    DEBUG_println();

    this->oled->display();
}


// Show big string
void Screen::showBigString(String string) {
    string = string.substring(0, 14);
    int str_len = (string.length() * 8);
    int pad = round((W - str_len) / 2);
    
    DEBUG_print(F("[SCR] Showing string: "));
    DEBUG_println(string);
    
    this->oled->clearDisplay();
    this->oled->setTextSize(2);
    this->oled->setCursor((pad + 3), 37);
    this->oled->print(string);
    this->oled->display();
}

// Clear screen
void Screen::clearScreen() {
    this->oled->clearDisplay();
    //this->oled->drawBitmap(10, 25, powerIcon, 11, 14, 0xFFFF);
    this->oled->display();
}
