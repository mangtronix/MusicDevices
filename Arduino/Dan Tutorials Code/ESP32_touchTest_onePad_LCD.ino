//Original Code from https://randomnerdtutorials.com/esp32-touch-pins-arduino-ide/
//Modified by Daniel Woc
#include <Adafruit_GFX.h>    
#include <Adafruit_ST7789.h>  
#include <SPI.h>


Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);


const int touchPin = 12;
const int ledPin = 16;


const int threshold = 25000;
int touchValue;
bool LED = false;


void setup() {
 Serial.begin(9600);
 Serial.print(F("Hello! Feather TFT Test"));


 pinMode(TFT_BACKLITE, OUTPUT);
 digitalWrite(TFT_BACKLITE, HIGH);


 pinMode(TFT_I2C_POWER, OUTPUT);
 digitalWrite(TFT_I2C_POWER, HIGH);
 delay(10);


 tft.init(135, 240);  
 tft.setRotation(3);
 tft.fillScreen(ST77XX_BLACK);


 Serial.println(F("Initialized"));


 pinMode(ledPin, OUTPUT);
}


void loop() {
 touchValue = touchRead(touchPin);


 Serial.print(touchValue);


 if (touchValue > threshold) {
   LED = true;
   digitalWrite(ledPin, HIGH);
 } else {
   LED = false;
   digitalWrite(ledPin, LOW);
 }


 updateScreen();


 delay(100);
}


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
}
