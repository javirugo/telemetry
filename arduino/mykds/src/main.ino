#include <SoftwareSerial.h>

#define PIN_TX 1
#define PIN_RX 0

#define KDS_BAUDRATE 10400
#define USBSERIAL_BAUDRATE 19200

char KDS_start_kds[]={0x81, 0x11, 0xF1, 0x81, 0x04};
//ECU replies with ok: 80 F1 11 03 C1 EA 8F BF

char KDS_start_diagnostic_mode[]={0x80, 0x11, 0xF1, 0x02, 0x10, 0x80, 0x14};
//ECU replies with OK: 80 F1 11 02 50 80 54

char KDS_ask_gear[]={0x80, 0x11, 0xF1, 0x02, 0x21, 0x0B, 0xB0};
char KDS_ask_temp[]={0x80, 0x11, 0xF1, 0x02, 0x21, 0x06, 0xAB};
char KDS_ask_speed[]={0x80, 0x11, 0xF1, 0x02, 0x21, 0x0C, 0xAB};


// Hardware serials seems to be the USB serial in arduino nano, so software serial
// for the TX/RX pins is needed (as nano's libs have no Serial1...)
SoftwareSerial SoftSer(11, 10);

void kds_start_sesion()
{
   uint8_t i;
   uint8_t c;
   Serial.end();
   delay(200);

   SoftSer.println("starting init...");

   digitalWrite(PIN_TX, HIGH);
   delay(300);
   digitalWrite(PIN_TX, LOW);
   delay(25);
   digitalWrite(PIN_TX, HIGH);
   delay(25);

   Serial.begin(KDS_BAUDRATE);

   for (i = 0; i < sizeof(KDS_start_kds); i++)
      Serial.write(KDS_start_kds[i]);

   delay(50);

   SoftSer.print("First: ");
   while (Serial.available())
   {
      c = Serial.read();
      SoftSer.print(c);
      SoftSer.print(" ");
   }

   for (i = 0; i < sizeof(KDS_start_diagnostic_mode); i++)
      Serial.write(KDS_start_diagnostic_mode[i]);

   delay(200);
   SoftSer.print("Second: ");
   if (Serial.available() > 0)
   {
      c = Serial.read();
      SoftSer.print(c);
      SoftSer.print(" ");
   }

   SoftSer.println(" ");
}

void setup()
{
   SoftSer.begin(USBSERIAL_BAUDRATE);
   pinMode(PIN_TX, OUTPUT);
   pinMode(PIN_RX, INPUT);}

void loop()
{
   kds_start_sesion();
   delay(2000);
}

