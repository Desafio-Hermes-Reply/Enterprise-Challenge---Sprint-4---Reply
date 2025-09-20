# Enterprise Challenge - Sprint 4 - Reply

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="https://i.imgur.com/2jMLsTa.png" alt="FIAP" width="300">
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

![Arquitetura da Solução](docs/arquitetura/arquitetura-final.png)

*O arquivo editável do diagrama (`.drawio`) está disponível no diretório `/docs/arquitetura/`.*

---

## 📁 Estrutura do Repositório

O projeto está organizado na seguinte estrutura de pastas, conforme os requisitos da entrega:

```
.
├── docs/
│   └── arquitetura/      # Diagrama da arquitetura da solução
├── ingest/               # Código e dados da simulação do sensor ESP32
├── db/                   # Scripts SQL para criação e carga do banco de dados
├── ml/                   # Notebook com o treinamento e avaliação do modelo de ML
├── dashboard/            # Aplicação do dashboard com KPIs e alertas
└── README.md             # Este arquivo
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

---

## 🎬 Vídeo Demonstrativo

Uma demonstração completa do pipeline em funcionamento, desde a geração de dados até o alerta no dashboard, está disponível no link abaixo:

**[➡️ Link para o seu vídeo de até 5 minutos no YouTube (não listado) aqui]**

---

## 📋 Licença

Este projeto está licenciado sob a Licença de Atribuição 4.0 International Creative Commons. Veja a `LICENSE` para mais detalhes.
