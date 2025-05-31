#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <SPI.h>
#include <SD.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>  // For GPS

#define SD_CS 5
#define BUTTON_PIN 4
#define LED_PIN 2
#define POT1_PIN 36
#define POT2_PIN 39
#define POT3_PIN 35
#define GPS_RX_PIN 16
#define GPS_TX_PIN 17

// Sampling Rates (in milliseconds)

// GPS Data (declared globally so that it can be used in multiple functions)
String gpsTimeStr = "00:00:00";  // Global readable timestamp
float latitude = 0.0;
float longitude = 0.0;
float speed = 0.0;
float course = 0.0;

// Initialize objects for the BNO055, SD, and GPS
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);
TinyGPSPlus gps;
HardwareSerial myGPS(1);

void sendUBX(byte *msg, byte len) {
  byte ck_a = 0, ck_b = 0;
  for (int i = 2; i < len - 2; i++) {
    ck_a = ck_a + msg[i];
    ck_b = ck_b + ck_a;
  }
  msg[len - 2] = ck_a;
  msg[len - 1] = ck_b;
  myGPS.write(msg, len);
}

void setGPSRateTo10Hz() {
  byte setRate[] = {
    0xB5, 0x62, 0x06, 0x08,
    0x06, 0x00,
    0x64, 0x00,  // 100 ms = 10 Hz
    0x01, 0x00,
    0x01, 0x00,
    0x00, 0x00   // Placeholder for checksum
  };
  sendUBX(setRate, sizeof(setRate));
}
File logFile;

bool logging = false;
bool buttonState = false;
bool lastButtonState = false;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;  // debounce delay in milliseconds

unsigned long gpsSamplingRate = 100;  // 10 Hz
unsigned long sensorSamplingRate = 100;  // 10 Hz
unsigned long lastGpsTime = 0;
unsigned long lastSensorTime = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Initialize the BNO055
  if (!bno.begin()) {
    Serial.println("Couldn't find BNO055");
    while (1);
  }

  // Start GPS serial communication at the correct baud rate
  myGPS.begin(38400, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN); 
  setGPSRateTo10Hz();

  // Initialize the SD card
  if (!SD.begin(SD_CS)) {
    Serial.println("SD card failed");
    while (1);
  }

  pinMode(BUTTON_PIN, INPUT_PULLUP); // Button should be connected to ground and GPIO 4
  pinMode(LED_PIN, OUTPUT); // LED should be connected to GPIO 2

  Serial.println("System initialized");
}

void loop() {
  // Read the button state
  bool reading = digitalRead(BUTTON_PIN) == LOW;  // Button pressed when LOW

  // Check if the button state has changed and if debounce delay has passed
  if (reading != lastButtonState) {
    lastDebounceTime = millis();  // reset debounce timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      // If the button was just pressed, toggle logging
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

  // Fetch and print data at specified sampling rates
  if (millis() - lastGpsTime >= gpsSamplingRate) {
    lastGpsTime = millis();
    logGpsData();
  }

  if (millis() - lastSensorTime >= sensorSamplingRate) {
    lastSensorTime = millis();
    logSensorData();
  }
}

void logSensorData() {
  // Read potentiometer data
  int pot1Value = analogRead(POT1_PIN);
  int pot2Value = analogRead(POT2_PIN);
  int pot3Value = analogRead(POT3_PIN);

  // Read acceleration and gyro data from BNO055
  
  sensors_event_t accelData, magData, gyroData;
  bno.getEvent(&accelData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
  bno.getEvent(&magData, Adafruit_BNO055::VECTOR_MAGNETOMETER);
  bno.getEvent(&gyroData, Adafruit_BNO055::VECTOR_GYROSCOPE);

  float accelX = accelData.acceleration.x;
  float accelY = accelData.acceleration.y;
  float accelZ = accelData.acceleration.z;
  float gyroX = gyroData.gyro.x;
  float gyroY = gyroData.gyro.y;
  float gyroZ = gyroData.gyro.z;
  float magX = magData.magnetic.x;
  float magY = magData.magnetic.y;
  float magZ = magData.magnetic.z;

  // Print to the serial monitor with timestamp
  Serial.print(gpsTimeStr);  // GPS Time
  Serial.print(",");
  Serial.print(pot1Value); // Potentiometer 1
  Serial.print(",");
  Serial.print(pot2Value); // Potentiometer 2
  Serial.print(",");
  Serial.print(pot3Value); // Potentiometer 3
  Serial.print(",");
  Serial.print(accelX);  // Accel X
  Serial.print(",");
  Serial.print(accelY);  // Accel Y
  Serial.print(",");
  Serial.print(accelZ);  // Accel Z
  Serial.print(",");
  Serial.print(gyroX);  // Gyro X
  Serial.print(",");
  Serial.print(gyroY);  // Gyro Y
  Serial.print(",");
  Serial.print(gyroZ);  // Gyro Z
  Serial.print(",");
  Serial.print(magX);  // Mag X
  Serial.print(",");
  Serial.print(magY);  // Mag Y
  Serial.print(",");
  Serial.print(magZ);  // Mag Z


  // Print GPS data (or 0 if not available)
  Serial.print(",");
  Serial.print(latitude, 6); // Latitude
  Serial.print(",");
  Serial.print(longitude, 6); // Longitude
  Serial.print(",");
  Serial.print(speed); // Speed
  Serial.print(",");
  Serial.println(course); // Course

  // If logging, save to SD card
  if (logging) {
    logFile.print(gpsTimeStr);  // GPS Time
    logFile.print(",");
    logFile.print(pot1Value); // Potentiometer 1
    logFile.print(",");
    logFile.print(pot2Value); // Potentiometer 2
    logFile.print(",");
    logFile.print(pot3Value); // Potentiometer 3
    logFile.print(",");
    logFile.print(accelX);  // Accel X
    logFile.print(",");
    logFile.print(accelY);  // Accel Y
    logFile.print(",");
    logFile.print(accelZ);  // Accel Z
    logFile.print(",");
    logFile.print(gyroX);  // Gyro X
    logFile.print(",");
    logFile.print(gyroY);  // Gyro Y
    logFile.print(",");
    logFile.print(gyroZ);  // Gyro Z
    logFile.print(",");
    logFile.print(magX);  // Mag X
    logFile.print(",");
    logFile.print(magY);  // Mag Y
    logFile.print(",");
    logFile.print(magZ);  // Mag Z
    logFile.print(",");
    logFile.print(latitude, 6); // Latitude
    logFile.print(",");
    logFile.print(longitude, 6); // Longitude
    logFile.print(",");
    logFile.print(speed); // Speed
    logFile.print(",");
    logFile.println(course); // Course
  }
}

void logGpsData() {
  // Read GPS data
  while (myGPS.available()) {
    gps.encode(myGPS.read());  // Feed the data to the GPS object

    // When new GPS data is available
    if (gps.location.isUpdated()) {
      if (gps.time.isValid()) {
        int hour = (gps.time.hour() + 2) % 24;  // Norway summer time (UTC+2)
        int minute = gps.time.minute();
        int second = gps.time.second();

        char timestamp[16];
        snprintf(timestamp, sizeof(timestamp), "%02d:%02d:%02d", hour, minute, second);
        gpsTimeStr = String(timestamp);
      } else {
        gpsTimeStr = "00:00:00";  // GPS time not available
      }

      // Update global values
      latitude = gps.location.lat();
      longitude = gps.location.lng();
      speed = gps.speed.mps();
      course = gps.course.deg();
    }
  }
}

void startLogging() {
  // Create a new file with a timestamp
  String filename = "/log_" + String(millis()) + ".csv";
  logFile = SD.open(filename, FILE_WRITE);
  if (logFile) {
    Serial.println("Logging started");
    digitalWrite(LED_PIN, HIGH); // Turn on LED
    logFile.println("GPS_Time,Pot1,Pot2,Pot3,AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ,MagX,MagY,MagZ,Lat,Lon,Speed,Course"); // CSV header for all data
    logging = true;
  } else {
    Serial.println("Failed to open file for writing");
  }
}

void closeLogging() {
  logFile.close();
  Serial.println("Logging stopped");
  digitalWrite(LED_PIN, LOW); // Turn off LED
  logging = false;
}