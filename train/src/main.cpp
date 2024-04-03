#include <Arduino.h>

float distance = 0;
float speed = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("|");
  delay(1000);
}