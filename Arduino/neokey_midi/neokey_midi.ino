/*
 * Adapted from https://learn.adafruit.com/neokey-1x4-qt-i2c/arduino
 * 
 * Michael Ang
 * @mangtronix
 #
 # 2024-04
 */

#include "Adafruit_NeoKey_1x4.h"
#include "seesaw_neopixel.h"

// Speed for I2C in attempt to go faster - $$$ causes glitches - need to change pullups?
// #define I2C_SPEED 400000

// Serial debugging of notes, etc
// #define SERIAL_DEBUG

// NeoSlider
// A0 on back was cut to give 0x31 I2C address
#define  NEOSLIDER_I2C_ADDR 0x31
#define  NEOSLIDER_ANALOGIN   18
#define  NEOSLIDER_PIXELOUT 14

uint16_t last_slide_val = 0;
uint8_t slide_tolerance = 1;

Adafruit_seesaw seesaw;
seesaw_NeoPixel slider_pixels = seesaw_NeoPixel(4, NEOSLIDER_PIXELOUT, NEO_GRB + NEO_KHZ800);

// NeoKey
Adafruit_NeoKey_1x4 neokey;
uint8_t previous_buttons = 0;
const int num_keys = 4;

// Display
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Adafruit_Debounce.h>

Adafruit_SH1107 display = Adafruit_SH1107(64, 128, &Wire);

#define BUTTON_A 15
#define BUTTON_B 32
#define BUTTON_C 14

// BUTTON_C is physically at top in this design
Adafruit_Debounce buttonA(BUTTON_C, LOW);
Adafruit_Debounce buttonB(BUTTON_B, LOW);
Adafruit_Debounce buttonC(BUTTON_A, LOW);

//// MIDI

uint8_t midi_channel = 0;

// $$$ add more scales
// Em pentatonic
uint8_t note_count = 4;
uint8_t notes[] = {64,67,69,71};
// uint8_t notes[] = {71, 69, 67, 64}; // Physical layout is reversed
uint8_t note_on[] = {false, false, false, false}; // Track note status

uint8_t cc_number = 0;
uint8_t last_cc_val = 0;

#include <BLEMidi.h>

int ble_midi_was_connected = 0;

// It takes a long time between BLE connection and Ableton receiving the messages
// We send all notes off multiple times after connection
const int ble_noteoff_resends = 8;
const int ble_resend_delay = 500;

// First button decreases speed
// Second button increases speed

int speed = 1; // Slow default
const int min_speed = 0;
const int max_speed = 10;

void setup() {
  Serial.begin(115200);

  while (! Serial) delay(10);

  #ifdef SERIAL_DEBUG
  delay(100); // For host serial to be ready to receive
  #endif

  Serial.println("Mangtronix coming online");

  // Set up display
  setupDisplay();

  if (!seesaw.begin(NEOSLIDER_I2C_ADDR)) {
    Serial.println(F("NeoSlider seesaw not found!"));
    // TODO -  continue without neoslider

    while(1) delay(10); // wait forever
  }

  uint16_t pid;
  uint8_t year, mon, day;

  seesaw.getProdDatecode(&pid, &year, &mon, &day);
  Serial.print("seesaw found PID: ");
  Serial.print(pid);
  Serial.print(" datecode: ");
  Serial.print(2000+year); Serial.print("/");
  Serial.print(mon); Serial.print("/");
  Serial.println(day);

  if (pid != 5295) {
    Serial.println(F("Wrong NeoSlider seesaw PID"));
    while (1) delay(10);
  }
  if (!slider_pixels.begin(NEOSLIDER_I2C_ADDR)){
    Serial.println("seesaw pixels not found!");
    while(1) delay(10);
  }
  Serial.println(F("NeoSlider seesaw started OK!"));

  slider_pixels.setBrightness(255);
  slider_pixels.clear();
  slider_pixels.show(); // Initialize all pixels


  Serial.println("Initializing bluetooth");
  BLEMidiServer.begin("M&S");
  Serial.println("Available for connections...");
  updateStatus("Waiting...");
  //BLEMidiServer.enableDebugging();  // Uncomment if you want to see some debugging output from the library (not much for the server class...)

  Serial.println("Connecting to NeoKey");
  if (! neokey.begin(0x30)) {
    Serial.println("Could not start NeoKey, check wiring?");
    while(1) delay(10);
  }
  
  Serial.println("NeoKey started!");

  #ifdef I2C_SPEED
  Serial.print("Setting I2C speed ");
  Serial.println(I2C_SPEED);
  Wire.setClock(I2C_SPEED);
  #endif


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

  Serial.println("Setup finished");
}

uint8_t j=0;  // this variable tracks the colors of the LEDs cycle.

void loop() {
  int display_needs_redraw = 0;

  // $$$ change to using interrupt?
  // Read buttons
  uint8_t buttons = neokey.read();

  // Read slider - ignore small changes
  uint16_t slide_val = seesaw.analogRead(NEOSLIDER_ANALOGIN);
  if (abs(slide_val - last_slide_val) > slide_tolerance) {
    #ifdef SERIAL_DEBUG
    Serial.println(slide_val);
    #endif
    last_slide_val = slide_val;
  }

  // Update slider NeoPixels
  // TODO - only if changed
  for (uint8_t i=0; i< slider_pixels.numPixels(); i++) {
    // $$$ better mapping of colours
    slider_pixels.setPixelColor(i, Wheel(slide_val / 8)); // Go halfway through wheel (don't loop back to same color)
  }
  slider_pixels.show();
  
  // Update pixels every loop - $$$ should be timed animation instead
  // If the buttons are *not* pressed the color will get set to black
  for (int i=0; i< neokey.pixels.numPixels(); i++) {
    neokey.pixels.setPixelColor(i, Wheel(((i * 256 / neokey.pixels.numPixels()) + j) & 255));
  }  
  
  if (buttons & (1<<0)) {
    #ifdef SERIAL_DEBUG
    Serial.println("Button A");
    #endif

    // Increase speed
    speed += 1;

    if (speed > max_speed) {
      speed = max_speed;
    }
  } else {
    neokey.pixels.setPixelColor(0, 0);
  }

  if (buttons & (1<<1)) {
    #ifdef SERIAL_DEBUG
    Serial.println("Button B");
    #endif

    // Decrease speed
    speed -= 1;
    if (speed < min_speed) {
      speed = min_speed;
    }
  } else {
    neokey.pixels.setPixelColor(1, 0);
  }
  
  if (buttons & (1<<2)) {
    #ifdef SERIAL_DEBUG
    Serial.println("Button C");
    #endif
  } else {
    neokey.pixels.setPixelColor(2, 0);
  }

  if (buttons & (1<<3)) {
    #ifdef SERIAL_DEBUG
    Serial.println("Button D");
    #endif
  } else {
    neokey.pixels.setPixelColor(3, 0);
  }  

  previous_buttons = buttons;

  // Needs to be updated every loop for (untimed) cycling animations
  neokey.pixels.show();
  
  // $$$ take out arbitrary delay
  //delay(10);    // don't print too fast
  j += speed;          // make colors cycle


  // Send MIDI as appropriate
  if(BLEMidiServer.isConnected()) {             // If we've got a connection, we send an A4 during one second, at full velocity (127)
    if (!ble_midi_was_connected) {
      Serial.println("BLE MIDI connected");
      updateStatus("Connected");
      display.display(); // OK to do here, waiting anyway

      // It takes time for the connection to be active, and then more
      // time for Ableton to set up its connection
      allNotesOff();
      Serial.print(F("  Sending all notes off "));
      Serial.print(ble_noteoff_resends);
      Serial.println(F(" times"));
      for (int i = 0; i < ble_noteoff_resends; i++) {
        Serial.print(F("  Wait "));
        Serial.print(i + 1);
        Serial.print(" ");
        Serial.println(ble_resend_delay);
        delay(ble_resend_delay);
        allNotesOff();
      }
      ble_midi_was_connected = true;
    }

    // Send notes
    for (int i = 0; i < num_keys; i++) {
      // Check button state
      if (buttons & (1<<i)) {
        // Button is just pressed or held
        if (!note_on[i]) {
          // Turn note on
          BLEMidiServer.noteOn(midi_channel, notes[i], 127);
          note_on[i] = true;
        }
      } else {
        if (note_on[i]) {
          BLEMidiServer.noteOff(midi_channel, notes[i], 127);
          note_on[i] = false;
        }
      }
    }
  } else {
    // Not connected
    if (ble_midi_was_connected) {
      Serial.println("Disconnected");
      updateStatus("Disconnected");
      display_needs_redraw = true;
      ble_midi_was_connected = 0;
    }
  }

  // Send controllers
  uint8_t cc_val = sliderToCC(slide_val);
  if (cc_val != last_cc_val) {
    BLEMidiServer.controlChange(midi_channel, cc_number, cc_val);
    last_cc_val = cc_val;
  }


  // Update display

  buttonA.update();
  buttonB.update();
  buttonC.update();

  // Board is rotated, remap buttons

  if(buttonA.justPressed()) {
    updateStatus("Button A");
    allNotesOff(); // XXX for testing
    display_needs_redraw = true;
  }

  if(buttonB.justPressed()) {
    updateStatus("Button B");
    display_needs_redraw = true;
  }

  if(buttonC.justPressed()) {
    // Clear screen
    display.fillScreen(0);
    display.setCursor(0,0);
    display_needs_redraw = true;
  }

  if (display_needs_redraw) {
    display.display();
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

uint8_t sliderToCC(uint16_t sliderVal) {
  return sliderVal / 8;
}

void setupDisplay() {
  Serial.println("128x64 OLED FeatherWing test");
  delay(250); // wait for the OLED to power up
  display.begin(0x3C, true); // Address 0x3C default

  Serial.println("OLED begun");

  // Clear the buffer.
  display.clearDisplay();
  display.display();

  display.setRotation(3);

  // text display tests
  display.setTextSize(2);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0,0);
  display.println("Mangtronix");
  display.setTextSize(1);
  display.display(); // actually display all of the above


  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);
  buttonA.begin();
  buttonB.begin();
  buttonC.begin();

}

void allNotesOff() {
  if(BLEMidiServer.isConnected()) {
    Serial.println("All notes off");
    BLEMidiServer.controlChange(midi_channel, 123, 0);
  }
}

// Update status line of screen
void updateStatus(char* message) {
  // Use fixed length buffer so we can overwrite existing text
  char buffer[] = "                \0";
  int x = 0, y = 30, w = 128, h = 30; // $$$ get width from display
  strncpy(buffer, message, strlen(buffer));
  display.fillRect(x, y, w, h, 0);
  display.setCursor(x, y);
  display.print(buffer);
}
