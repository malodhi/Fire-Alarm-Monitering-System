#include "SdsDustSensor.h"

int rxPin = 19;
int txPin = 18;
String smokeVal;
SdsDustSensor sds(Serial1);
const float smoke_threshold = 30;

void setup() {
  Serial.begin(9600);
  sds.begin();
}

void loop() {
  PmResult pm = sds.readPm();
  if (pm.isOk()){
    smokeVal = String(pm.pm25);
    Serial.println(smokeVal);
    if (pm.pm25 < smoke_threshold){
      // ring the buzzer using multi-threading}
    }
  }
  delay(200);
}
