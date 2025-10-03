# dashboard/app.py
import os
from datetime import timedelta
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Dashboard de Sensores e Modelo", layout="wide")

# --------------------------
# Funções auxiliares
# --------------------------
@st.cache_data
def load_data():
    candidates = [
        'ingest/sample_data.csv',
        #"data/dataset_teste.csv",
        #"data/sample_adjusted.csv",
        #"data/sample.csv",
        #"dashboard/data/dataset_teste.csv",
        #"dashboard/data/sample_adjusted.csv",
        #"dashboard/data/sample.csv",
    ]
    for p in candidates:
        if os.path.exists(p):
            df = pd.read_csv(p)
            if "timestamp" not in df.columns:
                continue
            df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)
            return df, p
    return None, None

def filter_data(df, start_date, end_date):
    end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    start_dt = pd.to_datetime(start_date)
    return df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)].copy()

# --------------------------
# Carregar dados
# --------------------------
df, used_path = load_data()
if df is None:
    st.error("Nenhum arquivo encontrado.")
    st.stop()

st.success(f"Arquivo carregado: `{used_path}`")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric_cols:
    st.error("Nenhuma coluna numérica encontrada.")
    st.stop()

# Detectar coluna padrão
if "sensor_value" in df.columns:
    default_sensor = "sensor_value"
elif "temperatura" in df.columns:
    default_sensor = "temperatura"
else:
    default_sensor = numeric_cols[0]

sensor_col = st.selectbox("Escolha a variável/sensor", numeric_cols, index=numeric_cols.index(default_sensor))

# Detectar coluna de previsão (se houver)
pred_col = "predicted_value" if "predicted_value" in df.columns else None

# --------------------------
# Filtro de datas
# --------------------------
min_date, max_date = df["timestamp"].dt.date.min(), df["timestamp"].dt.date.max()
date_range = st.date_input("Selecione o intervalo de datas", [min_date, max_date], min_value=min_date, max_value=max_date)
df_filtered = filter_data(df, date_range[0], date_range[1])

# --------------------------
# Threshold
# --------------------------
min_val, max_val = float(df[sensor_col].min()), float(df[sensor_col].max())
threshold = st.slider("Threshold de alerta", min_val, max_val, float(min_val + 0.85*(max_val - min_val)))

# --------------------------
# KPIs (3 principais)
# --------------------------
col1, col2, col3 = st.columns(3)

mean_val = df_filtered[sensor_col].mean() if not df_filtered.empty else np.nan
max_val_f = df_filtered[sensor_col].max() if not df_filtered.empty else np.nan
alerts_24h = df_filtered[
    (df_filtered["timestamp"] >= (df_filtered["timestamp"].max() - pd.Timedelta(days=1))) &
    (df_filtered[sensor_col] > threshold)
].shape[0]

col1.metric("Média (período)", f"{mean_val:.2f}" if not np.isnan(mean_val) else "-")
col2.metric("Máximo", f"{max_val_f:.2f}" if not np.isnan(max_val_f) else "-")
col3.metric("Alertas (24h)", str(alerts_24h))

st.markdown("---")

# --------------------------
# Velocímetro em tempo real
# --------------------------
if not df_filtered.empty:
    current_value = df_filtered[sensor_col].iloc[-1]
else:
    current_value = 0

max_range = float(df[sensor_col].max())
green_zone = threshold * 0.7
yellow_zone = threshold

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=current_value,
    title={'text': f"Nível atual: {sensor_col}"},
    gauge={
        'axis': {'range': [0, max_range]},
        'steps': [
            {'range': [0, green_zone], 'color': "lightgreen"},
            {'range': [green_zone, yellow_zone], 'color': "yellow"},
            {'range': [yellow_zone, max_range], 'color': "red"},
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': threshold
        }
    }
))

st.subheader("Velocímetro do Sensor")
st.plotly_chart(fig_gauge, use_container_width=True)

# Atualização automática a cada 5 segundos
st_autorefresh(interval=5000, key="datarefresh")

# --------------------------
# Gráfico principal
# --------------------------
with st.expander("Opções do gráfico"):
    apply_smooth = st.checkbox("Aplicar média móvel", value=False)
    window = st.slider("Janela da média móvel", 1, 51, 5) if apply_smooth else 1

plot_df = df_filtered.sort_values("timestamp")
if apply_smooth and window > 1:
    plot_df[f"{sensor_col}_smooth"] = plot_df[sensor_col].rolling(window, min_periods=1, center=True).mean()
    y_cols = [f"{sensor_col}_smooth"]
else:
    y_cols = [sensor_col]

fig = px.line(plot_df, x="timestamp", y=y_cols, labels={"value": "Valor", "timestamp": "Tempo"}, title=f"Série Temporal - {sensor_col}")
fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text=f"Threshold = {threshold:.2f}")
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Distribuição dos valores
# --------------------------
st.subheader("Distribuição dos valores")
fig_hist = px.histogram(df_filtered, x=sensor_col, nbins=30, title="Histograma")
st.plotly_chart(fig_hist, use_container_width=True)

# --------------------------
# Correlação entre variáveis
# --------------------------
st.subheader("Correlação entre variáveis")
if len(numeric_cols) > 1:
    corr = df_filtered[numeric_cols].corr()
    fig_corr = px.imshow(corr, text_auto=True, title="Matriz de Correlação")
    st.plotly_chart(fig_corr, use_container_width=True)

# --------------------------
# Log de alertas
# --------------------------
mask_alert = df_filtered[sensor_col] > threshold
alert_log = df_filtered.loc[mask_alert, ["timestamp", sensor_col]].copy()
if not alert_log.empty:
    alert_log = alert_log.rename(columns={sensor_col: "valor"})
    alert_log["excesso"] = alert_log["valor"] - threshold
    alert_log["tipo"] = "Valor acima do threshold"
    st.subheader("Log de Alertas")
    st.dataframe(alert_log.sort_values("timestamp", ascending=False).reset_index(drop=True))
    csv_bytes = alert_log.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar log de alertas (CSV)", data=csv_bytes, file_name="alert_log.csv", mime="text/csv")
else:
    st.info("Sem leituras acima do threshold no intervalo selecionado.")
