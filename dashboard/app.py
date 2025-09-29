# dashboard/app.py
import os
from datetime import timedelta
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard de Sensores e Modelo", layout="wide")

# --------------------------
# Carregar dados (vários caminhos possíveis)
# --------------------------
candidates = [
    #"data/dataset_teste.csv",
    #"data/sample_adjusted.csv",
    #"data/sample.csv",
    #"dashboard/data/dataset_teste.csv",
    #"dashboard/data/sample_adjusted.csv",
    #"dashboard/data/sample.csv",
    'ingest/sample_data.csv'
]
df = None
used_path = None
for p in candidates:
    if os.path.exists(p):
        try:
            df = pd.read_csv(p)
            used_path = p
            break
        except Exception as e:
            # tenta próxima opção
            pass

if df is None:
    st.error("Nenhum arquivo de dados encontrado. Coloque `dataset_teste.csv` dentro de `dashboard/data/` ou use outro nome listado no código.")
    st.stop()

# tenta parsear timestamp
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)
else:
    st.error("Arquivo carregado não contém a coluna 'timestamp'.")
    st.stop()

# mostrar informação básica
st.write(f"Arquivo carregado: `{used_path}`")
st.write("Colunas detectadas:", df.columns.tolist())

# --------------------------
# Seleção do sensor/variável
# --------------------------
# Detecta colunas numéricas (exclui id)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [c for c in numeric_cols if c.lower() not in ("id",)]

# se existir coluna named sensor_value, prioriza
default_sensor = None
if "sensor_value" in df.columns:
    default_sensor = "sensor_value"
elif "temperatura" in df.columns:
    default_sensor = "temperatura"
elif len(numeric_cols) > 0:
    default_sensor = numeric_cols[0]

if not numeric_cols:
    st.error("Nenhuma coluna numérica encontrada para usar como sensor.")
    st.stop()

sensor_col = st.selectbox("Escolha a variável/sensor", numeric_cols, index=numeric_cols.index(default_sensor) if default_sensor in numeric_cols else 0)

# detectar coluna de previsão (opcional)
pred_col = "predicted_value" if "predicted_value" in df.columns else None
if pred_col:
    st.info(f"Coluna de previsão detectada: `{pred_col}`")

# --------------------------
# Filtro de datas
# --------------------------
min_date = df["timestamp"].dt.date.min()
max_date = df["timestamp"].dt.date.max()
date_range = st.date_input("Selecione o intervalo de datas", [min_date, max_date], min_value=min_date, max_value=max_date)

# normalizar inputs (date_input pode retornar datetimes ou date)
if isinstance(date_range, (list, tuple)):
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:
    start_date = pd.to_datetime(date_range)
    end_date = pd.to_datetime(date_range)

# incluir o dia final inteiro
end_dt = end_date + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
start_dt = start_date

df_filtered = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)].copy()
if df_filtered.empty:
    st.warning("Nenhum dado no intervalo selecionado.")
    
# --------------------------
# Threshold / Alertas
# --------------------------
col1, col2, col3, col4 = st.columns([1,1,1,1])

# threshold slider range baseado na coluna selecionada
min_val = float(df[sensor_col].min())
max_val = float(df[sensor_col].max())
default_threshold = min_val + 0.85*(max_val - min_val)
threshold = st.slider("Threshold de alerta", min_val, max_val, float(default_threshold), step=(max_val-min_val)/100)

# suavização (opcional)
with st.expander("Opções do gráfico"):
    apply_smooth = st.checkbox("Aplicar média móvel (suavizar linhas)", value=False)
    if apply_smooth:
        window = st.slider("Janela da média móvel (n pontos)", 1, 51, 5, step=1)
    else:
        window = 1

# --------------------------
# KPIs dinâmicos
# --------------------------
def format_val(x):
    try:
        return f"{x:.2f}"
    except:
        return str(x)

mean_val = df_filtered[sensor_col].mean() if not df_filtered.empty else np.nan
max_val_f = df_filtered[sensor_col].max() if not df_filtered.empty else np.nan
alerts_24h = df_filtered[(df_filtered["timestamp"] >= (end_dt - pd.Timedelta(days=1))) & (df_filtered[sensor_col] > threshold)].shape[0]

col1.metric("Média (período)", format_val(mean_val))
col2.metric("Máximo", format_val(max_val_f))
col3.metric("Alertas (24h)", f"{alerts_24h}")
if pred_col and pred_col in df_filtered.columns:
    mae = (df_filtered[sensor_col] - df_filtered[pred_col]).abs().mean()
    col4.metric("MAE do Modelo", format_val(mae))
else:
    col4.metric("MAE do Modelo", "N/A")

st.markdown("---")

# --------------------------
# Gráfico principal (Plotly)
# --------------------------
plot_df = df_filtered[["timestamp", sensor_col] + ([pred_col] if pred_col else [])].copy()
plot_df = plot_df.sort_values("timestamp")

if apply_smooth and window > 1:
    plot_df[f"{sensor_col}_smooth"] = plot_df[sensor_col].rolling(window, min_periods=1, center=True).mean()
    if pred_col:
        plot_df[f"{pred_col}_smooth"] = plot_df[pred_col].rolling(window, min_periods=1, center=True).mean()
    y_cols = [f"{sensor_col}_smooth"] + ([f"{pred_col}_smooth"] if pred_col else [])
    legend_names = {f"{sensor_col}_smooth": sensor_col, **({f"{pred_col}_smooth": pred_col} if pred_col else {})}
else:
    y_cols = [sensor_col] + ([pred_col] if pred_col else [])
    legend_names = {}

fig = px.line(plot_df, x="timestamp", y=y_cols, labels={"value":"Valor", "timestamp":"Tempo"}, title=f"{sensor_col} vs Previsão" if pred_col else f"Série Temporal - {sensor_col}")
# renomear legendas se estiver usando smooth names
if legend_names:
    for old, new in legend_names.items():
        for t in fig.data:
            if t.name == old:
                t.name = new

fig.update_layout(legend_title_text="variable", margin=dict(t=60, b=40, l=60, r=20))
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Gráfico complementar
# --------------------------

st.markdown("---")
st.subheader(" Escolha o Tipo de Visualização")

chart_type = st.radio("Tipo de gráfico", ["Interativo (Plotly)", "Estático (Matplotlib)"])

if chart_type == "Interativo (Plotly)":
    fig2 = px.line(df_filtered, x="timestamp", y=sensor_col, title="Série Temporal - Interativo")
    fig2.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text=f"Threshold = {threshold:.2f}")
    st.plotly_chart(fig2, use_container_width=True)

else:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df_filtered["timestamp"], df_filtered[sensor_col], label="Raw", linewidth=0.8)
    ax.plot(df_filtered["timestamp"], df_filtered[sensor_col].rolling(window).mean(), label=f"Rolling Mean ({window})")
    ax.axhline(threshold, color='r', linestyle='--', label=f'Threshold = {threshold:.2f}')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Valor")
    ax.set_title("Sensor - Série Temporal (Estático)")
    ax.legend()
    st.pyplot(fig)


# --------------------------
# Widget de alerta visual + log
# --------------------------
mask_alert = df_filtered[sensor_col] > threshold
if mask_alert.any():
    n_alerts = mask_alert.sum()
    last_alert = df_filtered.loc[mask_alert].sort_values("timestamp").iloc[-1]
    st.error(f"Alerta: {n_alerts} leituras acima de {threshold:.2f}. Última: {last_alert['timestamp']} = {last_alert[sensor_col]:.2f}")

# criar log de alertas (para download)
alert_log = df_filtered.loc[mask_alert, ["timestamp", sensor_col]].copy()
if not alert_log.empty:
    alert_log = alert_log.rename(columns={sensor_col: "valor"})
    alert_log["tipo"] = "Valor acima do threshold"
    st.subheader("Log de Alertas")
    st.dataframe(alert_log.sort_values("timestamp", ascending=False).reset_index(drop=True))
    csv_bytes = alert_log.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar log de alertas (CSV)", data=csv_bytes, file_name="alert_log.csv", mime="text/csv")
else:
    st.info("Sem leituras acima do threshold no intervalo selecionado.")


