#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "DHT.h"

// ==== CONFIG WiFi ====
const char *ssid = "Wokwi-GUEST";
const char *password = "";
const char *serverUrl = "http://192.168.0.10:8000/sensors/"; // sua API

// ==== SENSORES ====
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature oneWireSensors(&oneWire);

#define DHTPIN 21
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const int pinMQ2 = 16;
const int pinFlame = 17;
const int pinVibration = 5;
const int pinCurrentADC = 36;
const int pinPressureSensor = 39;
const int pinZMPT = 34;
#define Kcal 311.0

#define ENCODER_A 18
#define ENCODER_B 19
volatile int encoderCount = 0;

#define TRIG_PIN 12
#define ECHO_PIN 14

Adafruit_MPU6050 mpu;

// ==== Funções Aux ====
void IRAM_ATTR handleEncoder() { encoderCount++; }

String getISO8601Time() {
  time_t now = time(nullptr);
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  char buf[25];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
  return String(buf);
}

void setup() {
  Serial.begin(115200);

  // WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("WiFi conectado!");

  // NTP
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  // Sensores
  Wire.begin(21,22);
  mpu.begin();
  dht.begin();
  oneWireSensors.begin();
  pinMode(pinMQ2, INPUT);
  pinMode(pinFlame, INPUT);
  pinMode(pinVibration, INPUT);
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), handleEncoder, RISING);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // ==== Leitura de sensores (resumida para exemplo) ====
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int mq2 = digitalRead(pinMQ2);
  int flame = digitalRead(pinFlame);
  int vibra = digitalRead(pinVibration);
  int raw = analogRead(pinCurrentADC);
  float volts = (raw / 4095.0f) * 3.3f;
  int pulses = encoderCount; encoderCount = 0;
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  float dist = (duration * 0.0343f) / 2.0f;

  // DS18B20
  oneWireSensors.requestTemperatures();
  float ds_t = oneWireSensors.getTempCByIndex(0);

  // MPU
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  // ZMPT101B
  int rawZ = analogRead(pinZMPT);
  float v_adc = (rawZ / 4095.0f) * 3.3f;
  float v_peak = v_adc * Kcal;
  float v_rms  = v_peak / 1.4142f;

  // ==== Monta JSON ====
  StaticJsonDocument<800> doc;
  doc["timestamp"] = getISO8601Time();
  doc["dht_t"] = t;
  doc["dht_h"] = h;
  doc["mq2_d"] = mq2;
  doc["flame_d"] = flame;
  doc["vibra_d"] = vibra;
  doc["current_v"] = volts;
  doc["encoder_c"] = pulses;
  doc["dist_cm"] = dist;
  doc["ds_t"] = ds_t;
  doc["mpu_ax"] = accel.acceleration.x;
  doc["mpu_ay"] = accel.acceleration.y;
  doc["mpu_az"] = accel.acceleration.z;
  doc["mpu_gx"] = gyro.gyro.x;
  doc["mpu_gy"] = gyro.gyro.y;
  doc["mpu_gz"] = gyro.gyro.z;
  doc["zmpt_vrms"] = v_rms;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  // ==== Envia HTTP ====
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonPayload);

    Serial.print("POST: ");
    Serial.println(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.printf("Resposta HTTP %d\n", httpResponseCode);
      Serial.println(http.getString());
    } else {
      Serial.printf("Erro HTTP %d\n", httpResponseCode);
    }
    http.end();
  }

  delay(5000); // aguarda antes da próxima leitura
}
