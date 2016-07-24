#define LEDPin 13 // Onboard LED

int trigPins[] = {2,3,4,5};
int echoPins[] = {6,7,8,9};

int numberOfSensors;

long duration, distance; // Duration used to calculate distance

void setup() {
    Serial.begin(9600);
    numberOfSensors = sizeof(trigPins)/sizeof(int);

 for (int n; n < numberOfSensors; n++) {
    pinMode(trigPins[n], OUTPUT);
    pinMode(echoPins[n], INPUT);
 }
 pinMode(LEDPin, OUTPUT); // Use LED indicator (if required)
}

void loop() {
  if (Serial.available()) {
    Serial.println(recordDataString()); 
  }
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

