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
    
## Estratégia de Batching, Retries e DLQ

- **Batching:** mensagens podem ser agrupadas para inserção em lote (exemplo: N=200 ou T=2s). Para o POC foi usada inserção simples.
- **Retries:** em falhas de conexão com o DB, usar retry com backoff exponencial.
- **DLQ:** mensagens inválidas (erros de schema) devem ser registradas em uma tabela `ingest_dead_letter` para posterior análise.
