/*
Debug.h - Simple debugging utilities.
*/

#ifndef DEBUGUTILS_H
#define DEBUGUTILS_H

#ifdef DEBUG
  #define DEBUG_print(...) Serial.print(__VA_ARGS__)
  #define DEBUG_println(...) Serial.println(__VA_ARGS__)
#else
  #define DEBUG_print(...)
  #define DEBUG_println(...)
#endif

#endif
