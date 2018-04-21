#include <MPU9250_asukiaaa.h>

MPU9250 sensor;
float mX, mY, mZ;
float mDirection;

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  sensor.setWire(&Wire);
  sensor.beginMag();
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) ;
  Serial.read();
  sensor.magUpdate();
  mX = sensor.magX();
  mY = sensor.magY();
  mZ = sensor.magZ();
  mDirection = sensor.magHorizDirection();
  Serial.print(mX);
  Serial.print(", ");
  Serial.print(mY);
  Serial.print(", ");
  Serial.print(mZ);
  Serial.print(", ");
  Serial.println(mDirection);
  delay(50);
}
