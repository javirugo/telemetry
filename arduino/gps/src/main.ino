// Use this code with UBLOX NEO M8N
#include "Ublox.h"
#define SERIAL_BAUD 115200
#define GPS_BAUD 115200
#define N_GPS_DATA 4

Ublox M8_Gps;
// Altitude - Latitude - Longitude - N Satellites
float gpsArray[N_GPS_DATA] = {0, 0, 0, 0};

void setup() {
   Serial.begin(SERIAL_BAUD);
   Serial1.begin(GPS_BAUD);

}

void loop() {
   if(!Serial1.available())
		return;

  while(Serial1.available()){
        char c = Serial1.read();
        M8_Gps.encode(c);          
        gpsArray[0] = M8_Gps.altitude;
        gpsArray[1] = M8_Gps.latitude;
        gpsArray[2] = M8_Gps.longitude;
        gpsArray[3] = M8_Gps.sats_in_use;
	}
}

