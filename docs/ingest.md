# Estratégia de Ingestão de Dados

## Protocolo escolhido
- **Primário:** MQTT (com QoS 1, sem retain).
- **Alternativas consideradas:**
  - HTTP: simples mas com mais overhead, adequado a edge devices.
  - Serial: útil apenas em simulação local (Wokwi/VSCode).
- **Justificativa:**
  - Baixa latência e overhead.
  - Modelo pub/sub escalável.
  - Suporte a QoS e sessões persistentes.
