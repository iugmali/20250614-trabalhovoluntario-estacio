#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def carregar_dados():
    """Carrega os dados do arquivo CSV de usuários ativos"""
    print("Carregando dados do arquivo z_raw_data_active.csv...")

    try:
        # Verificar se o arquivo existe
        if not os.path.exists('z_raw_data_active.csv'):
            print("ERRO: Arquivo z_raw_data_active.csv não encontrado!")
            return None

        # Identificar os nomes das colunas - sabemos que o tipo_plano é o 13º campo
        colunas = [
            'login', 'nome_completo', 'razao_social', 'endereco', 'bairro',
            'cidade', 'estado', 'cep', 'telefone1', 'telefone2',
            'data_cadastro', 'data_nascimento', 'tipo_plano', 'forma_pagamento',
            'cartao', 'validade_cartao', 'titular_cartao', 'campo17', 'campo18', 'senha',
            'cpf_cnpj', 'campo21', 'campo22', 'observacoes', 'campo24', 'campo25', 'campo26', 'col_0'
        ]

        # Carregar o CSV
        df = pd.read_csv('z_raw_data_active.csv', names=colunas, header=None)
        print(f"Total de registros carregados: {len(df)}")

        return df
    except Exception as e:
        print(f"ERRO ao carregar os dados: {str(e)}")
        return None

def analisar_tipos_plano(df):
    """Analisa a distribuição dos tipos de plano"""
    print("Analisando distribuição por tipo de plano...")

    # Verificar se a coluna existe
    if 'tipo_plano' not in df.columns:
        print("ERRO: Coluna 'tipo_plano' não encontrada!")
        return None

    # Contar a quantidade de cada tipo de plano
    contagem_planos = df['tipo_plano'].value_counts()

    # Substituir valores vazios por "Não informado"
    if '' in contagem_planos.index:
        contagem_planos = contagem_planos.rename({'': 'Não informado'})

    # Se houver NaN, renomear para "Não informado"
    if pd.isna(contagem_planos.index).any():
        contagem_planos = contagem_planos.rename({np.nan: 'Não informado'})

    print("Distribuição de usuários ativos por tipo de plano:")
    print(contagem_planos)

    return contagem_planos

def gerar_grafico_pizza(contagem_planos):
    """Gera um gráfico de pizza da distribuição por tipo de plano"""
    print("Gerando gráfico de pizza para tipos de plano...")

    # Definir cores para o gráfico
    cores = plt.cm.tab20.colors

    # Configurar o gráfico
    plt.figure(figsize=(12, 8))

    # Se houver muitos tipos de plano, agrupar os menores
    if len(contagem_planos) > 10:
        # Ordenar por frequência
        contagem_ordenada = contagem_planos.sort_values(ascending=False)

        # Pegar os 9 maiores e agrupar o restante como "Outros"
        principais = contagem_ordenada.head(9)
        outros = pd.Series({'Outros': contagem_ordenada[9:].sum()})
        contagem_final = pd.concat([principais, outros])
    else:
        contagem_final = contagem_planos

    # Gerar o gráfico
    patches, texts, autotexts = plt.pie(
        contagem_final,
        labels=contagem_final.index,
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        colors=cores[:len(contagem_final)],
        explode=[0.05] * len(contagem_final)  # Destacar ligeiramente cada fatia
    )

    # Melhorar a formatação dos textos
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color('white')

    plt.axis('equal')  # Para garantir que o gráfico seja circular
    plt.title('Distribuição de Usuários Ativos por Tipo de Plano', fontsize=16)

    # Adicionar legenda com valores absolutos
    valores_absolutos = [f"{plano}: {valor} usuários" for plano, valor in contagem_final.items()]
    plt.legend(valores_absolutos, loc="best", bbox_to_anchor=(1, 0.5), fontsize=10)

    # Salvar o gráfico
    plt.tight_layout()
    plt.savefig('grafico_tipo_plano.png')
    print("Gráfico salvo como 'grafico_tipo_plano.png'")

    # Mostrar o gráfico
    plt.show()

def main():
    print("Iniciando análise de distribuição por tipo de plano...")

    # Carregar dados
    df = carregar_dados()
    if df is None:
        print("Não foi possível carregar os dados. Encerrando.")
        return

    # Analisar tipos de plano
    contagem_planos = analisar_tipos_plano(df)
    if contagem_planos is None:
        print("Não foi possível analisar os tipos de plano. Encerrando.")
        return

    # Gerar gráfico
    gerar_grafico_pizza(contagem_planos)

    print("Análise concluída!")

if __name__ == "__main__":
    main()
