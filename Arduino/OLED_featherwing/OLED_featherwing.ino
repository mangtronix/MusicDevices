/*
 * Adapted from https://learn.adafruit.com/adafruit-128x64-oled-featherwing/arduino-code
 */


#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Adafruit_Debounce.h>

Adafruit_SH1107 display = Adafruit_SH1107(64, 128, &Wire);

// OLED FeatherWing buttons map to different pins depending on board:
#if defined(ESP8266)
  #define BUTTON_A  0
  #define BUTTON_B 16
  #define BUTTON_C  2
#elif defined(ESP32) && !defined(ARDUINO_ADAFRUIT_FEATHER_ESP32S2)
  #define BUTTON_A 15
  #define BUTTON_B 32
  #define BUTTON_C 14
#elif defined(ARDUINO_STM32_FEATHER)
  #define BUTTON_A PA15
  #define BUTTON_B PC7
  #define BUTTON_C PC5
#elif defined(TEENSYDUINO)
  #define BUTTON_A  4
  #define BUTTON_B  3
  #define BUTTON_C  8
#elif defined(ARDUINO_NRF52832_FEATHER)
  #define BUTTON_A 31
  #define BUTTON_B 30
  #define BUTTON_C 27
#else // 32u4, M0, M4, nrf52840, esp32-s2 and 328p
  #define BUTTON_A  9
  #define BUTTON_B  6
  #define BUTTON_C  5
#endif

// BUTTON_C is physically at top
Adafruit_Debounce buttonA(BUTTON_C, LOW);
Adafruit_Debounce buttonB(BUTTON_B, LOW);
Adafruit_Debounce buttonC(BUTTON_A, LOW);


void setup() {
  Serial.begin(115200);

  Serial.println("128x64 OLED FeatherWing test");
  delay(250); // wait for the OLED to power up
  display.begin(0x3C, true); // Address 0x3C default

  Serial.println("OLED begun");

  // Show image buffer on the display hardware.
  // Since the buffer is intialized with an Adafruit splashscreen
  // internally, this will display the splashscreen.
  display.display();
  delay(1000);

  // Clear the buffer.
  display.clearDisplay();
  display.display();

  display.setRotation(3);
  Serial.println("Button test");

  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);
  buttonA.begin();
  buttonB.begin();
  buttonC.begin();

  // text display tests
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0,0);
  display.print("Mangtronix");
  display.display(); // actually display all of the above
}

void loop() {
  int displayNeedsRedraw = 0;

  buttonA.update();
  buttonB.update();
  buttonC.update();

  // Board is rotated, remap buttons

  if(buttonA.justPressed()) {
    display.print("A");
    displayNeedsRedraw = true;
  }

  if(buttonB.justPressed()) {
    display.print("B");
    displayNeedsRedraw = true;
  }

  if(buttonC.justPressed()) {
    // Clear screen
    display.fillScreen(0);
    display.setCursor(0,0);
    displayNeedsRedraw = true;
  }

  if (displayNeedsRedraw) {
    display.display();
  }

  // Debounce delay
  // $$$ remove if not needed
  delay(10);

}
