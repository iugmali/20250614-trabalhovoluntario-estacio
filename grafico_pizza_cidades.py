#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv('z_raw_data_active.csv')

# Contar o número de ocorrências de cada cidade
contagem_cidades = df['cidade'].value_counts()

# Configurar o gráfico de pizza
plt.figure(figsize=(12, 8))
plt.pie(contagem_cidades.values, labels=contagem_cidades.index, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')  # Para garantir que o gráfico seja um círculo
plt.title('Distribuição de Usuários por Cidade')

# Adicionar legenda se houver muitas cidades
if len(contagem_cidades) > 5:
    plt.legend(contagem_cidades.index, loc="best", bbox_to_anchor=(1, 0.5))

# Salvar o gráfico como arquivo de imagem
plt.savefig('grafico_pizza_cidades.png', bbox_inches='tight')

# Exibir o gráfico na tela
plt.show()

# Imprimir estatísticas
print("Distribuição de usuários por cidade:")
print(contagem_cidades)
