#include "Temperature.h"

#define THERMISTOR_NOMINAL      10000 // resistance at 25 degrees C
#define TEMP_NOMINAL            25 // temp. for nominal resistance (almost always 25 C)
#define TEMP_NUMSAMPLES         5
#define TEMP_BCOEFFICIENT       3950 // beta coefficient of the thermistor (usually 3000-4000)
#define TEMP_SERIESRESISTOR     10000 // value of the 'other' resistor


// ===============================================================
//  Temperature
// ===============================================================
Temperature::Temperature(int sensorPin) {
  this->sensorPin = sensorPin;
}

// Setup
void Temperature::setup() {
    pinMode(this->sensorPin, INPUT);
}

// Read
float Temperature::read() {
    uint8_t i;
    float average;
    int temp_samples[TEMP_NUMSAMPLES];

    // take N samples in a row, with a slight delay
    for (i=0; i < TEMP_NUMSAMPLES; i++) {
        temp_samples[i] = analogRead(this->sensorPin);
        delay(10);
    }

    // average all the samples out
    average = 0;
    for (i=0; i< TEMP_NUMSAMPLES; i++) {
     average += temp_samples[i];
    }
    average /= TEMP_NUMSAMPLES;

    DEBUG_print(F("[TMP] "));
    DEBUG_print(F("Avg. analog reading="));
    DEBUG_print(average);

    // convert the value to resistance
    average = 1023 / average - 1;
    average = TEMP_SERIESRESISTOR / average;
    
    DEBUG_print(F(", thermistor resistance="));
    DEBUG_print(average);

    float steinhart;
    steinhart = average / THERMISTOR_NOMINAL;     // (R/Ro)
    steinhart = log(steinhart);                  // ln(R/Ro)
    steinhart /= TEMP_BCOEFFICIENT;                   // 1/B * ln(R/Ro)
    steinhart += 1.0 / (TEMP_NOMINAL + 273.15); // + (1/To)
    steinhart = 1.0 / steinhart;                 // Invert
    steinhart -= 273.15;                         // convert to C

    DEBUG_print(F(", temp="));
    DEBUG_print(steinhart);
    DEBUG_println(F("*C"));

    if (steinhart < 0) {
      return 0;
    } else {
      return round(steinhart);
    }
}
