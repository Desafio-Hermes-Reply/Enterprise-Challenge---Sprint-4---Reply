# Módulo de Coleta de Dados com ESP32 (Simulado)

Este diretório contém o firmware desenvolvido para um ESP32, simulado na plataforma Wokwi, responsável por gerar e publicar dados de um sensor de temperatura (DHT22).

## Funcionalidades
- **Geração de Dados Sintéticos:** Os dados de temperatura são gerados de forma dinâmica para simular um ambiente industrial, incluindo variações cíclicas e picos de anomalia para testes de alertas.
- **Formato de Dados:** As leituras são formatadas no padrão JSON, contendo os campos `sensor_id`, `timestamp`, `value` e `unit`.
- **Publicação:** Os dados são publicados via Saída Serial para fácil captura e ingestão.

## Como Executar a Simulação
O código pode ser executado diretamente na plataforma Wokwi através deste link do projeto: [text](https://wokwi.com/projects/442655409200613377)