#include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial KDSSerial(14, 15); // RX, TX for BT

#define BDR_pc 19200
#define BDR_zx6r 10400

//int MYUBRR=0;
int zx6r_rec_char=0;
char buf[3];
char temp=0;


char start_kds[]={0x81, 0x11, 0xF1, 0x81, 0x04};
//ECU replies with ok: 80 F1 11 03 C1 EA 8F BF

char start_diagnostic_mode[]={0x80, 0x11, 0xF1, 0x02, 0x10, 0x80, 0x14};
//ECU replies with OK: 80 F1 11 02 50 80 54

char ask_gear[]={0x80, 0x11, 0xF1, 0x02, 0x21, 0x0B, 0xB0};
char ask_temp[]={0x80, 0x11, 0xF1, 0x02, 0x21, 0x06, 0xAB};
char ask_speed[]={0x80, 0x11, 0xF1, 0x02, 0x21, 0x0C, 0xAB};


void serial_write_c(char c)
{
   while (!( UCSR0A&(1<<UDRE0)));
    UDR0 = c;
}
                

void kds_start_sesion()
{
   KDSSerial.end();

   pinMode(1, OUTPUT);
   digitalWrite(1, HIGH);
   delay(750); //in ms
   digitalWrite(1, LOW);
   delay(25);  //in ms
   digitalWrite(1, HIGH);
   delay(25);  //in ms

   KDSSerial.begin(BDR_zx6r);
   Serial.println("Init A");
   serial_write_c(0x81);
   serial_write_c(0x11);
   serial_write_c(0xF1);
   serial_write_c(0x81);
   serial_write_c(0x04);
   Serial.println(KDSSerial.available());
   delay(200);

   Serial.println("Init B");
   serial_write_c(0x80);
   serial_write_c(0x11);
   serial_write_c(0xF1);
   serial_write_c(0x02);
   serial_write_c(0x10);
   serial_write_c(0x80);
   serial_write_c(0x14);
   Serial.println(KDSSerial.available());
   delay(200);
}


void getTemp()
{
   //0x80, 0x11, 0xF1, 0x02, 0x21, 0x06, 0xAB
   Serial.println("temp= ");
   serial_write_c(0x80);
   serial_write_c(0x11);
   serial_write_c(0xF1);
   serial_write_c(0x02);
   serial_write_c(0x21);
   serial_write_c(0x06);
   serial_write_c(0xAB);
   delay(200);
}



void setup()
{
   Serial.begin(BDR_pc);
}

void loop()
{

   kds_start_sesion();
   delay(5000);
   


   /*
 if (KDSSerial.available() > 0)
    {
    zx6r_rec_char = KDSSerial.read();
    itoa(zx6r_rec_char, buf, HEX);
    Serial.print(" 0x");
    Serial.print(buf);
    }


// TODO determine if we need to init
if(pc_char==49) // 1 start initialisation
    {
    kds_start_sesion();
    Serial.println("_1");
    }

if(pc_char==50)//2 request gear no.
    {
    //0x80, 0x11, 0xF1, 0x02, 0x21, 0x0B, 0xB0
    Serial.println("gear= ");
    serial_write_c(0x80);
    serial_write_c(0x11);
    serial_write_c(0xF1);
    serial_write_c(0x02);
    serial_write_c(0x21);
    serial_write_c(0x0B);
    serial_write_c(0xB0);
    delay(200);
    }

if(pc_char==51)//3 request temp
    {
    //0x80, 0x11, 0xF1, 0x02, 0x21, 0x06, 0xAB
    Serial.println("temp= ");
    serial_write_c(0x80);
    serial_write_c(0x11);
    serial_write_c(0xF1);
    serial_write_c(0x02);
    serial_write_c(0x21);
    serial_write_c(0x06);
    serial_write_c(0xAB);
    delay(200);
    }

if(pc_char==52)//4 request SPEED
    {
    int i=0;
    //speed 0x80, 0x11, 0xF1, 0x02, 0x21, 0x0C, 0xAB
        Serial.println(" ");
        Serial.println("speed-");
        serial_write_c(0x80);
        serial_write_c(0x11);
        serial_write_c(0xF1);
        serial_write_c(0x02);
        serial_write_c(0x21);
        serial_write_c(0x0C);
        serial_write_c(0xB1);
        Serial.println(" ");
        //delay(200);
    }
*/
}
