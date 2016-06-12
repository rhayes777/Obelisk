/*
 * PIR sensor tester
 */
 
int ledPin = 13;                // choose the pin for the LED
int inputPins[] = {2, 3, 4};
int pirStates[3] = {};
int numberOfPins = 0;
 
void setup() {
  pinMode(ledPin, OUTPUT);      // declare LED as output
  numberOfPins = sizeof(inputPins)/sizeof(int);
  
  for (int n = 0; n < numberOfPins; n++) {
    pinMode(inputPins[n], INPUT);
  }
  
  Serial.begin(9600);
}

int readPin(int pin, int state, String title) {
  int val = digitalRead(pin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (state == LOW) {
      state = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (state == HIGH){
      state = LOW;
    }
  }
  return state;
}
 
void loop(){
//  Serial.println(numberOfPins);

  bool isChangedState = false;

  String stateString = "[";

  for (int n = 0; n < numberOfPins; n++) {
    int oldState = pirStates[n];
    int newState = readPin(inputPins[n], oldState, String(n));
    pirStates[n] = newState;
    String delimeter = n < numberOfPins - 1 ? "," : "]";
    stateString = stateString + String(newState) + delimeter;
    if (newState != oldState) {
      isChangedState = true;
    }
  }
  
  if (isChangedState) {
     Serial.println(stateString);
  }
}
