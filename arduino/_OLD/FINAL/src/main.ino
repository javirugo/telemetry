#include <SoftwareSerial.h>
#include <KDSPort.h>
// #include "I2Cdev.h"
// #include "MPU6050.h"
// #include "Wire.h"

KDSPort KDSThread(1, 0);
SoftwareSerial SoftSer(11, 10); // RX, TX

//MPU6050 accelgyro; //MPU6050 accelgyro(0x69); // <-- use for AD0 high
//int16_t ax, ay, az, gx, gy, gz, degrees_x, gforce; // MP6050

void setup()
{
   // MP6050
   //Wire.begin();
   //accelgyro.initialize();
   
   SoftSer.begin(19200);
}

void loop()
{
   //accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
   KDSThread.loop();

   //degrees_x = round(ax /180); 
   //gforce = gy;

   SoftSer.print(KDSThread.getRPM()); SoftSer.print(", ");
   SoftSer.print(KDSThread.getGear()); SoftSer.print("\n");
   // SoftSer.print(degrees_x); SoftSer.print(", ");
   // SoftSer.print(gforce); SoftSer.print("\n");
}

