#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {

   pinMode(10, INPUT);
   pinMode(11, OUTPUT);
   Serial.begin(115200);
   mySerial.begin(115200);
}

void loop() { // run over and over
   Serial.println("tesHardware");
   mySerial.println("tesSoftware");
   delay(1000);
}

