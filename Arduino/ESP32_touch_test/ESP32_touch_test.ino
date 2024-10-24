/*
 * ESP32-S3 Touch Test
 *
 * Read touch values from pins and write to serial.
 * Use Tools->Serial Plotter to see graph of values
 */

// Which pins to read from
int touchPins[] = {5,6,9,10,-1}; // -1 indicates end of array
int loopDelay = 50;

void setup() {
  Serial.begin(115200);
  delay(1000); // Wait for serial
  Serial.println("ESP32-S3 touch test");

  Serial.println("Using pins:");
  for (int i = 0; ; i++) {
    int touchPin = touchPins[i];
    if (touchPin == -1) { // sentinel value at end of array
      break; 
    }
    Serial.print("  ");
    Serial.println(touchPin);
  }
}

void loop() {
  for (int i = 0; ; i++) {
    int touchPin = touchPins[i];
    if (touchPin == -1) { // finished going through values
      break; // break out of loop
    }

    int value = touchRead(touchPin);

    // Add a comma between values
    if (i > 0) {
      Serial.print(",");
    }
    Serial.print(value);  // get value of Touch 0 pin = GPIO 4
  }
  Serial.println(); // end line

  delay(loopDelay);
}