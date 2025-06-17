# DGT0229 - Análise de Dados
### Trabalho voluntário realizado em 16/06/2025 para a empresa CentroIn Internet Provider
***Guilherme Pinto Lima de Almeida (202401455181 - Ciência da Computação - Estácio)***


#### Overview:
Dos 15.287 logins registrados no banco de dados, 11.304 (aprox. 73,9%) pertencem a pessoas físicas, 3.475 (aprox. 22,7%) a pessoas jurídicas, e 508 (aprox. 3,3%) não tiveram o dado informado. Desse total, apenas 777 logins estão ativos. Dentre os logins ativos, 681 (aprox. 87,5%) são de pessoas físicas, enquanto 80 (aprox. 10,3%) pertencem a pessoas jurídicas, e 16 (aprox. 2,1%) não tiveram o dado informado.

#### Insights:
Utilizando o modelo de IA Claude Sonnet 3.7 Thinking, fiz uma análise considerando principalmente o campos de observações dos logins, e o modelo chegou a seguinte conclusão: 
```
Contas e Planos:

- Total de aproximadamente 100 contas registradas
- Principais planos: Virtua pl G, Virtua pl C, Webmail Gold e Webmail Silver
- 15 contas "pop gratuitas" associadas a pacotes Virtua

Mudanças de Plano:

- 7 clientes migraram para planos Gold Mensal/Webmail Gold Mensal
- 2 clientes passaram de Gold para Silver
- 1 conta está hibernando por inatividade

Alterações de Forma de Pagamento:

- 9 clientes alteraram entre cartões de crédito (Visa/Mastercard/American Express)
- 3 clientes migraram de cartão de crédito para boleto
- 5 clientes fizeram o caminho inverso (boleto para cartão)

Localização:

- Maioria dos clientes no Rio de Janeiro (principalmente Zona Sul)
- Pequena parcela em outras cidades (Niterói, São Paulo, Porto Alegre)
```

#### Distribuição por tipo de plano (usuários ativos):
- Plano M: 162 logins (o mais popular)
- Plano X: 148 logins
- Plano G: 136 logins
- Plano W: 84 logins
- Plano C: 64 logins
- Plano H: 48 logins
- Plano Z: 38 logins
- Plano O: 35 logins
- Plano N: 16 logins
- Plano P: 10 logins
- Outros planos (S, E, R, F, B, T): com menos de 10 logins cada

#### Análise completa:
A análise completa dos dados foi realizada utilizando Python e as bibliotecas Pandas e Matplotlib. O código utilizado para a análise está disponível no repositório do GitHub. O arquivo final da análise é analise_dados.pptx.
