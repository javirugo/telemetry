
#include "Ublox.h"


#define SERIAL_BAUD 115200
#define M8N_BAUD 115200
#define N_FLOATS 4

Ublox M8_Gps;
float gpsArray[N_FLOATS] = {0, 0, 0, 0};


void setup()
{
   Serial.begin(SERIAL_BAUD);
   Serial1.begin(M8N_BAUD);
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
   }

   for(byte i = 0; i < N_FLOATS; i++)
   {
      Serial.print(gpsArray[i], 6);Serial.print(" ");
   }

   Serial.println("");
}

