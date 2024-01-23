#include <Servo.h>
#define esc 8
//
Servo motor;
 
void setup() {
  motor.attach(esc);
  
  
  Serial.begin(9600);
}
  
  

void loop() {
int val = map(analogRead(0), 0, 1023, 1000, 1500);
//motor.writeMicroseconds(val); // 1230 
Serial.println(val);



}
