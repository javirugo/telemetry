#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

MPU6050 accelgyro; //MPU6050 accelgyro(0x69); // <-- use for AD0 high
int16_t ax, ay, az, gx, gy, gz, degrees_x, gforce; // MP6050

void setup() {

   // MP6050
   Wire.begin();
   accelgyro.initialize();

   Serial.begin(38400);
}

void loop() {
   accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
   degrees_x = round(ax /180); 
   gforce = gy;

   // GForce Max: 32768
   Serial.print("degrees: "); Serial.print(degrees_x); Serial.print("  ");
   Serial.print("gforce: "); Serial.print(gforce); Serial.print("\n");
}
