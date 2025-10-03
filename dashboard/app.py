# dashboard/app.py
import os
import json
import warnings
import requests
from datetime import timedelta
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import joblib

# =======================
# CONFIGURAÇÃO BÁSICA
# =======================
warnings.filterwarnings("ignore", category=UserWarning)
st.set_page_config(page_title="Dashboard de Sensores", layout="wide")

# =======================
# CSS customizado
# =======================
st.markdown("""
<style>
    .metric-card {
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        background-color: #f9f9f9;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        margin: 5px;
    }
    .stMetric label {
        font-size: 16px !important;
        font-weight: bold !important;
    }
    .stMetric div {
        font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# =======================
# METADADOS DOS SENSORES
# =======================
SENSOR_METADATA = {
    "dht_t": {"label": "Temperatura (DHT22)", "unit": "°C"},
    "dht_h": {"label": "Umidade (DHT22)", "unit": "%"},
    "mq2_d": {"label": "Detecção de Gás/Fumaça (MQ-2)", "unit": "0=Gás, 1=Normal"},
    "flame_d": {"label": "Detecção de Chama (Flame IR)", "unit": "0=Chama, 1=Normal"},
    "vibra_d": {"label": "Detecção de Vibração (SW-420)", "unit": "0=Vibração, 1=Normal"},
    "current_v": {"label": "Corrente (SCT-013)", "unit": "V"},
    "encoder_c": {"label": "Contagem de Pulsos (Encoder)", "unit": "pulsos"},
    "dist_cm": {"label": "Distância (HC-SR04)", "unit": "cm"},
    "current_420": {"label": "Corrente de Loop", "unit": "mA"},
    "ds_t": {"label": "Temperatura (DS18B20)", "unit": "°C"},
    "mpu_ax": {"label": "Aceleração X (MPU6050)", "unit": "m/s²"},
    "mpu_ay": {"label": "Aceleração Y (MPU6050)", "unit": "m/s²"},
    "mpu_az": {"label": "Aceleração Z (MPU6050)", "unit": "m/s²"},
    "mpu_gx": {"label": "Velocidade Angular X (MPU6050)", "unit": "rad/s"},
    "mpu_gy": {"label": "Velocidade Angular Y (MPU6050)", "unit": "rad/s"},
    "mpu_gz": {"label": "Velocidade Angular Z (MPU6050)", "unit": "rad/s"},
    "zmpt_vrms": {"label": "Tensão RMS (ZMPT101B)", "unit": "V"},
}

# =======================
# FEATURES DO MODELO
# =======================
FEATURES_ML = [
    "temperatura", "vibracao", "corrente", "pressao", "umidade",
    "tensao", "nivel", "velocidade", "posicao", "qualidade_ar", "fumaca"
]

# =======================
# FUNÇÃO DE MAPEAMENTO
# =======================
def map_api_to_model_features(api_data):
    """Mapeia dados da API para as features usadas no treinamento"""
    try:
        mapped = pd.DataFrame([{
            "temperatura": api_data.get("ds_t", api_data.get("dht_t", 0)),
            "vibracao": api_data.get("vibra_d", 0),
            "corrente": api_data.get("current_v", 0),
            "pressao": api_data.get("dist_cm", 0),  # proxy caso não haja pressão
            "umidade": api_data.get("dht_h", 0),
            "tensao": api_data.get("zmpt_vrms", 0),
            "nivel": api_data.get("encoder_c", 0),
            "velocidade": api_data.get("mpu_az", 0),
            "posicao": api_data.get("mpu_ax", 0),
            "qualidade_ar": api_data.get("mq2_d", 0),
            "fumaca": api_data.get("flame_d", 0)
        }])
        return mapped
    except Exception as e:
        st.error(f"❌ Erro no mapeamento de features: {e}")
        return None

# =======================
# FUNÇÕES AUXILIARES
# =======================
@st.cache_data
def load_data():
    """Carrega dados da API ou de CSV local como fallback"""
    url = "http://3.139.63.62:8000/api/sensors"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)
            return df, url
        else:
            st.error(f"❌ Erro ao acessar API: {response.status_code}")
    except Exception as e:
        st.warning(f"⚠️ API offline: {e}")

    # fallback CSV
    for p in ["ingest/sample_data.csv", "data/dataset_teste.csv"]:
        if os.path.exists(p):
            df = pd.read_csv(p)
            df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)
            return df, p
    return None, None


def filter_data(df, start_date, end_date):
    end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    return df[(df["timestamp"] >= pd.to_datetime(start_date)) & (df["timestamp"] <= end_dt)]


def get_last_prediction(model, scaler):
    """Obtém última leitura da API, faz mapeamento e predição"""
    url = "http://3.139.63.62:8000/api/sensors/last/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            st.error(f"❌ Erro na API: status {response.status_code}")
            return None, None

        api_data = response.json()
        df_last = pd.DataFrame([api_data])
        st.write("📥 Última leitura recebida (API):", df_last)

        # Mapeia para features esperadas
        X = map_api_to_model_features(api_data)
        if X is None:
            return None, df_last

        try:
            X_scaled = scaler.transform(X)
        except Exception as e:
            st.error(f"❌ Erro ao escalar dados: {e}")
            return None, df_last

        try:
            y_pred = model.predict(X_scaled)
            y_proba = model.predict_proba(X_scaled)[0] if hasattr(model, "predict_proba") else None
            return (y_pred[0], y_proba), df_last
        except Exception as e:
            st.error(f"❌ Erro ao prever com o modelo: {e}")
            return None, df_last

    except Exception as e:
        st.error(f"❌ Erro inesperado em get_last_prediction: {e}")
        return None, None

# =======================
# CARREGAR MODELOS
# =======================
scaler, model = None, None
try:
    scaler = joblib.load("ml/models_preditivo/scaler_falha.pkl")
    st.success("✅ Scaler carregado")
except Exception as e:
    st.error(f"❌ Erro ao carregar scaler: {e}")

model_choice = st.sidebar.selectbox("Modelo preditivo", ["KNN", "Decision Tree"])
model_path = f"ml/models_preditivo/modelo_falha_{'knn' if model_choice=='KNN' else 'decision_tree'}.pkl"

try:
    model = joblib.load(model_path)
    st.success(f"✅ Modelo carregado: {model_choice}")
except Exception as e:
    st.error(f"❌ Erro ao carregar modelo ({model_path}): {e}")

# =======================
# CARREGAR DADOS
# =======================
df, source = load_data()
if df is None:
    st.error("❌ Sem dados disponíveis")
    st.stop()
st.success(f"📡 Fonte de dados: {source}")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric_cols:
    st.error("❌ Nenhuma coluna numérica encontrada")
    st.stop()

# =======================
# DASHBOARD
# =======================
st.title("📊 Dashboard de Sensores com IA Preditiva")
st.markdown("Monitoramento em tempo real com **Machine Learning** para detecção de falhas.")

# --- Predição em tempo real
st.subheader("🔮 Predição (Última Leitura)")

if model is not None and scaler is not None:
    prediction, df_last = get_last_prediction(model, scaler)
    if prediction:
        y_pred, y_proba = prediction
        status = "⚠️ Falha Prevista" if y_pred == 1 else "✅ Normal"
        st.metric("Status", status)
        if y_proba is not None:
            st.write(f"Probabilidade Normal: {y_proba[0]:.2f} | Falha: {y_proba[1]:.2f}")
    else:
        st.info("⚠️ Não foi possível calcular a predição.")
else:
    st.error("❌ Modelo ou Scaler não carregado.")

# Botão manual de atualização
if st.button("🔄 Atualizar previsão"):
    prediction, df_last = get_last_prediction(model, scaler)
    if prediction:
        y_pred, y_proba = prediction
        status = "⚠️ Falha Prevista" if y_pred == 1 else "✅ Normal"
        st.metric("Status (Atualizado)", status)
        if y_proba is not None:
            st.write(f"Probabilidade Normal: {y_proba[0]:.2f} | Falha: {y_proba[1]:.2f}")

st.markdown("---")

# --- Filtro de sensores
sensor_label = st.selectbox("Selecione um sensor", [SENSOR_METADATA.get(c, {"label":c})["label"] for c in numeric_cols])
sensor_col = numeric_cols[[SENSOR_METADATA.get(c, {"label":c})["label"] for c in numeric_cols].index(sensor_label)]
meta = SENSOR_METADATA.get(sensor_col, {"label": sensor_col, "unit": ""})

# --- Intervalo de datas
min_date, max_date = df["timestamp"].dt.date.min(), df["timestamp"].dt.date.max()
date_range = st.date_input("Intervalo", [min_date, max_date], min_value=min_date, max_value=max_date)
df_filtered = filter_data(df, date_range[0], date_range[1])

# --- KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Média", f"{df_filtered[sensor_col].mean():.2f}{meta['unit']}")
col2.metric("Máximo", f"{df_filtered[sensor_col].max():.2f}{meta['unit']}")
col3.metric("Leituras", str(df_filtered.shape[0]))

# --- Gauge
st.subheader("Velocímetro do Sensor")
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=df_filtered[sensor_col].iloc[-1] if not df_filtered.empty else 0,
    title={'text': f"{meta['label']}"},
    gauge={'axis': {'range': [0, df[sensor_col].max()]}}
))
st.plotly_chart(fig_gauge, use_container_width=True)

# --- Gráfico temporal
st.subheader("Série Temporal")
fig = px.line(df_filtered, x="timestamp", y=sensor_col, title=f"{meta['label']} ({meta['unit']})")
st.plotly_chart(fig, use_container_width=True)

# --- Histograma
st.subheader("Distribuição")
fig_hist = px.histogram(df_filtered, x=sensor_col, nbins=30)
st.plotly_chart(fig_hist, use_container_width=True)

# --- Correlação
if len(numeric_cols) > 1:
    st.subheader("Matriz de Correlação")
    fig_corr = px.imshow(df_filtered[numeric_cols].corr(), text_auto=True)
    st.plotly_chart(fig_corr, use_container_width=True)

# --- Log de alertas
st.subheader("Log de Alertas")
threshold = df[sensor_col].mean() * 1.2
alert_log = df_filtered[df_filtered[sensor_col] > threshold][["timestamp", sensor_col]]
if not alert_log.empty:
    st.dataframe(alert_log)
    st.download_button("Baixar CSV", alert_log.to_csv(index=False), "alertas.csv", "text/csv")
else:
    st.info("Sem alertas no período.")

# Auto refresh opcional
st_autorefresh(interval=10000, key="refresh")
