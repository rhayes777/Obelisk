#define LEDPin 13 // Onboard LED

int trigPins[] = {2,3,4};
int echoPins[] = {5,6,7};

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
  String result = "[";
  for (int n; n < numberOfSensors; n++) {
    int trigPin = trigPins[n];
    int echoPin = echoPins[n];
    digitalWrite(trigPin, LOW); 
    delayMicroseconds(2); 

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10); 
    
    digitalWrite(trigPin, LOW);
    result += String(pulseIn(echoPin, HIGH)) + (n < numberOfSensors - 1 ? "," : "]");
  }
  Serial.println(result); 
}
