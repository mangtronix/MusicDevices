//libraries

/*
#include <Adafruit_GFX.h>     // Core graphics library
#include <Adafruit_ST7789.h>  // Hardware-specific library for ST7789
#include <SPI.h>

// Use dedicated hardware SPI pins
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);
*/

// set pin numbers
const int touchPinR = 12;
const int touchPinY = 11;
const int touchPinG = 10;
const int touchPinB = 9;


const int ledPinR = 18;
const int ledPinY = 17;
const int ledPinG = 16;
const int ledPinB = 15;


// change with your threshold value
const int threshold = 25000;

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

void setup() {
  Serial.begin(115200);
  Serial.print(F("Hello! Feather TFT Test"));

  /*
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
  */

  Serial.println(F("Initialized"));

  pinMode(ledPinR, OUTPUT);
  pinMode(ledPinY, OUTPUT);
  pinMode(ledPinG, OUTPUT);
  pinMode(ledPinB, OUTPUT);
}

void loop() {
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

  // check if the touchValue is below the threshold
  // if it is, set ledPin to HIGH

  if (touchValueR > threshold) {
    redLED = true;
    digitalWrite(ledPinR, HIGH);
  } else {
    redLED = false;
    digitalWrite(ledPinR, LOW);
  }

  if (touchValueY > threshold) {
    yellowLED = true;
    digitalWrite(ledPinY, HIGH);
  } else {
    yellowLED = false;
    digitalWrite(ledPinY, LOW);
  }

  if (touchValueG > threshold) {
    greenLED = true;
    digitalWrite(ledPinG, HIGH);
  } else {
    greenLED = false;
    digitalWrite(ledPinG, LOW);
  }

  if (touchValueB > threshold) {
    blueLED = true;
    digitalWrite(ledPinB, HIGH);
  } else {
    blueLED = false;
    digitalWrite(ledPinB, LOW);
  }

  /*
  updateScreen();
  */
}

/*
void updateScreen() {
  tft.setCursor(0, 0);
  tft.setTextSize(2);
  tft.fillScreen(ST77XX_BLACK);

  tft.setTextColor(ST77XX_RED);
  tft.print("1 ");
  tft.print(touchValueR);
  if (redLED) {
    tft.print("ON");
  }
  tft.println();

  tft.setTextColor(ST77XX_YELLOW);
  tft.print("2 ");
  tft.print(touchValueY);
  if (yellowLED) {
    tft.print("ON");
  }
  tft.println();

  tft.setTextColor(ST77XX_GREEN);
  tft.print("3 ");
  tft.print(touchValueG);
  if (greenLED) {
    tft.print("ON");
  }
  tft.println();

  tft.setTextColor(ST77XX_BLUE);
  tft.print("4 ");
  tft.print(touchValueB);
  if (blueLED) {
    tft.print("ON");
  }
  tft.println();

  delay(100);
}
*/
