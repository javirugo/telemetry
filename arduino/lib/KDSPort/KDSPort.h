#ifndef KDSPORT_h
#define KDSPORT_h

#include <stdint.h>
#include <Arduino.h>
#include <SoftwareSerial.h>

class KDSPort
{
   private:
      uint8_t _pinTX;
      uint8_t _pinRX;
      const uint32_t ISORequestDelay = 120; // Time between requests.

      const uint8_t ECUaddr = 0x11;
      const uint8_t myAddr = 0xF2;
      const uint16_t MAXSENDTIME = 2000;

      bool ECUconnected = false;
      uint16_t rpms = 0;
      uint16_t kph = 0;
      uint8_t kphCounter = 0;
      uint8_t gear = 0;
      uint8_t gearCounter = 0;

      uint8_t sendRequest(const uint8_t *request, uint8_t *response, uint8_t reqLen, uint8_t maxLen);
      uint8_t calcChecksum(uint8_t *data, uint8_t len);

   public:
      KDSPort(uint8_t pinTX, uint8_t pinRX);
      void setup();
      void loop();

      uint16_t getRPM();
      uint16_t getKPH();
      uint8_t getGear();
};

#endif KDSPORT_h

