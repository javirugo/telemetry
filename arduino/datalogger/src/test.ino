// Debug mode?
#define _DEBUG true

// SD
#include <SPI.h>
#include <SD.h>
const int chipSelect = 10;
File dataFile;
String logfile;

// KDS
#include <KDSPort.h>
unsigned long kds_millis;
KDSPort KDSThread(16, 17);

// GPS
#include "Ublox.h"
#define SERIAL_BAUD 115200
#define M8N_BAUD 57600
Ublox M8_Gps;

// BMA180 (Accel)
#include <Wire.h>
#define BMA180 0x40  //address of the accelerometer
#define BMA180_RESET 0x10   
#define BMA180_PWR 0x0D
#define BMA180_BW 0X20
#define BMA180_RANGE 0X35
#define BMA180_DATA 0x02
int BMA180_offx = 31;
int BMA180_offy = 47; 
int BMA180_offz = -23;

// ITG3205 (Gyros)
#define GYRO 0x68
#define G_SMPLRT_DIV 0x15
#define G_DLPF_FS 0x16
#define G_INT_CFG 0x17
#define G_PWR_MGM 0x3E
#define G_TO_READ 8 // 2 bytes for each axis x, y, z
int g_offx = 120;
int g_offy = 20;
int g_offz = 93;

// BMP065 (barometer)
#include <BMP085.h>
BMP085 bmp085 = BMP085();

// HMC5883 (compass)
#include <HMC58X3.h>
HMC58X3 magnetometer;

// Data variables
unsigned long start_millis;
float altitude = 0;
long altitude_bmp = 0;
float latitude = 0;
float longitude = 0;
float speed = 0;
float gforce_x = 0;
float gforce_y = 0;
float gforce_z = 0;
float xAngle = 0;
float yAngle = 0;
float zAngle = 0;
int hx = 0;
int hy = 0;
int hz = 0;
int temperature = 0;
long temp_bmp = 0;
long pressure = 0;
float heading = 0;

void initGyro()
{
   /*****************************************
   * ITG 3200
   * power management set to:
   * clock select = internal oscillator
   * no reset, no sleep mode
   * no standby mode
   * sample rate to = 125Hz
   * parameter to +/- 2000 degrees/sec
   * low pass filter = 5Hz
   * no interrupt
   ******************************************/
   writeTo(GYRO, G_PWR_MGM, 0x00);
   writeTo(GYRO, G_SMPLRT_DIV, 0x07); // EB, 50, 80, 7F, DE, 23, 20, FF
   writeTo(GYRO, G_DLPF_FS, 0x1E); // +/- 2000 dgrs/sec, 1KHz, 1E, 19
   writeTo(GYRO, G_INT_CFG, 0x00);
}

void GyroscopeRead()
{
   /**************************************
   Gyro ITG-3200 I2C
   registers:
   temp MSB = 1B, temp LSB = 1C
   x axis MSB = 1D, x axis LSB = 1E
   y axis MSB = 1F, y axis LSB = 20
   z axis MSB = 21, z axis LSB = 22
   *************************************/
   int regAddress = 0x1B;
   int temp, x, y, z;
   byte buff[G_TO_READ];
   readFrom(GYRO, regAddress, G_TO_READ, buff); //read the gyro data from the ITG3200
   hx = (((buff[2] << 8) | buff[3]) + g_offx) / 14.375;
   hy = (((buff[4] << 8) | buff[5]) + g_offy) / 14.375;
   hz = (((buff[6] << 8) | buff[7]) + g_offz) / 14.375;
   temperature = 35+ ((double) (((buff[0] << 8) | buff[1]) + 13200)) / 280; // temperature
}


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

   xAngle = atan( x / (sqrt(square(y) + square(z))));
   yAngle = atan( y / (sqrt(square(x) + square(z))));
   zAngle = atan( sqrt(square(x) + square(y)) / z);

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

void HMC5883Init()
{
   // no delay needed as we have already a delay(5) in HMC5843::init()
   magnetometer.init(false); // Dont set mode yet, we'll do that later on.
   // Calibrate HMC using self test, not recommended to change the gain after calibration.
   magnetometer.calibrate(1, 32); // Use gain 1=default, valid 0-7, 7 not recommended.
   // Single mode conversion was used in calibration, now set continuous mode
   magnetometer.setMode(0);
}

void HMC5883Read()
{
  int ix,iy,iz;
  float fx,fy,fz;
  magnetometer.getValues(&ix,&iy,&iz);
  magnetometer.getValues(&fx,&fy,&fz);

  heading = atan2(fy, fx);
  if(heading < 0) {
    heading += 2 * M_PI;
  }
  
  heading = heading * 180/M_PI;
}

void BMP085Init()
{
   bmp085.init();
}

void BMP085Read()
{
   bmp085.getPressure(&pressure);
   bmp085.getAltitude(&altitude_bmp);
   bmp085.getTemperature(&temp_bmp);
}


void GPSRead()
{
   if (!Serial1.available()) return;
   while (Serial1.available())
   {
      char c = Serial1.read();
      if (M8_Gps.encode(c))
      {
         altitude = M8_Gps.altitude;
         latitude = M8_Gps.latitude;
         longitude = M8_Gps.longitude; 
         speed = M8_Gps.speed;
      }
   }
}

void SDInit()
{
   pinMode(SS, OUTPUT);
   SD.begin(chipSelect);
   char filename[10] = "data0.log";
   for (int i = 0; i < 200; i++)
   {
      logfile = String("data") + String(i) + String(".log");
      char filename[50];
      logfile.toCharArray(filename, 50);
      if (!SD.exists(filename))
      {
         dataFile = SD.open(filename, FILE_WRITE);
         dataFile.print("elapsed time, altitude, latitude, longitude, heading, speed, ");
         dataFile.print("gforce_x, gforce_y, gforce_z, angle_x, angle_y, angle_z, ");
         dataFile.print("gyros_x, gyros_y, gyros_z, temp, temp_bmp085, pressure, ");
         dataFile.println("rpm, gear");
         dataFile.close();
         break;
      }
   }
}


void SDWrite()
{
   char filename[50];
   logfile.toCharArray(filename, 50);
   dataFile = SD.open(filename, FILE_WRITE);

   unsigned long elapsed_millis = (millis() - start_millis);
   dataFile.print((elapsed_millis / 1000)); dataFile.print(".");
   dataFile.print((elapsed_millis % 1000)); dataFile.print(", ");
   dataFile.print(altitude); dataFile.print(", ");
   dataFile.print(latitude, 6); dataFile.print(", ");
   dataFile.print(longitude, 6); dataFile.print(", ");
   dataFile.print(heading); dataFile.print(", ");
   dataFile.print(speed); dataFile.print(", ");
   dataFile.print(gforce_x); dataFile.print(", ");
   dataFile.print(gforce_y); dataFile.print(", ");
   dataFile.print(gforce_z); dataFile.print(", ");
   dataFile.print(xAngle); dataFile.print(", ");
   dataFile.print(yAngle); dataFile.print(", ");
   dataFile.print(zAngle); dataFile.print(", ");
   dataFile.print(hx); dataFile.print(", ");
   dataFile.print(hy); dataFile.print(", ");
   dataFile.print(hz); dataFile.print(", ");
   dataFile.print(temperature); dataFile.print(", ");
   dataFile.print(temp_bmp); dataFile.print(", ");
   dataFile.print(pressure); dataFile.print(", ");
   dataFile.print(KDSThread.getRPM()); dataFile.print(", ");
   dataFile.print(KDSThread.getGear());
   dataFile.println("");
   dataFile.close();
}


void setup()
{
   if (_DEBUG) Serial.begin(SERIAL_BAUD);
   else SDInit();

   Serial1.begin(M8N_BAUD);
   Wire.begin();

   AccelerometerInit();
   BMP085Init();
   initGyro();
   HMC5883Init();
   start_millis = millis();
   kds_millis = start_millis;
}


void loop()
{
   GPSRead();
   AccelerometerRead();
   GyroscopeRead();
   BMP085Read();
   HMC5883Read();
   if (KDSThread.loop(kds_millis)) kds_millis = millis();
   
   if (!_DEBUG)
   {
      SDWrite();
   }
   else
   {
      #unsigned long elapsed_millis = (millis() - start_millis);
      #Serial.print((elapsed_millis / 1000)); Serial.print(".");
      #Serial.print((elapsed_millis % 1000)); Serial.print(", ");
      Serial.print(altitude, 6); Serial.print(", ");
      Serial.print(latitude, 6); Serial.print(", ");
      Serial.print(longitude, 6); Serial.print(", ");
      Serial.print(heading); Serial.print(", ");
      Serial.print(speed, 0); Serial.print(", ");
      Serial.print(gforce_x); Serial.print(", ");
      Serial.print(gforce_y); Serial.print(", ");
      Serial.print(gforce_z); Serial.print(", ");
      Serial.print(xAngle); Serial.print(", ");
      Serial.print(yAngle); Serial.print(", ");
      Serial.print(zAngle); Serial.print(", ");
      Serial.print(hx); Serial.print(", ");
      Serial.print(hy); Serial.print(", ");
      Serial.print(hz); Serial.print(", ");
      Serial.print(temperature); Serial.print(", ");
      Serial.print(temp_bmp); Serial.print(", ");
      Serial.print(pressure); Serial.print(", ");
      Serial.print(KDSThread.getRPM()); Serial.print(", ");
      Serial.print(KDSThread.getGear());
      Serial.println("");
   }

   delay(10);
}

