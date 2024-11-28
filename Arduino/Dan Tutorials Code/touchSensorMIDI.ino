// Original code 
// LCD Screen - https://learn.adafruit.com/esp32-s3-reverse-tft-feather/built-in-tft
// MIDI - Examples from Adafruit Feather ESP32-S3 Reverse TFT -> USB -> MIDI -> MIDIController
// Modified by Daniel Woc

#if ARDUINO_USB_MODE
#warning This sketch should be used when USB is in OTG mode
void setup() {}
void loop() {}
#else

#define LCD_SCREEN
#ifdef LCD_SCREEN
#include <Adafruit_GFX.h>     // Core graphics library
#include <Adafruit_ST7789.h>  // Hardware-specific library for ST7789
#include <SPI.h>

// Use dedicated hardware SPI pins
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);
#endif

#include <math.h>
#include "USB.h"
#include "USBMIDI.h"
USBMIDI MIDI;

#define MIDI_NOTE_C4 60
#define MIDI_NOTE_D4 62
#define MIDI_NOTE_E4 64
#define MIDI_NOTE_F4 65

#define MIDI_NOTE_E2 40
#define MIDI_NOTE_A2 45
#define MIDI_NOTE_D3 52
#define MIDI_NOTE_G3 57 

#define MIDI_CC_CUTOFF 74

///// ADC & Controller Input Handling /////
#define CONTROLLER_PIN 5

// ESP32 ADC needs a ton of smoothing
#define SMOOTHING_VALUE 1000
static double controllerInputValue = 0;

const int screenUpdateMillis = 100; // 10 Hz screen update
static int lastScreenUpdate = 0; // time of last update

void updateControllerInputValue() {
  controllerInputValue = (controllerInputValue * (SMOOTHING_VALUE - 1) + analogRead(CONTROLLER_PIN)) / SMOOTHING_VALUE;
}

void primeControllerInputValue() {
  for (int i = 0; i < SMOOTHING_VALUE; i++) {
    updateControllerInputValue();
  }
}

uint16_t readControllerValue() {
  // Lower ADC input amplitude to get a stable value
  return round(controllerInputValue / 12);
}

//"Button" Handling
const int touchPinR = 12;
const int touchPinY = 11;
const int touchPinG = 10;
const int touchPinB = 9;

// change with your threshold value
const int threshold = 75000;

// variable for storing the touch pin value
int touchValueR;
int touchValueY;
int touchValueG;
int touchValueB;

//booleans for updating the screen
bool redLED = false;
bool yellowLED = false;
bool greenLED = false;
bool blueLED = false;

// Simple button state transition function with debounce
// (See also: https://tinyurl.com/simple-debounce)
#define PRESSED 0xff00
#define RELEASED 0xfe1f

uint16_t getButtonOneEvent() {
  static uint16_t state = 0;
  state = (state << 1) | !redLED | 0xfe00;
  return state;
}

uint16_t getButtonTwoEvent() {
  static uint16_t state = 0;
  state = (state << 1) | !yellowLED | 0xfe00;
  return state;
}

uint16_t getButtonThreeEvent() {
  static uint16_t state = 0;
  state = (state << 1) | !greenLED | 0xfe00;
  return state;
}

uint16_t getButtonFourEvent() {
  static uint16_t state = 0;
  state = (state << 1) | !blueLED | 0xfe00;
  return state;
}

///// Arduino Hooks /////
void setup() {
  Serial.begin(115200);
  MIDI.begin();
  USB.begin();
  primeControllerInputValue();

#ifdef LCD_SCREEN
  // turn on backlite
  pinMode(TFT_BACKLITE, OUTPUT);
  digitalWrite(TFT_BACKLITE, HIGH);

  // turn on the TFT / I2C power supply
  pinMode(TFT_I2C_POWER, OUTPUT);
  digitalWrite(TFT_I2C_POWER, HIGH);
  delay(10);

  // initialize TFT
  tft.init(135, 240);  // Init ST7789 240x135
  tft.setRotation(3);
  tft.fillScreen(ST77XX_BLACK);
#endif
}

void loop() {
  //Touch
  touchValueR = touchRead(touchPinR);
  touchValueY = touchRead(touchPinY);
  touchValueG = touchRead(touchPinG);
  touchValueB = touchRead(touchPinB);

  Serial.print(touchValueR);
  Serial.print(",");
  Serial.print(touchValueY);
  Serial.print(",");
  Serial.print(touchValueG);
  Serial.print(",");
  Serial.print(touchValueB);
  Serial.println();

  if (touchValueR > threshold) {
    redLED = true;
  } else {
    redLED = false;
  }

  if (touchValueY > threshold) {
    yellowLED = true;
  } else {
    yellowLED = false;
  }

  if (touchValueG > threshold) {
    greenLED = true;
  } else {
    greenLED = false;
  }

  if (touchValueB > threshold) {
    blueLED = true;
  } else {
    blueLED = false;
  }

  //MIDI
  uint16_t newControllerValue = readControllerValue();
  static uint16_t lastControllerValue = 0;

  // Auto-calibrate the controller range
  static uint16_t maxControllerValue = 0;
  static uint16_t minControllerValue = 0xFFFF;

  if (newControllerValue < minControllerValue) {
    minControllerValue = newControllerValue;
  }
  if (newControllerValue > maxControllerValue) {
    maxControllerValue = newControllerValue;
  }

  // Send update if the controller value has changed
  if (lastControllerValue != newControllerValue) {
    lastControllerValue = newControllerValue;

    // Can't map if the range is zero
    if (minControllerValue != maxControllerValue) {
      MIDI.controlChange(MIDI_CC_CUTOFF, map(newControllerValue, minControllerValue, maxControllerValue, 0, 127));
    }
  }
  updateControllerInputValue();

  // Hook Button0 to a MIDI note so that we can observe
  // the CC effect without the need for a MIDI keyboard.
  switch (getButtonOneEvent()) {
    case PRESSED: MIDI.noteOn(MIDI_NOTE_E2, 64); break;
    case RELEASED: MIDI.noteOff(MIDI_NOTE_E2, 0); break;
    default: break;
  }

  switch (getButtonTwoEvent()) {
    case PRESSED: MIDI.noteOn(MIDI_NOTE_A2, 64); break;
    case RELEASED: MIDI.noteOff(MIDI_NOTE_A2, 0); break;
    default: break;
  }

  switch (getButtonThreeEvent()) {
    case PRESSED: MIDI.noteOn(MIDI_NOTE_D3, 64); break;
    case RELEASED: MIDI.noteOff(MIDI_NOTE_D3, 0); break;
    default: break;
  }

  switch (getButtonFourEvent()) {
    case PRESSED: MIDI.noteOn(MIDI_NOTE_G3, 64); break;
    case RELEASED: MIDI.noteOff(MIDI_NOTE_G3, 0); break;
    default: break;
  }

#ifdef LCD_SCREEN
  int now = millis();
  if ((now - lastScreenUpdate) > screenUpdateMillis) {
    updateScreen();
    lastScreenUpdate = now;
  }
#endif
}

#ifdef LCD_SCREEN
void updateScreen() {
  tft.setCursor(0, 0);
  tft.setTextSize(2);
  tft.fillScreen(ST77XX_BLACK);

  tft.setTextColor(ST77XX_RED);
  tft.print("1 ");
  tft.print(touchValueR);
  if (redLED) {
    tft.setCursor(200, 0);
    tft.print(" ON");
    tft.setCursor(0, 0);
  }
  tft.println();

  tft.setTextColor(ST77XX_YELLOW);
  tft.print("2 ");
  tft.print(touchValueY);
  if (yellowLED) {
    tft.setCursor(200, 15);
    tft.print(" ON");
    tft.setCursor(0, 15);
  }
  tft.println();

  tft.setTextColor(ST77XX_GREEN);
  tft.print("3 ");
  tft.print(touchValueG);
  if (greenLED) {
    tft.setCursor(200, 30);
    tft.print(" ON");
    tft.setCursor(0, 30);
  }
  tft.println();

  tft.setTextColor(ST77XX_BLUE);
  tft.print("4 ");
  tft.print(touchValueB);
  if (blueLED) {
    tft.setCursor(200, 45);
    tft.print(" ON");
    tft.setCursor(0, 45);
  }
  tft.println();

  // delay(5);
}
#endif
#endif /* ARDUINO_USB_MODE */

