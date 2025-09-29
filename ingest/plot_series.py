import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminhos
DATA_PATH = Path("ingest/sample_data.csv")
OUTPUT_PATH = Path("docs/screenshots/sensor_timeseries.png")

# Parâmetros
ROLLING_WINDOW = 12   # pontos
THRESHOLD = 60.0

def main():

    print("Iniciando execução...")
    print(f"Arquivo existe? {DATA_PATH.exists()}")
    if not DATA_PATH.exists():
        print(f"Arquivo de dados não encontrado: {DATA_PATH}")
        return
    
    
    
    # Carregar dados
    df = pd.read_csv(DATA_PATH)  # colunas esperadas: sensor_id, ts, value
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Criar figura
    plt.figure(figsize=(12, 4))

    # Série bruta
    plt.plot(df['timestamp'], df['value'], label='raw', linewidth=0.8)

    # Rolling mean
    df['rolling_mean'] = df['value'].rolling(window=ROLLING_WINDOW).mean()
    plt.plot(df['timestamp'], df['rolling_mean'], label=f'rolling_mean({ROLLING_WINDOW})')

    # Linha de threshold
    plt.axhline(THRESHOLD, color='r', linestyle='--', label=f'threshold={THRESHOLD}')

    # Formatação
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Sensor - Série Temporal')
    plt.legend()
    plt.tight_layout()

    # Criar pasta de saída se não existir
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Salvar imagem
    plt.savefig(OUTPUT_PATH, dpi=200)
    print(f"Gráfico salvo em {OUTPUT_PATH.resolve()}")

    # Mostrar (opcional)
    plt.show()

if __name__ == "__main__":
    main()
