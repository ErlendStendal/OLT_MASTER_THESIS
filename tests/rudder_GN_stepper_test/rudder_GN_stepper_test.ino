#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <SPI.h>
#include <SD.h>
#include <AccelStepper.h>

#define SD_CS 5
#define BUTTON_PIN 4
#define LED_PIN 2
#define POT1_PIN 36
#define POT3_PIN 35
#define STEP_PIN 25
#define DIR_PIN 26

// Stepper configuration
const int STEPS_PER_REV = 3200; // 1.8° step with 1/16 microstepping
const int STEPS_FOR_270 = (250.0 / 360.0) * STEPS_PER_REV;

// AccelStepper setup (DRIVER mode)
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// BNO055 and SD
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);
File logFile;

bool logging = false;
bool buttonState = false;
bool lastButtonState = false;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
unsigned long sensorSamplingRate = 100;  // 10 Hz
unsigned long lastSensorTime = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!bno.begin()) {
    Serial.println("Couldn't find BNO055");
    while (1);
  }

  if (!SD.begin(SD_CS)) {
    Serial.println("SD card failed");
    while (1);
  }

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);

  // Stepper settings
  stepper.setMaxSpeed(1000); // steps/sec
  stepper.setAcceleration(500); // steps/sec^2
  stepper.moveTo(STEPS_FOR_270); // initial target
}

void loop() {
  // Debounce button
  bool reading = digitalRead(BUTTON_PIN) == LOW;
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState) {
        if (logging) {
          closeLogging();
        } else {
          startLogging();
        }
      }
    }
  }

  lastButtonState = reading;

  // Stepper movement
  if (stepper.distanceToGo() == 0) {
    long nextTarget = (stepper.currentPosition() == STEPS_FOR_270) ? 0 : STEPS_FOR_270;
    stepper.moveTo(nextTarget);
  }
  stepper.run();

  if (millis() - lastSensorTime >= sensorSamplingRate) {
    lastSensorTime = millis();
    logSensorData();
  }
}

float getStepperAngle() {
  return (360.0 * stepper.currentPosition()) / STEPS_PER_REV;
}

void logSensorData() {
  int pot1Value = analogRead(POT1_PIN);
  int pot3Value = analogRead(POT3_PIN);

  sensors_event_t accelData, magData, gyroData;
  bno.getEvent(&accelData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
  bno.getEvent(&magData, Adafruit_BNO055::VECTOR_MAGNETOMETER);
  bno.getEvent(&gyroData, Adafruit_BNO055::VECTOR_GYROSCOPE);

  float stepperAngle = getStepperAngle();

  float accelX = accelData.acceleration.x;
  float accelY = accelData.acceleration.y;
  float accelZ = accelData.acceleration.z;
  float gyroX = gyroData.gyro.x;
  float gyroY = gyroData.gyro.y;
  float gyroZ = gyroData.gyro.z;
  float magX = magData.magnetic.x;
  float magY = magData.magnetic.y;
  float magZ = magData.magnetic.z;

  Serial.print(pot1Value); Serial.print(",");
  Serial.print(pot3Value); Serial.print(",");
  Serial.print(accelX); Serial.print(",");
  Serial.print(accelY); Serial.print(",");
  Serial.print(accelZ); Serial.print(",");
  Serial.print(gyroX); Serial.print(",");
  Serial.print(gyroY); Serial.print(",");
  Serial.print(gyroZ); Serial.print(",");
  Serial.print(magX); Serial.print(",");
  Serial.print(magY); Serial.print(",");
  Serial.print(magZ); Serial.print(",");
  Serial.println(stepperAngle);

  if (logging) {
    logFile.print(pot1Value); logFile.print(",");
    logFile.print(pot3Value); logFile.print(",");
    logFile.print(accelX); logFile.print(",");
    logFile.print(accelY); logFile.print(",");
    logFile.print(accelZ); logFile.print(",");
    logFile.print(gyroX); logFile.print(",");
    logFile.print(gyroY); logFile.print(",");
    logFile.print(gyroZ); logFile.print(",");
    logFile.print(magX); logFile.print(",");
    logFile.print(magY); logFile.print(",");
    logFile.print(magZ); logFile.print(",");
    logFile.println(stepperAngle);
  }
}

void startLogging() {
  String filename = "/log_" + String(millis()) + ".csv";
  logFile = SD.open(filename, FILE_WRITE);
  if (logFile) {
    Serial.println("Logging started");
    digitalWrite(LED_PIN, HIGH);
    logFile.println("Pot1,Pot3,AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ,MagX,MagY,MagZ,StepperAngle");
    logging = true;
  } else {
    Serial.println("Failed to open file for writing");
  }
}

void closeLogging() {
  logFile.close();
  Serial.println("Logging stopped");
  digitalWrite(LED_PIN, LOW);
  logging = false;
}
