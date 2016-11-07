#include <SoftwareSerial.h>
 
SoftwareSerial mySerial(11, 10); // RX, TX
byte GPSBuffer[82];
byte GPSIndex=0;
unsigned int GPS_Satellites=0;
unsigned int GPS_Altitude=0;
 
void setup()
{
  Serial.begin(57600);
  mySerial.begin(19200);
}
 
void loop()
{
  CheckGPS();
}
 
void CheckGPS()
{
  int inByte;
  while (Serial.available() > 0)
  {
    inByte = Serial.read();
 
    // mySerial.write(inByte); // Output exactly what we read from the GPS to debug
 
    if ((inByte =='$') || (GPSIndex >= 80))
    {
      GPSIndex = 0;
    }
 
    if (inByte != '\r')
    {
      GPSBuffer[GPSIndex++] = inByte;
    }
 
    if (inByte == '\n')
    {
      ProcessGPSLine();
      GPSIndex = 0;
    }
  }
}

void ProcessGPSLine()
{
  if ((GPSBuffer[1] == 'G') && (GPSBuffer[2] == 'N') && (GPSBuffer[3] == 'G') && (GPSBuffer[4] == 'G') && (GPSBuffer[5] == 'A'))
  {
    ProcessGNGGACommand();
    mySerial.print("Altitude :");
    mySerial.print(GPS_Altitude);
    mySerial.print("   Satellites :");
    mySerial.println(GPS_Satellites);
  }
}

void ProcessGNGGACommand()
{
  int i, j, k, IntegerPart;
  unsigned int Altitude;
 
  // $GNGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
  //                                               =====  <-- altitude in field 8
 
  IntegerPart = 1;
  GPS_Satellites = 0;
  Altitude = 0;
 
  for (i=7, j=0, k=0; (i<GPSIndex) && (j<9); i++) // We start at 7 so we ignore the '$GNGGA,'
  {
    if (GPSBuffer[i] == ',')
    {
      j++;    // Segment index
      k=0;    // Index into target variable
      IntegerPart = 1;
    }
    else
    {
      if (j == 6)
      {
        // Satellite Count
        if ((GPSBuffer[i] >= '0') && (GPSBuffer[i] <= '9'))
        {
          GPS_Satellites = GPS_Satellites * 10;
          GPS_Satellites += (unsigned int)(GPSBuffer[i] - '0');
        }
      }
      else if (j == 8)
      {
        // Altitude
        if ((GPSBuffer[i] >= '0') && (GPSBuffer[i] <= '9') && IntegerPart)
        {
          Altitude = Altitude * 10;
          Altitude += (unsigned int)(GPSBuffer[i] - '0');
        }
        else
        {
          IntegerPart = 0;
        }
      }
    }
    GPS_Altitude = Altitude;
  }
}

