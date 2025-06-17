import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from pandas import DataFrame

# Definir a data atual
data_atual = datetime(2025, 6, 17)

# Ler o arquivo CSV
df = pd.read_csv('z_raw_data_active.csv')

# Converter a coluna de data_nascimento para datetime
# O formato parece ser DD/MM/YYYY
df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], format='%d/%m/%Y', errors='coerce')

# Filtrar apenas as linhas onde data_nascimento não é nula
df_filtrado: DataFrame = df.dropna(subset=['data_nascimento'])

# Calcular a idade em anos
df_filtrado['idade'] = ((data_atual - df_filtrado['data_nascimento']).dt.days / 365.25).astype(int)

# Criar faixas etárias
faixas_etarias = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
labels = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100+']

df_filtrado['faixa_etaria'] = pd.cut(df_filtrado['idade'], bins=faixas_etarias, labels=labels, right=False)

# Calcular a distribuição de frequência
distribuicao = df_filtrado['faixa_etaria'].value_counts().sort_index()

# Calcular estatísticas básicas
estatisticas = df_filtrado['idade'].describe()

# Exibir resultados
print("Distribuição de frequência por faixa etária:")
print(distribuicao)
print("\nEstatísticas da idade:")
print(estatisticas)

# Criar gráfico de barras para visualização
plt.figure(figsize=(12, 6))
distribuicao.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribuição de Frequência por Faixa Etária', fontsize=14)
plt.xlabel('Faixa Etária', fontsize=12)
plt.ylabel('Quantidade de Clientes', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(distribuicao):
    plt.text(i, v + 0.1, str(v), ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('distribuicao_idade.png')
plt.show()

# Salvar os resultados em um arquivo de texto
with open('estatisticas_idade.txt', 'w') as f:
    f.write("Distribuição de frequência por faixa etária:\n")
    f.write(str(distribuicao))
    f.write("\n\nEstatísticas da idade:\n")
    f.write(str(estatisticas))
    f.write(f"\n\nTotal de clientes com data de nascimento válida: {len(df_filtrado)}")
    f.write(f"\nTotal de clientes sem data de nascimento: {len(df) - len(df_filtrado)}")
