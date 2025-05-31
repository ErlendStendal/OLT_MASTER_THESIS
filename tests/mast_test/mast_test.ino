#include <AccelStepper.h>
#include <Wire.h>
#include <cmath> // For fmod()

// Stepper motor pins
#define STEP_PIN 25
#define DIR_PIN 26

// Potentiometer pin
#define POT_PIN 34 // Connect the potentiometer's analog output here

// Create AccelStepper object
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Motor and encoder variables
const float STEPS_PER_REV = 800.0; // Adjust based on your stepper motor
const float TOTAL_STEPS = STEPS_PER_REV * 10; // Steps for 10 revolutions

void setup() {
  Serial.begin(115200);

  // Initialize stepper motor
  stepper.setMaxSpeed(2000);    // Max speed (steps/second)
  stepper.setAcceleration(10000); // Acceleration (steps/second^2)

  // Initialize potentiometer pin
  pinMode(POT_PIN, INPUT);

  Serial.println("Motor Angle [deg], Potentiometer [deg]");
  Serial.print("current position: ");
  Serial.println(stepper.currentPosition());
  stepper.moveTo(10); // Move to an initial position
}

void loop() {
  // Move to 3600 degrees (10 revolutions)
  stepper.moveTo(TOTAL_STEPS - 10); // Move to the equivalent of 10 revolutions
  while (stepper.distanceToGo() != 0) {
    stepper.run(); // Continuously move the stepper

    // Calculate and print the current motor angle
    float motorAngle = fmod(stepper.currentPosition(), TOTAL_STEPS) * (3600.0 / TOTAL_STEPS);
    if (motorAngle < 0) motorAngle += 3600; // Ensure angle is positive within the range of 10 revolutions

    // Read potentiometer value and convert to degrees for 10 revolutions
    int potValue = analogRead(POT_PIN); // Read raw potentiometer value (0-4095 for ESP32)
    float potAngle = (float)potValue / 4095.0 * 3600.0; // Map to 0-3600 degrees for 10 revolutions

    // Print both angles
    Serial.print(motorAngle, 2);
    Serial.print(", ");
    Serial.println(potAngle, 2);

    
  }
  delay(1000); // Pause for 1 second at 10 revolutions

  // Move back to 0 degrees
  stepper.moveTo(10); // Return to the zero position
  while (stepper.distanceToGo() != 0) {
    stepper.run(); // Continuously move the stepper

    // Calculate and print the current motor angle
    float motorAngle = fmod(stepper.currentPosition(), TOTAL_STEPS) * (3600.0 / TOTAL_STEPS);
    if (motorAngle < 0) motorAngle += 3600; // Ensure angle is positive within the range of 10 revolutions

    // Read potentiometer value and convert to degrees for 10 revolutions
    int potValue = analogRead(POT_PIN); // Read raw potentiometer value (0-4095 for ESP32)
    float potAngle = (float)potValue / 4095.0 * 3600.0; // Map to 0-3600 degrees for 10 revolutions

    // Print both angles
    Serial.print(motorAngle, 2);
    Serial.print(", ");
    Serial.println(potAngle, 2);

    //delay(10); // Small delay for readability
  }
  delay(1000); // Pause for 1 second at 0 degrees
}
