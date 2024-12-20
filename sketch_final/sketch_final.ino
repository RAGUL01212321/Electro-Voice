const int motorPin = 4;
const int touchPin = 2;
const int touchPin2 = 3;

unsigned long startTime = 0;
unsigned long duration = 0;
bool sensorPressed = false;

void setup() {
  pinMode(touchPin, INPUT);
  pinMode(touchPin2, INPUT);
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int sensorState = digitalRead(touchPin);
  int sensorState2 = digitalRead(touchPin2);

  // Detecting simultaneous press
  if (sensorState == HIGH && sensorState2 == HIGH) {
    vibrateMotor(200);  // Vibrate motor for 0.2 seconds
    delay(500);         // Add a delay to prevent rapid triggering
    Serial.println();   // Move to the next line in serial output
    return;             // Exit the loop iteration and wait for further input
  }

  // Detecting dot and dash duration
  if (sensorState == HIGH && !sensorPressed) {
    sensorPressed = true;
    startTime = millis();
  }

  if (sensorState == LOW && sensorPressed) {
    sensorPressed = false;
    duration = millis() - startTime;

    if (duration >= 50 && duration <= 150) {
      Serial.print(".");  // Dot
    } else if (duration > 150 && duration <= 800) {
      Serial.print("-");  // Dash
    }
  }

  // Detecting word separation (slash) when second sensor is pressed
  if (sensorState2 == HIGH) {
    Serial.print("/");  // Separate letters
    delay(300);         // Debounce delay
  }

  // Check for commands from Python
  if (Serial.available() > 0) {
    char incomingChar = Serial.read();
    if (incomingChar == '.') {
      vibrateMotor(250);  // Dot vibration
    } else if (incomingChar == '-') {
      vibrateMotor(500);  // Dash vibration
    } else if (incomingChar == '/') {
      delay(500);  // Slash pass
    }
  }
}

// Vibration motor function
void vibrateMotor(int vibrateTime) {
  digitalWrite(motorPin, HIGH);
  delay(vibrateTime);
  digitalWrite(motorPin, LOW);
  delay(100);
}

