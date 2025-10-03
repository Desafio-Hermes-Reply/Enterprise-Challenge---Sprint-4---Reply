# Enterprise Challenge - Sprint 4 - Reply

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="assets\logo-fiap.png" alt="FIAP" width="300">
  </a>
</p>

**Projeto final da disciplina de Inteligência Artificial, em parceria com a Hermes Reply.**

---

## 👨‍🎓 Integrantes

* **Antônio Ancelmo Neto Barros**
    * **RM:** rm563683
    * **GitHub:** [@AntonioBarros19](https://github.com/AntonioBarros19)
* **Beatriz Pilecarte de Melo**
    * **RM:** rm564952
    * **GitHub:** [@BPilecarte](https://github.com/BPilecarte)
* **Francismar Alves Martins Junior**
    * **RM:** rm562869
    * **GitHub:** [@yggdrasilGit](https://github.com/yggdrasilGit)
* **Matheus Soares Bento da Silva**
    * **RM:** rm565540
    * **GitHub:** [@matheusbento044](https://github.com/matheusbento04)
* **Vitor Eiji Fernandes Teruia**
    * **RM:** rm563683
    * **GitHub:** [@Vitor985-hub](https://github.com/Vitor985-hub)

## 👩‍🏫 Professores

* **Tutor:** Leonardo Ruiz Orabona
* **Coordenador:** André Godoi Chiovato

---

## 📜 Descrição do Projeto

Este projeto implementa um MVP (Minimum Viable Product) de um **pipeline de dados fim-a-fim**, simulando um cenário de monitoramento na Indústria 4.0. O fluxo consolida as etapas de arquitetura, coleta, armazenamento, modelagem e visualização de dados, demonstrando uma solução integrada e funcional.

O objetivo é transformar os dados brutos gerados por sensores em insights acionáveis, exibidos em um dashboard com métricas de desempenho e um sistema de alertas para detecção de anomalias, como picos de temperatura em um maquinário industrial.

---

## 🏛️ Arquitetura da Solução

A arquitetura do sistema foi desenhada para ser modular e escalável, representando o fluxo completo de dados desde a origem até a camada de apresentação.

![Arquitetura da Solução](docs/arquitetura/reply_arquitetura_drawio.png)

*O arquivo editável do diagrama (`.drawio`) está disponível no diretório `/docs/arquitetura/`.*

---
## prints do sensor/monitor serial

<img src="docs\screenshots\Captura de Tela 2025-10-03 às 18.57.52.png" width="500">
<img src="docs\screenshots\Captura de Tela 2025-10-03 às 18.58.05.png" width="500">
<img src="docs\screenshots\Captura de Tela 2025-10-03 às 18.58.25.png" width="500">
<img src="docs\screenshots\Captura de Tela 2025-10-03 às 18.58.35.png" width="500">

---
## prints dos diagramas lógico e racional
<img src="db\reply_modelo_db\src\logical_model_db_sprint4.png" width="500">
<img src="db\reply_modelo_db\src\relational_model_db_sprint4.png" width="500">
---

## 📁 Estrutura do Repositório

O projeto está organizado na seguinte estrutura de pastas, conforme os requisitos da entrega:

```
Enterprise-Challenge---Sprint-4---Reply/
│── .env                        # Variáveis de ambiente
│── .gitignore                  # Arquivos/pastas ignorados no Git
│── .gitkeep                    # Placeholder para manter pastas vazias
│── requirements.txt            # Dependências Python
│── README.md                   # Documentação principal
│── app.py                      # Script principal em Python
│── dl_settings.xml             # Configurações do Data Layer
│── script_db_sprint4.ddl       # Script de criação do banco de dados
│── reply_modelo_db.dmd         # Metadados do modelo de banco
│── logical_model_db_sprint4.png# Diagrama lógico do BD
│── relational_model_db_sprint4.png # Diagrama relacional do BD
│── logo-fiap.png               # Logo utilizada no projeto
│
├── assets/                     # Recursos estáticos
│   └── logo-fiap.png
│
├── dashboard/                  # Dashboards e visualizações
│   └── ...
│
├── data/                       # Dados do projeto
│   ├── dataset_teste.csv
│   ├── raw/                    # Dados brutos
│   └── processed/              # Dados tratados
│
├── db/                         # Scripts e schemas de banco
│   └── ...
│
├── reply_modelo_db/            # Estrutura de metadados e modelos de BD
│   ├── businessinfo/
│   ├── datatypes/
│   ├── domains/
│   ├── logical/                # Entidades, relações e subviews
│   ├── mapping/                # Mapeamentos e versões de entidades
│   ├── pm/                     # Process models
│   ├── rdbms/                  # Configs de banco relacional
│   └── rel/                    # Chaves estrangeiras e tabelas
│
├── mapping/                    # Mapeamentos auxiliares
│   └── ...
│
├── pdm/                        # Physical Data Model
│   └── ...
│
├── rdbms/                      # Definições específicas de SGBD
│   └── ...
│
├── rel/                        # Relacionamentos adicionais
│   └── ...
│
├── src/                        # Código-fonte principal
│   ├── _init_.py
│   ├── preprocessing/          # Pré-processamento de dados
│   ├── models/                 # Modelos de ML/IA
│   ├── utils/                  # Funções utilitárias
│   └── visualization/          # Visualizações e gráficos
│
├── tests/                      # Testes unitários
│   └── test_app.py
│
├── docs/                       # Documentação técnica
│   └── arquitetura.md
│
├── document/                   # Documentos adicionais
│   └── ...
│
├── fireguard_api/              # Projeto Django (API Backend)
│   ├── .venv/                  # Ambiente virtual Python
│   ├── db.sqlite3              # Banco local SQLite
│   ├── manage.py               # Utilitário Django
│   ├── fireguard/              # Configuração principal Django
│   │   ├── settings.py         # Configurações globais
│   │   ├── urls.py             # Rotas globais
│   │   ├── wsgi.py / asgi.py   # Configuração servidor
│   │   └── _init_.py
│   └── sensors/                # App Django para sensores
│       ├── models.py           # Modelos do banco
│       ├── views.py            # Views/API REST
│       ├── serializers.py      # Serializadores (DRF)
│       ├── urls.py             # Rotas da app
│       ├── tests.py            # Testes unitários
│       ├── admin.py            # Configuração no Django Admin
│       └── apps.py             # Registro da app
│
└── fireguard-sensor/           # Projeto IoT (PlatformIO/Wokwi + ML)
    │── .pio/                   # Arquivos gerados pelo PlatformIO
    │── .vscode/                # Configurações do VSCode
    │── src/                    # Código C++/Arduino do microcontrolador
    │── diagram.json            # Diagrama de hardware (Wokwi)
    │── platformio.ini          # Configuração PlatformIO
    │── wokwi.toml              # Configuração simulação Wokwi
    │
    ├── ingest/                 # Ingestão de dados de sensores
    │   ├── config_mqtt/        # Configuração do MQTT
    │   ├── ESP32/              # Scripts para ESP32
    │   ├── consumer.py         # Consumidor de mensagens MQTT
    │   ├── plot_series.py      # Plotagem de séries temporais
    │   ├── sample_data.csv     # Dados de amostra
    │   ├── v1.json             # Configuração de versão
    │   └── wokwi_monitor_serial.png # Monitor serial da simulação
    │
    ├── ml/                     # Modelos de ML embarcados
    │   ├── models_preditivo/
    │   │   ├── modelo_falha_decision_tree.pkl
    │   │   ├── modelo_falha_knn.pkl
    │   │   └── scaler_falha.pkl
    │   ├── dataset_tratado.csv
    │   └── modelo_preditivo.ipynb
    │
    └── src/                    # (Duplicata) Código adicional
```

---

## 🔧 Ferramentas e Tecnologias

* **Simulação do Sensor:** Wokwi com ESP32 (DHT22)
* **Banco de Dados:** [Preencher com o SGBD escolhido, ex: PostgreSQL, MySQL]
* **Machine Learning:** Python com Scikit-learn, Pandas
* **Dashboard:** Streamlit
* **Versionamento:** Git e GitHub

---

## 🚀 Como Executar o Pipeline Completo

Siga os passos abaixo para configurar e executar o projeto em um ambiente local.

**Pré-requisitos:**
* Python 3.8+
* Git
* [Listar outros, como o SGBD que vocês usaram]

**1. Clone o Repositório:**
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

**2. Simulação e Coleta de Dados:**
A fonte de dados é um sensor de temperatura DHT22 simulado em um ESP32 no Wokwi. As instruções detalhadas estão no [README da Ingestão](/ingest/esp32/README.md). Os dados brutos gerados para este projeto estão disponíveis em `/ingest/sample_data.csv`.

**3. Configuração do Banco de Dados:**
Primeiro, execute o script para criar as tabelas no seu banco de dados.
```bash
# Exemplo de comando para executar o script SQL
psql -U seu_usuario -d seu_banco < db/schema.sql
```
Em seguida, execute o script Python para carregar os dados do arquivo CSV para o banco.
```bash
# Pode ser necessário instalar dependências antes
pip install -r requirements.txt 
python db/carga_dados.py
```

**4. Treinamento do Modelo de Machine Learning:**
O modelo de ML é treinado e avaliado em um Jupyter Notebook. Abra e execute todas as células do arquivo `/ml/treinamento_modelo.ipynb` para treinar o modelo com os dados do banco.

**5. Visualização no Dashboard:**
Para iniciar o dashboard interativo, execute a aplicação Streamlit:
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```
Acesse o endereço local informado no terminal para visualizar os KPIs e o sistema de alertas.

## Gráfico da série temporal do sensor

Para gerar o gráfico estático da série temporal (linhas bruta, média móvel e threshold):

```
python ingest/plot_timeseries.py
```
o resultado sera salvo em:
[grafico timeseries](docs\screenshots\sensor_timeseries.png)

---

## 🎬 Vídeo Demonstrativo

Uma demonstração completa do pipeline em funcionamento, desde a geração de dados até o alerta no dashboard, está disponível no link abaixo:

**[➡️ Link para o seu vídeo de até 5 minutos no YouTube (não listado) aqui]**

---

## 📋 Licença

Este projeto está licenciado sob a Licença de Atribuição 4.0 International Creative Commons. Veja a `LICENSE` para mais detalhes.
