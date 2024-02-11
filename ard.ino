#include <Servo.h>  

Servo servo;
Servo esc;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5);

  servo.attach(8); 
  esc.attach(3);
}


void loop() {
  if (Serial.available() > 1){
  char key = Serial.read();
  int val = Serial.parseInt();

  switch (key) {
    case 's': servo.writeMicroseconds(val);
    break;
    case 'e': esc.writeMicroseconds(val);
    break;
  }

}}
