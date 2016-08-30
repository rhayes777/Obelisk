#define LEDPin 13 // Onboard LED
#define LIGHT_MODE_OFF 0
#define LIGHT_MODE_ON 1
#include <avr/wdt.h>

int trigPins[] = {2,3,4,5};
int echoPins[] = {6,7,8,9};
int lightPins[] = {10, 11};
int lightModes[] = {0, 0};
boolean isLightOnArray[] = {false, false};

int lightPattern0[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int lightPattern1[] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
int lightPattern2[] = {0, 1, 1, 1, 1, 1, 1, 1, 1, 1};
int lightPattern3[] = {0, 1, 1, 1, 1, 0, 1, 1, 1, 1};
int lightPattern4[] = {1, 0, 1, 0, 1, 0, 1, 1, 1, 1};
int lightPattern5[] = {1, 1, 1, 0, 1, 1, 0, 1, 0, 0};
int lightPattern6[] = {1, 0, 1, 1, 0, 1, 1, 1, 0, 0};
int lightPattern7[] = {1, 1, 1, 1, 1, 0, 0, 0, 0, 0};
int lightPattern8[] = {1, 1, 0, 1, 1, 0, 1, 1, 0, 0};
int lightPattern9[] = {1, 0, 1, 0, 1, 0, 1, 0, 1, 0};

int* lightPatterns[10];

int numberOfSensors;
int lightPatternLength;
int count;

void setup() {
 Serial.begin(9600);
 wdt_enable(WDTO_1S);
 
 numberOfSensors = sizeof(trigPins)/sizeof(int);
 lightPatternLength = sizeof(*lightPatterns[0])/sizeof(int);
 count = 0;

 lightPatterns[0] = lightPattern0;
 lightPatterns[1] = lightPattern1;
 lightPatterns[2] = lightPattern2;
 lightPatterns[3] = lightPattern3;
 lightPatterns[4] = lightPattern4;
 lightPatterns[5] = lightPattern5;
 lightPatterns[6] = lightPattern6;
 lightPatterns[7] = lightPattern7;
 lightPatterns[8] = lightPattern8;
 lightPatterns[9] = lightPattern9;
 
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

  count++;
  if (count > lightPatternLength - 1) {
    count = 0;
  }
  
  for (int n; n < 2; n++) {
   
    int pin = lightPins[n];
    int lightMode = lightModes[n];
    int* lightPattern = lightPatterns[lightMode];

    if (*(lightPattern + count) == 1) {
      digitalWrite(pin, LOW);
    }
    else {
      digitalWrite(pin, HIGH);
    }
                                      
  }
  wdt_reset();
  delay(50);
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

