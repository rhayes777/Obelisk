#define LEDPin 13 // Onboard LED

int trigPins[] = {2,3,4,5};
int echoPins[] = {6,7,8,9};

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int numberOfSensors;

long duration, distance; // Duration used to calculate distance

void setup() {
    Serial.begin(9600);
    inputString.reserve(200);
    numberOfSensors = sizeof(trigPins)/sizeof(int);

 for (int n; n < numberOfSensors; n++) {
    pinMode(trigPins[n], OUTPUT);
    pinMode(echoPins[n], INPUT);
 }
 pinMode(LEDPin, OUTPUT); // Use LED indicator (if required)
}

void loop() {

  if (stringComplete) {
//    Serial.println(recordDataString()); 
    while (true) {
       Serial.println(inputString); 
    }
    stringComplete = false;
  }

}


void serialEvent() {
  while (Serial.available()) {
    Serial.read();
  }
       
  Serial.println(recordDataString());
    
//  while (Serial.available()) {
//    // get the new byte:
//    char inChar = (char)Serial.read();
//    // add it to the inputString:
//    inputString += inChar;
//    // if the incoming character is a newline, set a flag
//    // so the main loop can do something about it:
//    if (inChar == '\n') {
//      stringComplete = true;
//    }
//  }
}

String recordDataString() {
  String result = "[";
  int sum = -1;
  for (int n; n < numberOfSensors; n++) {
    int trigPin = trigPins[n];
    int echoPin = echoPins[n];
    digitalWrite(trigPin, LOW); 
    delayMicroseconds(2); 

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10); 
    
    digitalWrite(trigPin, LOW);
    int input = pulseIn(echoPin, HIGH);
    if (sum == -1) {
      sum = input;
    }
    else {
      sum += input;
      int avg = sum / 2;
      sum = -1;
      result += String(avg) + (n < numberOfSensors - 1 ? "," : "]");
    }
  }
  return result;
}

