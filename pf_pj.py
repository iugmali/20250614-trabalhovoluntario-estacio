#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Define os nomes das colunas baseados na análise do arquivo
colunas = [
    'login', 'nome_completo', 'razao_social', 'endereco', 'bairro',
    'cidade', 'estado', 'cep', 'telefone1', 'telefone2',
    'data_cadastro', 'data_nascimento', 'tipo_plano', 'forma_pagamento',
    'cartao', 'validade_cartao', 'titular_cartao', 'campo17', 'campo18', 'senha',
    'cpf_cnpj', 'campo21', 'campo22', 'observacoes', 'campo24', 'campo25', 'campo26'
]

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

def classificar_pf_pj(df):
    """Classifica os registros como PF ou PJ com base no CPF/CNPJ"""
    try:
        print("Classificando registros como PF ou PJ...")

        # Verificar se a coluna existe
        if 'cpf_cnpj' not in df.columns:
            print("AVISO: Coluna 'cpf_cnpj' não encontrada. Tentando adivinhar coluna correta...")
            # Tenta encontrar coluna que pode conter CPF/CNPJ
            for col in df.columns:
                # Amostra de valores para verificação
                sample = df[col].dropna().astype(str).head(10)
                has_cpf_cnpj = any(len(val.replace('-', '').replace('/', '').replace('.', '').strip()) >= 11
                                for val in sample)
                if has_cpf_cnpj:
                    print(f"Usando coluna '{col}' como CPF/CNPJ")
                    df['cpf_cnpj'] = df[col]
                    break
            else:
                print("ERRO: Não foi possível encontrar coluna com CPF/CNPJ")
                return df

        # Limpar os dados - remover caracteres não numéricos
        df['cpf_cnpj_limpo'] = df['cpf_cnpj'].astype(str).str.replace(r'[^0-9]', '', regex=True)

        # Exibe alguns valores para verificação
        print("Amostra de CPF/CNPJ após limpeza:")
        print(df['cpf_cnpj_limpo'].head())

        # Classificar como PF ou PJ
        def tipo_pessoa(cpf_cnpj):
            if pd.isna(cpf_cnpj) or not cpf_cnpj or cpf_cnpj == 'nan':
                return 'Não informado'
            cpf_cnpj = str(cpf_cnpj).strip()
            if len(cpf_cnpj) == 11:
                return 'PF'
            elif len(cpf_cnpj) == 14:
                return 'PJ'
            else:
                return 'Formato inválido'

        df['tipo_pessoa'] = df['cpf_cnpj_limpo'].apply(tipo_pessoa)

        # Exibe contagem de cada tipo
        print("Resultado da classificação:")
        print(df['tipo_pessoa'].value_counts())

        return df
    except Exception as e:
        print(f"ERRO na classificação: {str(e)}")
        return df

def gerar_grafico_pizza(df):
    """Gera um gráfico de pizza da proporção PF/PJ"""
    try:
        print("Gerando gráfico de pizza da proporção PF/PJ...")

        if 'tipo_pessoa' not in df.columns:
            print("ERRO: Classificação PF/PJ não realizada!")
            return

        # Contar os registros por tipo de pessoa
        contagem = df['tipo_pessoa'].value_counts()

        # Exibe os valores
        print("Distribuição para o gráfico:")
        print(contagem)

        # Configurar o gráfico
        plt.figure(figsize=(10, 6))
        plt.pie(contagem, labels=contagem.index, autopct='%1.1f%%', startangle=90, shadow=True)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Proporção de Pessoas Físicas e Jurídicas')

        # Salvar o gráfico
        plt.savefig('grafico_pf_pj_ativos.png')
        print("Gráfico salvo como 'grafico_pf_pj_ativos.png'")

    except Exception as e:
        print(f"ERRO ao gerar gráfico: {str(e)}")

def main():
    print("Iniciando análise de dados...")
    print(f"Diretório de trabalho: {os.getcwd()}")

    # Converter para CSV
    df = carregar_dados()

    # Classificar PF/PJ
    df = classificar_pf_pj(df)

    # Informações sobre o dataset após a classificação
    print("\nInformações gerais do dataset:")
    print(f"Total de registros: {len(df)}")

    # Gerar gráfico
    gerar_grafico_pizza(df)

    print("Análise concluída!")

if __name__ == "__main__":
    main()
