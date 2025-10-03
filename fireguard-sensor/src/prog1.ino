// -----------------------------
// FireGuard – Leitura de Sensores + Vibração + Corrente (SCT-013)
//          + Encoder + Ultrassom (HC-SR04) + 4–20mA + MPU6050 + DS18B20 + ZMPT101B
// -----------------------------

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "DHT.h"      // Biblioteca para o DHT22

// 1-Wire bus para DS18B20
#define ONE_WIRE_BUS     4    // DQ do DS18B20 → GPIO4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature oneWireSensors(&oneWire);

// pinos do DHT22
#define DHTPIN           21   // SDA → GPIO21
#define DHTTYPE          DHT22

// pinos digitais
const int pinMQ2           = 16;  // MQ-2 D0 → GPIO16
const int pinFlame         = 17;  // Flame IR D0 → GPIO17
const int pinVibration     = 5;   // SW-420 D0 → GPIO5

// pinos ADC
const int pinCurrentADC    = 36;  // SCT-013 → GPIO36 (ADC1_CH0)
const int pinPressureSensor= 39;  // 4–20mA shunt 250Ω → GPIO39 (ADC1_CH3)

// pinos do ZMPT101B (simulado via Potentiometer no ADC)
const int pinZMPT          = 34;  // ZMPT101B simulado → GPIO34 (ADC1_CH6)
// Fator de calibração: cada 1 V no ADC representa ~311 V de pico real na rede
const float Kcal           = 311.0;

// encoder (KY-040 ou equivalente)
#define ENCODER_A        18   // CLK → GPIO18
#define ENCODER_B        19   // DT  → GPIO19
volatile int encoderCount = 0;

// HC-SR04
#define TRIG_PIN         12   // TRIG → GPIO12
#define ECHO_PIN         14   // ECHO → GPIO14

// MPU-6050
Adafruit_MPU6050 mpu;

// DHT22
DHT dht(DHTPIN, DHTTYPE);

// Encoder ISR
void IRAM_ATTR handleEncoder() {
  encoderCount++;
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println();
  Serial.println("=== FireGuard iniciado ===");

  // I2C & MPU6050
  Wire.begin(21, 22);  // SDA=GPIO21, SCL=GPIO22
  if (!mpu.begin()) {
    Serial.println("MPU6050 não respondeu, mas continuaremos lendo.");
  } else {
    Serial.println("MPU6050 iniciado.");
  }

  // DHT22
  dht.begin();

  // DS18B20 1-Wire
  pinMode(ONE_WIRE_BUS, INPUT_PULLUP);
  oneWireSensors.begin();
  Serial.println("DS18B20 iniciado.");

  // Digitais
  pinMode(pinMQ2,       INPUT);
  pinMode(pinFlame,     INPUT);
  pinMode(pinVibration, INPUT);

  // Encoder
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), handleEncoder, RISING);

  // HC-SR04
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // ZMPT101B simulado via ADC34 – nada a inicializar
}

void loop() {
  // 1. DHT22
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Erro ao ler DHT22!");
  } else {
    Serial.print("DHT22 → Umid: "); Serial.print(h);
    Serial.print("%  | Temp: "); Serial.print(t);
    Serial.println(" °C");
  }

  // 2. MQ-2
  Serial.println(
    digitalRead(pinMQ2)==LOW
      ? "MQ-2 → Alerta de GÁS/FUMAÇA!"
      : "MQ-2 → Sem Gás/Fumaça."
  );

  // 3. Flame IR
  Serial.println(
    digitalRead(pinFlame)==LOW
      ? "Flame IR → Chama DETECTADA!"
      : "Flame IR → Sem Chama."
  );

  // 4. SW-420
  Serial.println(
    digitalRead(pinVibration)==LOW
      ? "SW-420 → Vibração DETECTADA!"
      : "SW-420 → Sem Vibração."
  );

  // 5. SCT-013
  int raw = analogRead(pinCurrentADC);
  float volts = (raw / 4095.0f) * 3.3f;
  Serial.print("SCT-013 → ADC: "); Serial.print(raw);
  Serial.print("  | V: "); Serial.print(volts,3); Serial.println(" V");

  // 6. Encoder
  Serial.print("Encoder count: "); Serial.println(encoderCount);

  // 7. HC-SR04
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = (duration * 0.0343f) / 2.0f;
  Serial.print("HC-SR04 → Dist: "); Serial.print(distance,2);
  Serial.println(" cm");

  // 8. 4–20mA
  int sensorValue = analogRead(pinPressureSensor);
  float voltage420 = (sensorValue / 4095.0f) * 3.3f;
  float current_mA = (voltage420 / 250.0f) * 1000.0f;
  Serial.print("4-20mA → ADC: "); Serial.print(sensorValue);
  Serial.print("  | V: "); Serial.print(voltage420,3);
  Serial.print(" V  | I: "); Serial.print(current_mA,1);
  Serial.println(" mA");

  // 9. DS18B20
  oneWireSensors.requestTemperatures();
  float temp1 = oneWireSensors.getTempCByIndex(0);
  if (temp1 == DEVICE_DISCONNECTED_C) {
    Serial.println("DS18B20 → Falha na leitura!");
  } else {
    Serial.print("DS18B20 → Temp: "); Serial.print(temp1,1);
    Serial.println(" °C");
  }

  // 10. MPU6050
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);
  Serial.print("MPU → Acel X:"); Serial.print(accel.acceleration.x,1);
  Serial.print(" Y:"); Serial.print(accel.acceleration.y,1);
  Serial.print(" Z:"); Serial.print(accel.acceleration.z,1);
  Serial.println(" m/s²");
  Serial.print("MPU → Gyro X:"); Serial.print(gyro.gyro.x,1);
  Serial.print(" Y:"); Serial.print(gyro.gyro.y,1);
  Serial.print(" Z:"); Serial.print(gyro.gyro.z,1);
  Serial.println(" rad/s");

  // 11. ZMPT101B (Tensão AC)
  int rawZ = analogRead(pinZMPT);
  float v_adc  = (rawZ / 4095.0f) * 3.3f;
  float v_peak = v_adc * Kcal;
  float v_rms  = v_peak / 1.4142f;
  Serial.print("ZMPT101B → Vadc: "); Serial.print(v_adc,3);
  Serial.print(" V  | Vp: "); Serial.print(v_peak,1);
  Serial.print(" V  | Vrms: "); Serial.print(v_rms,1);
  Serial.println(" V");

  Serial.println("-------------------------------");
  delay(2000);
}