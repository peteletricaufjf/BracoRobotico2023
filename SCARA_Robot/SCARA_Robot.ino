
/*
   Arduino based SCARA Robot
   by Dejan, www.HowToMechatronics.com
   AccelStepper: http://www.airspayce.com/mikem/arduino/AccelStepper/index.html

*/
#include <AccelStepper.h>
#include <math.h>

#define limitSwitch1 11
#define limitSwitch2 10
#define eletroima 12
#define limitSwitch4 A3

// Define the stepper motors and the pins the will use
AccelStepper stepper1(1, 2, 5); // (Type:driver, STEP, DIR)
AccelStepper stepper2(1, 3, 6);
AccelStepper stepper4(1, 12, 13);


double x = 10.0;
double y = 10.0;
double L1 = 228; // L1 = 228mm
double L2 = 136.5; // L2 = 136.5mm
double theta1, theta2, z;

int stepper1Position, stepper2Position, stepper4Position;

const float theta1AngleToSteps = 44.444444;
const float theta2AngleToSteps = 35.555555;
const float zDistanceToSteps = 100;

byte inputValue[2];
int k = 0;

String content = "";
int data[6];

void setup() {
  Serial.begin(115200);

  pinMode(limitSwitch1, INPUT_PULLUP);
  pinMode(limitSwitch2, INPUT_PULLUP);
  pinMode(limitSwitch4, INPUT_PULLUP);

  pinMode(eletroima, OUTPUT);

  // Stepper motors max speed
  stepper1.setMaxSpeed(4000);
  stepper1.setAcceleration(2000);
  stepper2.setMaxSpeed(4000);
  stepper2.setAcceleration(2000);
  stepper4.setMaxSpeed(4000);
  stepper4.setAcceleration(2000);

  // initial eletroimã value - desligado (logica dessa merda tá invertida e fiquei com preguiça de mudar o fio)
  // data[5] = 1;

  digitalWrite(eletroima, LOW);
  //data[2] = 100;
  delay(1000);
  homing();
}

void loop() {

  if (Serial.available()) {
    content = Serial.readString(); // Read the incomding data from Processing
    // Extract the data from the string and put into separate integer variables (data[] array)
    for (int i = 0; i < 6; i++) {
      int index = content.indexOf(","); // locate the first ","
      data[i] = content.substring(0, index).toInt(); //Extract the number from start to the ","
      content = content.substring(index + 1); //Remove the number from the string
      Serial.println(data[i]);

    }
  /*
    data[0] - Angulo j1
    data[1] - Angulo j2
    data[2] - Eixo Z (posição)
    data[3] - Velocidade
    data[4] - Aceleração
    data[5] - Garra
  */

  stepper1Position = data[0] * theta1AngleToSteps;
  stepper2Position = data[1] * theta2AngleToSteps;
  stepper4Position = data[2] * zDistanceToSteps;

  stepper1.setSpeed(data[3]);
  stepper2.setSpeed(data[3]);
  stepper4.setSpeed(data[3]);

  stepper1.setAcceleration(data[4]);
  stepper2.setAcceleration(data[4]);
  stepper4.setAcceleration(data[4]);

  stepper1.moveTo(stepper1Position);
  stepper2.moveTo(stepper2Position);
  stepper4.moveTo(stepper4Position);

  while (stepper1.currentPosition() != stepper1Position || stepper2.currentPosition() != stepper2Position || stepper4.currentPosition() != stepper4Position) {
    stepper1.run();
    stepper2.run();
    stepper4.run();
  }
  delay(100);


  if (data[5] == 1) {
    digitalWrite(eletroima, HIGH);
  }
    else {
      digitalWrite(eletroima, LOW);
    }
  }

  Serial.println("deu");
}

void homing() {
  // Homing Stepper4

  Serial.println("motor4");
  while (digitalRead(limitSwitch4) != 1) {
    stepper4.setSpeed(-650);
    stepper4.runSpeed();
    stepper4.setCurrentPosition(-1978); // When limit switch pressed set position to 0 steps
  }
  delay(20);
  stepper4.moveTo(5000);
  while (stepper4.currentPosition() != 5000) {
    stepper4.run();
  }


  // Homing Stepper2
  Serial.println("motor2");
  while (digitalRead(limitSwitch2) != 1) {
    stepper2.setSpeed(-1300);
    stepper2.runSpeed();
    stepper2.setCurrentPosition(-5420); // When limit switch pressed set position to -5440 steps
  }
  delay(20);

  stepper2.moveTo(0);
  while (stepper2.currentPosition() != 0) {
    stepper2.run();
  }

  // Homing Stepper1
  Serial.println("motor1");
  while (digitalRead(limitSwitch1) != 1) {
    stepper1.setSpeed(-1200);
    stepper1.runSpeed();
    stepper1.setCurrentPosition(-3955); // When limit switch pressed set position to 0 steps
  }
  delay(20);
  stepper1.moveTo(800);
  while (stepper1.currentPosition() != 800) {
    stepper1.run();
  }
}

void serialFlush() {
  while (Serial.available() > 0) {  //while there are characters in the serial buffer, because Serial.available is >0
    Serial.read();         // get one character
  }
}
