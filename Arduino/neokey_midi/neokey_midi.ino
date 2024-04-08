/*
 * Adapted from https://learn.adafruit.com/neokey-1x4-qt-i2c/arduino
 */

#include "Adafruit_NeoKey_1x4.h"
#include "seesaw_neopixel.h"

Adafruit_NeoKey_1x4 neokey;


#include <BLEMidi.h>

// First button decreases speed
// Second button increases speed

int speed = 1; // Slow default
const int min_speed = 0;
const int max_speed = 10;

void setup() {
  Serial.begin(115200);
  while (! Serial) delay(10);

  Serial.println("Initializing bluetooth");
  BLEMidiServer.begin("M&S");
  Serial.println("Waiting for connections...");
  //BLEMidiServer.enableDebugging();  // Uncomment if you want to see some debugging output from the library (not much for the server class...)

   
  if (! neokey.begin(0x30)) {
    Serial.println("Could not start NeoKey, check wiring?");
    while(1) delay(10);
  }
  
  Serial.println("NeoKey started!");

  for (uint16_t i=0; i<neokey.pixels.numPixels(); i++) {
    neokey.pixels.setPixelColor(i, Wheel(map(i, 0, neokey.pixels.numPixels(), 0, 255)));
    neokey.pixels.show();
    delay(50);
  }
  for (uint16_t i=0; i<neokey.pixels.numPixels(); i++) {
    neokey.pixels.setPixelColor(i, 0x000000);
    neokey.pixels.show();
    delay(50);
  }
}

uint8_t j=0;  // this variable tracks the colors of the LEDs cycle.

void loop() {
  uint8_t buttons = neokey.read();

  
  for (int i=0; i< neokey.pixels.numPixels(); i++) {
    neokey.pixels.setPixelColor(i, Wheel(((i * 256 / neokey.pixels.numPixels()) + j) & 255));
  }  
  
  if (buttons & (1<<0)) {
    Serial.println("Button A");

    // Increase speed
    speed += 1;

    if (speed > max_speed) {
      speed = max_speed;
    }
  } else {
    neokey.pixels.setPixelColor(0, 0);
  }

  if (buttons & (1<<1)) {
    Serial.println("Button B");

    // Decrease speed
    speed -= 1;
    if (speed < min_speed) {
      speed = min_speed;
    }
  } else {
    neokey.pixels.setPixelColor(1, 0);
  }
  
  if (buttons & (1<<2)) {
    Serial.println("Button C");
  } else {
    neokey.pixels.setPixelColor(2, 0);
  }

  if (buttons & (1<<3)) {
    Serial.println("Button D");
  } else {
    neokey.pixels.setPixelColor(3, 0);
  }  

  neokey.pixels.show();
  
  delay(10);    // don't print too fast
  j += speed;          // make colors cycle


  // Send MIDI as appropriate
  // TODO - trigger / hold based on key down / up
  if(BLEMidiServer.isConnected()) {             // If we've got a connection, we send an A4 during one second, at full velocity (127)

    if (buttons & (1<<0)) {
      BLEMidiServer.noteOn(0, 69, 127);
      Serial.println("NoteOn");
      delay(10);
      BLEMidiServer.noteOff(0, 69, 127);        // Then we make a delay of one second before returning to the beginning of the loop
      Serial.println("NoteOff");
    }
  }
}



/******************************************/

// Input a value 0 to 255 to get a color value.
// The colors are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return seesaw_NeoPixel::Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return seesaw_NeoPixel::Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return seesaw_NeoPixel::Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  return 0;
}
