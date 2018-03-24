#include <SoftwareSerial.h>

SoftwareSerial comm(2, 3);

void setup() {
  // put your setup code here, to run once:
  comm.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (comm.available() == 0) {
    return;
  }
  comm.print("Got: ");
  while (comm.available() > 0) {
    comm.print((char)comm.read());
    delay(10);
  }
}
