#include <SPI.h>
void setup (void)
{
  SPI.begin();
  pinMode(MISO, OUTPUT);
 
  // turn on SPI in slave mode
  SPCR |= _BV(SPE);
}

void loop  (void) {
  SPI.transfer('TEST');
}

