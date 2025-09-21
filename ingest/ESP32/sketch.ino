#include <Wifi.h>
#include "DHT.h"
#include <time.h>

// --- Configurações ---
#define DHTPIN 15           // Pino onde o sensor DHT22 está conectado
#define DHTTYPE DHT22       // Define o tipo do sensor como DHT22
const char* SENSOR_ID = "temp-sensor-01";
const char* SENSOR_UNIT = "Celsius";

// --- Objetos e Variáveis Globais ---
DHT dht(DHTPIN, DHTTYPE);
unsigned long lastPublish = 0;
const long interval = 5000; // Publica dados a cada 5 segundos

// --- Funções ---

// Função para gerar uma variação mais realista na temperatura
float getSimulatedTemperature() {
  float baseTemperature = 25.0; // Temperatura base
  // Cria uma onda senoidal para simular variações dia/noite
  float sineWave = 5.0 * sin(millis() / 60000.0); // Varia 5 graus ao longo de ~60s
  // Adiciona um ruído aleatório para pequenas flutuações
  float noise = (random(-10, 11) / 10.0); // Ruído de -1.0 a +1.0
  
  float temperature = baseTemperature + sineWave + noise;

  // Força um pico para testar alertas posteriormente
  // A cada 2 minutos (120 segundos), força um pico de temperatura
  if ((millis() / 1000) % 120 == 0 && millis() > 1000) {
      temperature = 45.0 + noise; // Pico de alta temperatura
  }
  
  return temperature;
}

// Função para obter o timestamp atual
String getTimestamp() {
  char timeStr[30];
  // Usando uma aproximação baseada em millis() para garantir funcionamento no Wokwi
  snprintf(timeStr, sizeof(timeStr), "2025-09-20T%02lu:%02lu:%02luZ", 
           (millis() / 3600000) % 24, (millis() / 60000) % 60, (millis() / 1000) % 60);
  return String(timeStr);
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Simulador de Sensor Iniciado. Gerando dados...");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - lastPublish >= interval) {
    lastPublish = currentMillis;

    float temperature = getSimulatedTemperature();
    
    // Checa se a leitura falhou (não deve acontecer na simulação)
    if (isnan(temperature)) {
      Serial.println("Falha ao ler o sensor!");
      return;
    }

    // Cria o payload JSON
    char jsonPayload[200];
    snprintf(jsonPayload, sizeof(jsonPayload),
             "{\"sensor_id\": \"%s\", \"timestamp\": \"%s\", \"value\": %.2f, \"unit\": \"%s\"}",
             SENSOR_ID,
             getTimestamp().c_str(),
             temperature,
             SENSOR_UNIT);

    // Publica o payload no Monitor Serial
    Serial.println(jsonPayload);
  }
}