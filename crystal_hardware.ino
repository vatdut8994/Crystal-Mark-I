#include <Stepper.h>
#include <Servo.h>

String serialData;

Servo shoulder;  //Higher to decrease
Servo elbow;     //Higher to increase
Servo wrist;     //Higher to decrease
Servo fingers;   //Higher to increase


int in1 = 4;
int in2 = 5;
int in3 = 6;
int in4 = 7;


void forward(){
  digitalWrite(in1, 0);
  digitalWrite(in2, 1);
  digitalWrite(in3, 1);
  digitalWrite(in4, 0);
}

void backward(){
  digitalWrite(in1, 1);
  digitalWrite(in2, 0);
  digitalWrite(in3, 0);
  digitalWrite(in4, 1);
}

void left(){
  digitalWrite(in1, 1);
  digitalWrite(in2, 0);
  digitalWrite(in3, 1);
  digitalWrite(in4, 0);
}

void right(){
  digitalWrite(in1, 0);
  digitalWrite(in2, 1);
  digitalWrite(in3, 0);
  digitalWrite(in4, 1);
}

void stop_car(){
  digitalWrite(in1, 0);
  digitalWrite(in2, 0);
  digitalWrite(in3, 0);
  digitalWrite(in4, 0);
}


void setup() {
  Serial.begin(9600);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  shoulder.attach(10);
  elbow.attach(11);
  wrist.attach(9);
  fingers.attach(8);
  shoulder.write(0);
  elbow.write(0);
}
 
void loop() {
  if (Serial.available() > 0){
    serialData = Serial.readString();
    Serial.println(serialData);
    if (serialData == "1"){
      fingers.write(30);
    }else if (serialData == "2"){
      fingers.write(150);
    }else if (serialData == "3"){
      forward();
    }else if (serialData == "4"){
      backward();
    }else if (serialData == "5"){
      wrist.write(0);
    }else if (serialData == "6"){
      wrist.write(180);
    }else if (serialData == "7"){
      elbow.write(180);
    }else if (serialData == "8"){
      elbow.write(0);
    }else if (serialData == "9"){
      shoulder.write(0);
    }else if (serialData == "10"){
      shoulder.write(180);
    }else if (serialData == "11"){
      shoulder.write(45);
    }else if (serialData == "12"){
      shoulder.write(90);
    }else if (serialData == "13"){
      shoulder.write(135);
    }else if (serialData == "14"){
      elbow.write(135);
    }else if (serialData == "15"){
      elbow.write(90);
    }else if (serialData == "16"){
      elbow.write(45);
    }else if (serialData == "17"){
      wrist.write(45);
    }else if (serialData == "18"){
      wrist.write(90);
    }else if (serialData == "19"){
      wrist.write(135);
    }else if (serialData == "0"){
      stop_car();
    }
  }
  digitalWrite(in1, 1);
  digitalWrite(in2, 0);
}
