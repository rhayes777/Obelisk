#define LEDPin 13 // Onboard LED
#include <avr/wdt.h>

int trigPins[] = {2,3,4,5};
int echoPins[] = {6,7,8,9};
int lightModes[] = {0, 0};
boolean isOn = true;
int count = 0;
int switchLimit = 2000;

int numberOfSensors;

void setup() {
    Serial.begin(9600);
    wdt_enable(WDTO_1S);
 
    numberOfSensors = sizeof(trigPins)/sizeof(int);

 for (int n; n < numberOfSensors; n++) {
    pinMode(trigPins[n], OUTPUT);
    pinMode(echoPins[n], INPUT);
 }
 pinMode(LEDPin, OUTPUT); // Use LED indicator (if required)
 
}

void loop() {
  wdt_reset();
  count++;
  if (isOn) {
    digitalWrite(LEDPin, HIGH);
    delayMicroseconds(lightModes[0]);
    digitalWrite(LEDPin, LOW);
  }
  if (count == switchLimit) {
    isOn = !isOn;
    count = 0;
  }
}

void serialEvent() {
  int n = 0;
  while (Serial.available()) {
      int msg = Serial.read();
      if (msg >= 48) {
        lightModes[n++] = msg - 48;
      }
      else {
        Serial.println(recordDataString());
      }
  }
}

String recordDataString() {
  String result = "[";
  int value = -1;
  int pairNumber = 0;
  for (int n; n < numberOfSensors; n++) {
    int trigPin = trigPins[n];
    int echoPin = echoPins[n];
    digitalWrite(trigPin, LOW); 
    delayMicroseconds(2); 

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10); 
    
    digitalWrite(trigPin, LOW);
    int input = pulseIn(echoPin, HIGH);
    Serial.println("input = " + String(input));
    if (input < value || value == -1) {
      value = input;
      Serial.println("value set " + String(value));
    }
    if (pairNumber == 1) {
      result += String(value) + (n < numberOfSensors - 1 ? "," : "]");
      value = -1;
      pairNumber = 0;
    } else {
      pairNumber = 1;
    }
  }
  return result;
}

