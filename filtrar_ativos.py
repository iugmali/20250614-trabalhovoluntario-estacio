#!/usr/bin/env python3
import pandas as pd
import sys
import os

def extrair_logins_ativos():
    """Extrair logins do arquivo z_active_users.txt"""
    print("Extraindo logins de usuários ativos...", flush=True)
    logins_ativos = set()

    try:
        if not os.path.exists('z_active_users.txt'):
            print("ERRO: Arquivo z_active_users.txt não encontrado!", flush=True)
            sys.exit(1)

        with open('z_active_users.txt', 'r') as f:
            for linha in f:
                # Extrair o login (parte antes do primeiro ':')
                partes = linha.strip().split(':', 1)
                if partes:
                    login = partes[0]
                    logins_ativos.add(login)

        print(f"Total de logins ativos extraídos: {len(logins_ativos)}", flush=True)
        # Mostrar alguns exemplos de logins extraídos para verificação
        print(f"Exemplos de logins ativos: {list(logins_ativos)[:5]}", flush=True)
        return logins_ativos
    except Exception as e:
        print(f"ERRO ao extrair logins: {str(e)}", flush=True)
        sys.exit(1)

def filtrar_trabalho_csv(logins_ativos):
    """Filtrar z_raw_data.csv para incluir apenas logins ativos"""
    print("Carregando arquivo z_raw_data.csv...", flush=True)
    try:
        if not os.path.exists('z_raw_data.csv'):
            print("ERRO: Arquivo z_raw_data.csv não encontrado!", flush=True)
            sys.exit(1)

        # Verificar o tamanho do arquivo
        tamanho_mb = os.path.getsize('z_raw_data.csv') / (1024 * 1024)
        print(f"Tamanho do arquivo z_raw_data.csv: {tamanho_mb:.2f} MB", flush=True)

        # Carregar o CSV com todos os registros
        df = pd.read_csv('z_raw_data.csv')
        total_registros = len(df)
        print(f"Total de registros em z_raw_data.csv: {total_registros}", flush=True)

        # Verificar se a coluna login existe
        if 'login' not in df.columns:
            print(f"ERRO: Coluna 'login' não encontrada no CSV. Colunas disponíveis: {df.columns.tolist()}", flush=True)
            sys.exit(1)

        # Filtrar apenas os registros com login ativo
        df_filtrado = df[df['login'].isin(logins_ativos)]
        registros_filtrados = len(df_filtrado)
        print(f"Registros filtrados (com logins ativos): {registros_filtrados}", flush=True)
        print(f"Registros removidos: {total_registros - registros_filtrados}", flush=True)

        # Mostrar alguns registros para verificação
        print("\nPrimeiros registros filtrados:", flush=True)
        print(df_filtrado.head(2), flush=True)

        # Salvar o resultado filtrado
        df_filtrado.to_csv('z_raw_data_active.csv', index=False)
        print("\nArquivo z_raw_data_active.csv criado com sucesso!", flush=True)

        # Verificar se o arquivo foi criado
        if os.path.exists('z_raw_data_active.csv'):
            tamanho_mb = os.path.getsize('z_raw_data_active.csv') / (1024 * 1024)
            print(f"Tamanho do arquivo z_raw_data_active.csv: {tamanho_mb:.2f} MB", flush=True)
        else:
            print("ERRO: O arquivo z_raw_data_active.csv não foi criado!", flush=True)

        return registros_filtrados
    except Exception as e:
        print(f"ERRO ao processar o arquivo CSV: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        return 0

def main():
    print("Iniciando filtragem de z_raw_data.csv com base em z_active_users.txt...", flush=True)
    print(f"Diretório atual: {os.getcwd()}", flush=True)

    # Listar arquivos no diretório para verificação
    arquivos = os.listdir('.')
    print(f"Arquivos no diretório: {arquivos}", flush=True)

    # Extrair logins ativos
    logins_ativos = extrair_logins_ativos()

    # Filtrar z_raw_data.csv
    if logins_ativos:
        registros_filtrados = filtrar_trabalho_csv(logins_ativos)
        print(f"Processo concluído! {registros_filtrados} registros foram salvos em z_raw_data_active.csv", flush=True)

if __name__ == "__main__":
    main()
