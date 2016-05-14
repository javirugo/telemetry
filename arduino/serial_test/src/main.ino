#include <SoftwareSerial.h>

SoftwareSerial mySerial(11, 10); // RX, TX

void setup() {

   Serial.begin(115200);
   mySerial.begin(115200);
}

void loop() { // run over and over
   Serial.println("tesHardware");
   mySerial.println("tesSoftware");
   delay(1000);
}

