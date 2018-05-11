#include <MPU9250_asukiaaa.h>

MPU9250 sensor;
float mX, mY, mZ;
float mDirection;

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  sensor.setWire(&Wire);
  sensor.beginMag();
  sensor.magXOffset = 0;
  sensor.magYOffset = 0;
  sensor.magZOffset = 0;
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) ;
  char m = Serial.read();
  if (m == 'F') {
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
  }
  else if (m == 'C') {
    setMagMinMaxAndSetOffset(&sensor, 10);
    Serial.println("Calibrated");
  }
  
  delay(1);
}

void setMagMinMaxAndSetOffset(MPU9250* sensor, int seconds) {
  unsigned long calibStartAt = millis();
  float magX, magXMin, magXMax, magY, magYMin, magYMax, magZ, magZMin, magZMax;

  sensor->magXOffset = 0;
  sensor->magYOffset = 0;
  sensor->magZOffset = 0;

  sensor->magUpdate();
  magXMin = magXMax = sensor->magX();
  magYMin = magYMax = sensor->magY();
  magZMin = magZMax = sensor->magZ();

  while(millis() - calibStartAt < (unsigned long) seconds * 1000) {
    delay(100);
    sensor->magUpdate();
    magX = sensor->magX();
    magY = sensor->magY();
    magZ = sensor->magZ();
    if (magX > magXMax) magXMax = magX;
    if (magY > magYMax) magYMax = magY;
    if (magZ > magZMax) magZMax = magZ;
    if (magX < magXMin) magXMin = magX;
    if (magY < magYMin) magYMin = magY;
    if (magZ < magZMin) magZMin = magZ;
  }

  sensor->magXOffset = - (magXMax - magXMin) / 2;
  sensor->magYOffset = - (magYMax - magYMin) / 2;
  sensor->magZOffset = - (magZMax - magZMin) / 2;
}
