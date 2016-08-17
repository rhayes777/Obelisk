#define LEDPin 13 // Onboard LED
#include <avr/wdt.h>

int trigPins[] = {2,3,4,5};
int echoPins[] = {6,7,8,9};
int lightPins[] = {10, 11};
int lightModes[] = {0, 0};

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
 pinMode(lightPins[0], OUTPUT);
 pinMode(lightPins[1], OUTPUT);
}

void loop() {
  wdt_reset();
  for (int n; n < 2; n++) {
    int pin = lightPins[n];
    digitalWrite(pin,HIGH);
    delay(2000);
    digitalWrite(pin,LOW);           
    delay(2000);                                      
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
    
    if (input < value || value == -1) {
      value = input;
      
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

