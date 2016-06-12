/*
 * PIR sensor tester
 */
 
int ledPin = 13;                // choose the pin for the LED
int inputPins[] = {2, 3, 4};
int pirStates[] = {LOW, LOW, LOW};
 
void setup() {
  pinMode(ledPin, OUTPUT);      // declare LED as output
  for (int n = 0; n < (sizeof(inputPins)/sizeof(int)); n++) {
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

  bool isChangedState = false;

  for (int n = 0; n < (sizeof(inputPins)/sizeof(int)); n++) {
    int oldState = pirStates[n];
    int newState = readPin(inputPins[n], oldState, String(n));
    pirStates[n] = newState;
    if (newState != oldState) {
      isChangedState = true;
    }
  }
  
  if (isChangedState) 
    Serial.write((uint8_t*)pirStates, sizeof(pirStates));
}
