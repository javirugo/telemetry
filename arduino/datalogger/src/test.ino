
#include "Ublox.h"
#include <Wire.h>


#define SERIAL_BAUD 115200
#define M8N_BAUD 115200
#define N_FLOATS 4

#define BMA180 0x40  //address of the accelerometer
#define BMA180_RESET 0x10   
#define BMA180_PWR 0x0D
#define BMA180_BW 0X20
#define BMA180_RANGE 0X35
#define BMA180_DATA 0x02

Ublox M8_Gps;

// Adjustments for accelerometer
int BMA180_offx = 31;
int BMA180_offy = 47; 
int BMA180_offz = -23;


// Data variables
float gpsArray[N_FLOATS] = {0, 0, 0, 0};
float gforce_x = 0;
float gforce_y = 0;
float gforce_z = 0;
double xAngle = 0;
double yAngle = 0;
double zAngle = 0;


void AccelerometerInit()
{
   byte temp[1];
   byte temp1;
   writeTo(BMA180, BMA180_RESET, 0xB6);

   //wake up mode
   writeTo(BMA180, BMA180_PWR, 0x10);

   // low pass filter,
   readFrom(BMA180, BMA180_BW, 1, temp);
   temp1 = temp[0]&0x0F;
   writeTo(BMA180, BMA180_BW, temp1);

   // range +/- 2g
   readFrom(BMA180, BMA180_RANGE, 1, temp);
   temp1=(temp[0]&0xF1) | 0x04;
   writeTo(BMA180, BMA180_RANGE, temp1);
}


void AccelerometerRead()
{
   // read in the 3 axis data, each one is 14 bits 
   int n = 6;
   byte result[5];
   readFrom(BMA180, BMA180_DATA, n, result);

   int x = (( result[0] | result[1]<<8 )>>2) + BMA180_offx;
   int y = (( result[2] | result[3]<<8 )>>2) + BMA180_offy;
   int z = (( result[4] | result[5]<<8 )>>2) + BMA180_offz;

   gforce_x = x/4096.0;
   gforce_y = y/4096.0;
   gforce_z = z/4096.0;

   double xAngle = atan( x / (sqrt(square(y) + square(z))));
   double yAngle = atan( y / (sqrt(square(x) + square(z))));
   double zAngle = atan( sqrt(square(x) + square(y)) / z);

   xAngle *= 180.00;   yAngle *= 180.00;   zAngle *= 180.00;
   xAngle /= 3.141592; yAngle /= 3.141592; zAngle /= 3.141592;
}


// Writes val to address register on ACC
void writeTo(int DEVICE, byte address, byte val) 
{
   Wire.beginTransmission(DEVICE); // start transmission to ACC
   Wire.write(address);            // send register address
   Wire.write(val);                // send value to write
   Wire.endTransmission();         // end trnsmisson
}

// Reads num bytes starting from address register in to buff array
void readFrom(int DEVICE, byte address , int num ,byte buff[])
{
   Wire.beginTransmission(DEVICE); // start transmission to ACC
   Wire.write(address);            // send reguster address
   Wire.endTransmission();         // end transmission

   Wire.beginTransmission(DEVICE); // start transmission to ACC
   Wire.requestFrom(DEVICE,num);   // request 6 bits from ACC

   int i = 0;
   while(Wire.available())         // ACC may abnormal
   {
      buff[i] = Wire.read();       // receive a byte
      i++;
   }

   Wire.endTransmission();         // end transmission
}


void setup()
{
   Serial.begin(SERIAL_BAUD);

   Serial1.begin(M8N_BAUD);

   Wire.begin(); 
   AccelerometerInit(); 

}


void loop()
{
   if (!Serial1.available()) return;
   while(Serial1.available())
   {
      char c = Serial1.read();
      if (M8_Gps.encode(c))
      {
         gpsArray[0] = M8_Gps.altitude;
         gpsArray[1] = M8_Gps.latitude;
         gpsArray[2] = M8_Gps.longitude; 
         gpsArray[3] = M8_Gps.speed;
      }

      AccelerometerRead(); 
   }


   for(byte i = 0; i < N_FLOATS; i++)
   {
      Serial.print(gpsArray[i], 6); Serial.print(", ");
   }

   Serial.print(gforce_x); Serial.print(", ");
   Serial.print(gforce_y); Serial.print(", ");
   Serial.print(gforce_z); Serial.print(", ");

   Serial.print(xAngle); Serial.print(", ");
   Serial.print(yAngle); Serial.print(", ");
   Serial.print(zAngle);
   Serial.println("");
}

