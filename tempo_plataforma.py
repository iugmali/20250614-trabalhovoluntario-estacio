.4#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import sys
import os

def carregar_dados():
    """Carrega os dados do arquivo CSV"""
    try:
        print("Carregando dados do arquivo CSV...")
        # Verificar se o arquivo existe
        if not os.path.exists('z_raw_data_active.csv'):
            print(f"ERRO: Arquivo trabalho.csv não encontrado! Diretório atual: {os.getcwd()}")
            sys.exit(1)

        # Lê o arquivo CSV
        df = pd.read_csv('z_raw_data_active.csv')
        print(f"Total de registros carregados: {len(df)}")
        return df
    except Exception as e:
        print(f"ERRO ao carregar o arquivo CSV: {str(e)}")
        sys.exit(1)

def calcular_tempo_plataforma(df):
    """Calcula o tempo de plataforma para cada login"""
    try:
        print("Calculando tempo de plataforma para cada login...")

        # Verificar se a coluna de data de cadastro existe
        if 'data_cadastro' not in df.columns:
            print("ERRO: Coluna 'data_cadastro' não encontrada!")
            sys.exit(1)

        # Converter a coluna de data de cadastro para datetime
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], format='%d/%m/%Y', errors='coerce')

        # Definir a data atual (16 de junho de 2025)
        data_atual = datetime(2025, 6, 16)

        # Calcular a diferença entre a data atual e a data de cadastro em anos
        df['tempo_plataforma'] = (data_atual - df['data_cadastro']).dt.days / 365.25

        # Exibir algumas estatísticas básicas
        print("Estatísticas básicas do tempo de plataforma (em anos):")
        estatisticas = df['tempo_plataforma'].describe()
        print(estatisticas)

        # Calcular média, mediana e variância
        media = df['tempo_plataforma'].mean()
        mediana = df['tempo_plataforma'].median()
        variancia = df['tempo_plataforma'].var()
        desvio_padrao = df['tempo_plataforma'].std()

        print(f"Média: {media:.2f} anos")
        print(f"Mediana: {mediana:.2f} anos")
        print(f"Variância: {variancia:.2f}")
        print(f"Desvio Padrão: {desvio_padrao:.2f}")

        # Remover dados problemáticos para análise (NaN, negativos e outliers extremos)
        df = df.dropna(subset=['tempo_plataforma'])
        df = df[df['tempo_plataforma'] >= 0]  # remove tempos negativos, se houver

        # Agrupar em categorias de anos
        df['tempo_categoria'] = pd.cut(
            df['tempo_plataforma'],
            bins=[0, 5, 10, 15, 20, 25, 30, float('inf')],
            labels=['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30+']
        )

        return df, media, mediana, variancia, desvio_padrao
    except Exception as e:
        print(f"ERRO ao calcular tempo de plataforma: {str(e)}")
        sys.exit(1)

def analisar_distribuicao(df, media, mediana, variancia, desvio_padrao):
    """Analisa a distribuição de frequência de tempo na plataforma"""
    try:
        print("Analisando distribuição de frequência por tempo na plataforma...")

        # Calcular distribuição por categoria de tempo
        distribuicao = df['tempo_categoria'].value_counts().sort_index()
        print("\nDistribuição por categoria de tempo (anos):")
        print(distribuicao)

        # Calcular frequência de logins por ano de cadastro
        freq_por_ano = df.groupby(df['data_cadastro'].dt.year).size()
        print("\nFrequência de logins por ano de cadastro:")
        print(freq_por_ano)

        return distribuicao, freq_por_ano
    except Exception as e:
        print(f"ERRO na análise de distribuição: {str(e)}")
        return None, None

def gerar_graficos(df, distribuicao, freq_por_ano, media, mediana, variancia, desvio_padrao):
    """Gera gráficos para análise"""
    try:
        print("Gerando gráficos de análise...")

        # Configuração visual para os gráficos
        plt.style.use('ggplot')
        sns.set(font_scale=1.1)

        # 1. Histograma de distribuição de tempo na plataforma
        plt.figure(figsize=(12, 7))
        sns.histplot(df['tempo_plataforma'], bins=20, kde=True)
        plt.axvline(media, color='red', linestyle='--', label=f'Média: {media:.2f} anos')
        plt.axvline(mediana, color='green', linestyle='-', label=f'Mediana: {mediana:.2f} anos')
        plt.title('Distribuição do Tempo de Plataforma', fontsize=16)
        plt.xlabel('Tempo na Plataforma (anos)', fontsize=14)
        plt.ylabel('Número de Usuários', fontsize=14)
        plt.legend()
        plt.tight_layout()
        plt.savefig('histograma_tempo_plataforma.png')
        print("Histograma salvo como 'histograma_tempo_plataforma.png'")

        # 2. Gráfico de barras para categorias de tempo
        plt.figure(figsize=(12, 7))
        sns.barplot(x=distribuicao.index, y=distribuicao.values)
        plt.title('Distribuição por Categorias de Tempo', fontsize=16)
        plt.xlabel('Categoria de Tempo (anos)', fontsize=14)
        plt.ylabel('Número de Usuários', fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('categorias_tempo_plataforma.png')
        print("Gráfico de categorias salvo como 'categorias_tempo_plataforma.png'")

        # 3. Gráfico de linha para frequência por ano de cadastro
        plt.figure(figsize=(14, 7))
        freq_por_ano.plot(kind='line', marker='o', linewidth=2)
        plt.title('Número de Cadastros por Ano', fontsize=16)
        plt.xlabel('Ano de Cadastro', fontsize=14)
        plt.ylabel('Número de Cadastros', fontsize=14)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('cadastros_por_ano.png')
        print("Gráfico de cadastros por ano salvo como 'cadastros_por_ano.png'")

        # 4. Boxplot para visualizar a distribuição e outliers
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=df['tempo_plataforma'])
        plt.title('Boxplot do Tempo na Plataforma', fontsize=16)
        plt.xlabel('Tempo na Plataforma (anos)', fontsize=14)
        plt.tight_layout()
        plt.savefig('boxplot_tempo_plataforma.png')
        print("Boxplot salvo como 'boxplot_tempo_plataforma.png'")

        # 5. Gráfico para mostrar média, mediana, variância e desvio padrão
        plt.figure(figsize=(10, 6))
        metricas = ['Média', 'Mediana', 'Desvio Padrão']
        valores = [media, mediana, desvio_padrao]
        colors = ['#FF9999', '#66B2FF', '#99FF99']

        bars = plt.bar(metricas, valores, color=colors)
        plt.title('Métricas Estatísticas do Tempo na Plataforma', fontsize=16)
        plt.ylabel('Anos', fontsize=14)

        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=12)

        # Adicionar informação sobre variância em um texto
        plt.figtext(0.5, 0.01, f'Variância: {variancia:.2f}', ha='center', fontsize=14)

        plt.tight_layout()
        plt.savefig('metricas_estatisticas.png')
        print("Gráfico de métricas estatísticas salvo como 'metricas_estatisticas.png'")

    except Exception as e:
        print(f"ERRO ao gerar gráficos: {str(e)}")

def main():
    print("Iniciando análise de tempo na plataforma...")
    print(f"Diretório de trabalho: {os.getcwd()}")

    # Carregar dados do CSV
    df = carregar_dados()

    # Calcular tempo de plataforma
    df, media, mediana, variancia, desvio_padrao = calcular_tempo_plataforma(df)

    # Analisar distribuição de frequência
    distribuicao, freq_por_ano = analisar_distribuicao(df, media, mediana, variancia, desvio_padrao)

    # Gerar gráficos
    gerar_graficos(df, distribuicao, freq_por_ano, media, mediana, variancia, desvio_padrao)

    print("Análise concluída!")

if __name__ == "__main__":
    main()
