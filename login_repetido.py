import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('z_raw_data.csv')

# Verificar se existem logins repetidos
duplicados = df['login'].duplicated().any()

if duplicados:
    # Contagem de ocorrências de cada login
    contagem_login = df['login'].value_counts()
    # Filtrar apenas os logins que aparecem mais de uma vez
    logins_repetidos = contagem_login[contagem_login > 1]

    print(f"Existem {len(logins_repetidos)} logins repetidos no arquivo:")
    print(logins_repetidos)
else:
    print("Não existem logins repetidos no arquivo.")

# Opcional: mostrar os registros completos de logins duplicados
if duplicados:
    print("\nRegistros com logins repetidos:")
    for login in logins_repetidos.index:
        print(f"\nLogin: {login}")
        print(df[df['login'] == login])