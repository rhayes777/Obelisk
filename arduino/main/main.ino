
int ledPin = 13;                
int inputPins[] = {2, 3, 4};
int pirStates[3] = {};
int numberOfPins = 0;
 
void setup() {
  pinMode(ledPin, OUTPUT);    
  numberOfPins = sizeof(inputPins)/sizeof(int);
  
  for (int n = 0; n < numberOfPins; n++) {
    pinMode(inputPins[n], INPUT);
  }
  
  Serial.begin(9600);
}

int readPin(int pin, int state, String title) {
  int val = digitalRead(pin);  
  if (val == HIGH) {           
    digitalWrite(ledPin, HIGH); 
    if (state == LOW) {
      state = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW);
    if (state == HIGH){
      state = LOW;
    }
  }
  return state;
}
 
void loop(){

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
