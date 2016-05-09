
#include "KDSPort.h"

// Constructor
KDSPort::KDSPort(uint8_t pinTX, uint8_t pinRX)
{
   this->_pinTX = pinTX;
   this->_pinRX = pinRX;
}


uint8_t KDSPort::sendRequest(const uint8_t *request, uint8_t *response, uint8_t reqLen, uint8_t maxLen)
{
  uint8_t buf[16], rbuf[16];
  uint8_t bytesToSend;
  uint8_t bytesSent = 0;
  uint8_t bytesToRcv = 0;
  uint8_t bytesRcvd = 0;
  uint8_t rCnt = 0;
  uint8_t c, z;
  bool forMe = false;
  char radioBuf[32];
  uint32_t startTime;
  
  for (uint8_t i = 0; i < 16; i++) {
    buf[i] = 0;
  }
  
  // Zero the response buffer up to maxLen
  for (uint8_t i = 0; i < maxLen; i++) {
    response[i] = 0;
  }

  // Form the request:
  if (reqLen == 1) {
    buf[0] = 0x81;
  } else {
    buf[0] = 0x80;
  }
  buf[1] = this->ECUaddr;
  buf[2] = this->myAddr;

  if (reqLen == 1) {
    buf[3] = request[0];
    buf[4] = this->calcChecksum(buf, 4);
    bytesToSend = 5;
  } else {
    buf[3] = reqLen;
    for (z = 0; z < reqLen; z++) {
      buf[4 + z] = request[z];
    }
    buf[4 + z] = this->calcChecksum(buf, 4 + z);
    bytesToSend = 5 + z;
  }
  
  // Now send the command...
  for (uint8_t i = 0; i < bytesToSend; i++) {
    bytesSent += Serial.write(buf[i]);
    delay(this->ISORequestByteDelay);
  }
  
  startTime = millis();
  
  // Wait for and deal with the reply
  while ((bytesRcvd <= maxLen) && ((millis() - startTime) < this->MAXSENDTIME)) {
    if (Serial.available()) {
      c = Serial.read();
      startTime = millis(); // reset the timer on each byte received

      rbuf[rCnt] = c;
      switch (rCnt) {
      case 0:
        // should be an addr packet either 0x80 or 0x81
        if (c == 0x81) {
          bytesToRcv = 1;
        } else if (c == 0x80) {
          bytesToRcv = 0;
        }
        rCnt++;
        break;
      case 1:
        // should be the target address
        if (c == this->myAddr) {
          forMe = true;
        }
        rCnt++;
        break;
      case 2:
        // should be the sender address
        if (c == this->ECUaddr) {
          forMe = true;
        } else if (c == this->myAddr) {
          forMe = false; // ignore the packet if it came from us!
        }
        rCnt++;
        break;
      case 3:
        // should be the number of bytes, or the response if its a single byte packet.
        if (bytesToRcv == 1) {
          bytesRcvd++;
          if (forMe) {
            response[0] = c; // single byte response so store it.
          }
        } else {
          bytesToRcv = c; // number of bytes of data in the packet.
        }
        rCnt++;
        break;
      default:
        if (bytesToRcv == bytesRcvd) {
          // must be at the checksum...
          if (forMe) {
            // Only check the checksum if it was for us - don't care otherwise!
            if (this->calcChecksum(rbuf, rCnt) == rbuf[rCnt]) {
              // Checksum OK.
              return(bytesRcvd);
            } else {
              // Checksum Error.
              return(0);
            }
          }
          // Reset the counters
          rCnt = 0;
          bytesRcvd = 0;
          
          // ISO 14230 specifies a delay between ECU responses.
        } else {
          // must be data, so put it in the response buffer
          // rCnt must be >= 4 to be here.
          if (forMe) {
            response[bytesRcvd] = c;
          }
          bytesRcvd++;
          rCnt++;
        }
        break;
      }
    }
  }

  return false;
}

uint8_t KDSPort::calcChecksum(uint8_t *data, uint8_t len) {
  uint8_t crc = 0;

  for (uint8_t i = 0; i < len; i++) {
    crc = crc + data[i];
  }
  return crc;
}


void KDSPort::setup()
{
   this->kph = 0;
   this->rpms = 0;

   pinMode(this->_pinTX, OUTPUT);
   pinMode(this->_pinRX, INPUT);
   
   uint8_t rLen;
   uint8_t req[2];
   uint8_t resp[3];

   Serial.end();

   // This is the ISO 14230-2 "Fast Init" sequence.
   digitalWrite(this->_pinTX, HIGH);
   delay(300);
   digitalWrite(this->_pinTX, LOW);
   delay(25);
   digitalWrite(this->_pinTX, HIGH);
   delay(25);

   Serial.begin(10400);

   // Start Communication is a single byte "0x81" packet.
   req[0] = 0x81;
   rLen = this->sendRequest(req, resp, 1, 3);

   delay(200);

   // Response should be 3 bytes: 0xC1 0xEA 0x8F
   if ((rLen == 3) && (resp[0] == 0xC1) && (resp[1] == 0xEA) && (resp[2] == 0x8F))
   {
      // Success, so send the Start Diag frame
      // 2 bytes: 0x10 0x80
      req[0] = 0x10;
      req[1] = 0x80;
      rLen = this->sendRequest(req, resp, 2, 3);
      delay(200);

      // OK Response should be 2 bytes: 0x50 0x80
      if ((rLen == 2) && (resp[0] == 0x50) && (resp[1] == 0x80)) {
         this->ECUconnected = true;
         return;
      }
   }
   
   // Otherwise, we failed to init.
   this->ECUconnected = false;
   return;
}


void KDSPort::loop()
{
   uint8_t cmdSize;
   uint8_t cmdBuf[6];
   uint8_t respSize;
   uint8_t respBuf[12];
   uint8_t ect;

   if (!this->ECUconnected)
   {
      // Start KDS comms
      delay(2000);
      this->setup();
   }
   else
   {
      // Send register requests
      cmdSize = 2; // each request is a 2 byte packet.
      cmdBuf[0] = 0x21; // Register request cmd
      // Response to a register request is either:
      // 0x61 - Register read OK
      // 0x?? - Register requested
      // 0x?? - Value byte 1
      // ...  - (if more than 1 byte value - remainder of values)
      // ___ or:
      // 0x7F - Error response
      // 0x21 - command (0x21 = Read register)
      // 0x?? - error code (0x10 = General Reject: The service is rejected
      //      but the server does not specify the reason of the rejection

      // Grab RPMs
      for (uint8_t i = 0; i < 5; i++) respBuf[i] = 0;

      // Request RPM is register: 0x09
      cmdBuf[1] = 0x09;
      respSize = sendRequest(cmdBuf, respBuf, cmdSize, 12);
      if (respSize == 4) {
         // Formula for RPMs from response
         this->rpms = respBuf[2] * 100 + respBuf[3];
      }
      else if (respSize == 0)
      {
         this->ECUconnected = false;
         return;
      }

      delay(this->ISORequestDelay);

      // Speed
      for (uint8_t i = 0; i < 5; i++) respBuf[i] = 0;

      // Request Speed is register: 0x0C
      cmdBuf[1] = 0x0C;
      respSize = sendRequest(cmdBuf, respBuf, cmdSize, 12);
      if (respSize == 4) {
         // NOTE: Actual MPH is this value halved, but we want to
         // keep full available resolution
         this->kph = ((respBuf[2] << 8) + respBuf[3]) / 2;
      }
      else if (respSize == 0)
      {
         this->ECUconnected = false;
         return;
      }

      delay(this->ISORequestDelay);

      /*
      // Throttle
      for (uint8_t i = 0; i < 5; i++) respBuf[i] = 0;

      // Request Throttle is register: 0x04
      cmdBuf[1] = 0x04;
      respSize = sendRequest(cmdBuf, respBuf, cmdSize, 12);
      if (respSize == 4) {
         // NOTE: Actual MPH is this value halved, but we want to
         // keep full available resolution
         this->this->kph = (respBuf[2] << 8) + respBuf[3];

         // PRINT on usb serial
         SoftSer..print("MPH: ");
         SoftSer..print(this->this->kph);
      }
      else if (respSize == 0)
      {
         this->ECUconnected = false;
         break;
      }

      */
   }
}


uint32_t KDSPort::getRPM()
{
   return this->rpms;
}


uint32_t KDSPort::getKPH()
{
   return this->kph;
}

