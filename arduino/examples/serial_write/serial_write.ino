void setup() {
  Serial.begin(9600);

}

void loop() {
  while (Serial.available() > 0) {
    int red = Serial.parseInt();
    int green = Serial.parseInt();
    int blue = Serial.parseInt();

     if (Serial.read() == '\n') {
      red = 255 - constrain(red, 0, 255);
      green = 255 - constrain(green, 0, 255);
      blue = 255 - constrain(blue, 0, 255);

      Serial.print(red, HEX);
      Serial.print(green, HEX);
      Serial.println(blue, HEX);
     }
  }

}
