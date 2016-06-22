//BMA180 triple axis accelerometer sample code//
//www.geeetech.com//
//
#include <Wire.h> 
#define BMA180 0x40  //address of the accelerometer
#define RESET 0x10   
#define PWR 0x0D
#define BW 0X20
#define RANGE 0X35
#define DATA 0x02
//
int offx = 31;  
int offy = 47;   
int offz = -23; 
// 
void setup() 
{ 
 Serial.begin(9600); 
 Wire.begin(); 
 Serial.println("Demo started, initializing sensors"); 
 AccelerometerInit(); 
 Serial.println("Sensors have been initialized"); 
} 
//
void AccelerometerInit() 
//
{ 
 byte temp[1];
 byte temp1;
  //
  writeTo(BMA180,RESET,0xB6);
  //wake up mode
  writeTo(BMA180,PWR,0x10);
  // low pass filter,
  readFrom(BMA180, BW,1,temp);
  temp1=temp[0]&0x0F;
  writeTo(BMA180, BW, temp1);   
  // range +/- 2g 
  readFrom(BMA180, RANGE, 1 ,temp);  
  temp1=(temp[0]&0xF1) | 0x04;
  writeTo(BMA180,RANGE,temp1);
}
//
void AccelerometerRead() 
{ 
 // read in the 3 axis data, each one is 14 bits 
 // print the data to terminal 
 int n=6;
 byte result[5];
 readFrom(BMA180, DATA, n , result);
 
 int x= (( result[0] | result[1]<<8)>>2)+offx ;
 float x1=x/4096.0;
 Serial.print("x=");
 Serial.print(x1);
 Serial.print("g"); 
 //
 int y= (( result[2] | result[3]<<8 )>>2)+offy;
 float y1=y/4096.0;
 Serial.print(",y=");
 Serial.print(y1);
 Serial.print("g"); 
 //
 int z= (( result[4] | result[5]<<8 )>>2)+offz;
 float z1=z/4096.0;
 Serial.print(",z=");
 Serial.print(z1);
 Serial.println("g"); 

   double xAngle = atan( x / (sqrt(square(y) + square(z))));
   double yAngle = atan( y / (sqrt(square(x) + square(z))));
   double zAngle = atan( sqrt(square(x) + square(y)) / z);

   xAngle *= 180.00;   yAngle *= 180.00;   zAngle *= 180.00;
   xAngle /= 3.141592; yAngle /= 3.141592; zAngle /= 3.141592;

  Serial.print(xAngle); Serial.print(", "); Serial.print(yAngle); Serial.print("\n");

}
//
void loop() 
{ 
 AccelerometerRead(); 
 delay(300); // slow down output   
}
//
//---------------- Functions--------------------
//Writes val to address register on ACC
void writeTo(int DEVICE, byte address, byte val) 
{
  Wire.beginTransmission(DEVICE);   //start transmission to ACC
  Wire.write(address);               //send register address
  Wire.write(val);                   //send value to write
  Wire.endTransmission();           //end trnsmisson
}
//reads num bytes starting from address register in to buff array
 void readFrom(int DEVICE, byte address , int num ,byte buff[])
 {
 Wire.beginTransmission(DEVICE); //start transmission to ACC
 Wire.write(address);            //send reguster address
 Wire.endTransmission();        //end transmission
 
 Wire.beginTransmission(DEVICE); //start transmission to ACC
 Wire.requestFrom(DEVICE,num);  //request 6 bits from ACC
 
 int i=0;
 while(Wire.available())        //ACC may abnormal
 {
 buff[i] =Wire.read();        //receive a byte
 i++;
 }
 Wire.endTransmission();         //end transmission
 }

