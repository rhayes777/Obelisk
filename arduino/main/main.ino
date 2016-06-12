/*
 * PIR sensor tester
 */
 
int ledPin = 13;                // choose the pin for the LED
int inputPin1 = 2;               // choose the input pin (for PIR sensor)
int inputPin2 = 3;
int pirState1 = LOW;             // we start, assuming no motion detected
int pirState2 = LOW;                 // variable for reading the pin status
 
void setup() {
  pinMode(ledPin, OUTPUT);      // declare LED as output
  pinMode(inputPin1, INPUT);     // declare sensor as input
  pinMode(inputPin2, INPUT);     // declare sensor as input
 
  Serial.begin(9600);
}

int readPin(int pin, int state, String title) {
  int val = digitalRead(pin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (state == LOW) {
      // we have just turned on
      Serial.println(title + " on");
      // We only want to print on the output change, not state
      state = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (state == HIGH){
      // we have just turned of
      Serial.println(title + " off");
      // We only want to print on the output change, not state
      state = LOW;
    }
  }
  return state;
}
 
void loop(){
  pirState1 = readPin(inputPin1, pirState1, "First sensor");
  pirState2 = readPin(inputPin2, pirState2, "Second sensor");
}
