#include <Arduino.h>

float distance_speed[2] = {0,0};
float speed = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(distance_speed[0]);
  Serial.print(",");
  Serial.println(distance_speed[1]);
  delay(1000);
  distance_speed[0]++;
  distance_speed[1]++;
  if(distance_speed[0]==5){
    distance_speed[0]=0;
  }
}
