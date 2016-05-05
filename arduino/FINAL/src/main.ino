#include <SoftwareSerial.h>
#include <KDSPort.h>

KDSPort KDSThread(1, 0);
SoftwareSerial SoftSer(11,10); // RX, TX
uint32_t rpms = 0;
uint32_t kph = 0;

void setup()
{
   SoftSer.begin(19200);
}

void loop()
{
   KDSThread.loop();
   SoftSer.print(rpms); SoftSer.print(", ");
   SoftSer.print(kph); SoftSer.print("\n");
}

