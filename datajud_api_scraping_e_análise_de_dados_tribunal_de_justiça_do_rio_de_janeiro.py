"""Datajud API - Scraping e Análise de Dados - Tribunal de Justiça do Rio de Janeiro.ipynb
https://colab.research.google.com/drive/19_uscmevykJNaBsNz7ocm2EAfWWkClzi
# Casos ajuizados Tribunal de Justiça do Rio de Janeiro
# Tiago Cupertino
"""

import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
api_key = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

payload = json.dumps({
  "size": 10000,
  "sort": [{"dataAjuizamento": {"order": "desc"}}]
})

headers = {
  'Authorization': api_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
dados_dict = response.json()
print(len(dados_dict))

display(dados_dict['hits']['hits'])

processos = []

for processo in dados_dict['hits']['hits']:
  numero_processo = processo['_source']['numeroProcesso']
  grau = processo['_source']['grau']
  classe = processo['_source']['classe']['nome']
  assuntos = processo['_source']['assuntos']
  data_ajuizamento = processo['_source']['dataAjuizamento']
  ultima_atualizacao = processo['_source']['dataHoraUltimaAtualizacao']
  formato = processo['_source']['formato']['nome']
  codigo = processo['_source']['orgaoJulgador']['codigo']
  orgao_julgador = processo['_source']['orgaoJulgador']['nome']
  municipio = processo['_source']['orgaoJulgador']['codigoMunicipioIBGE']
  sort = processo['sort'][0]
  try:
    movimentos = processo['_source']['movimentos']
  except:
    movimentos = []

  processos.append([numero_processo, classe, data_ajuizamento, ultima_atualizacao, formato, \
                    codigo, orgao_julgador, municipio, grau, assuntos, movimentos, sort])

df = pd.DataFrame(processos, columns=['numero_processo', 'classe', 'data_ajuizamento', 'ultima_atualizacao', \
                      'formato', 'codigo', 'orgao_julgador', 'municipio', 'grau', 'assuntos', 'movimentos', 'sort'])

df.sample(10)

def converte_data(data_str):
    return pd.to_datetime(data_str).tz_convert('America/Sao_Paulo')


def gera_lista_assuntos(assuntos_do_df):
    lst_assuntos=[]
    for assunto in assuntos_do_df:
        try:
            lst_assuntos.append(assunto.get('nome'))
        except:
            lst_assuntos.append('')

    return lst_assuntos


def gera_lista_movimentos(movimentos):
    lst_movimentos_final =[]
    for movimento in movimentos:
        codigo = movimento.get('codigo')
        nome = movimento.get('nome')
        data_hora = movimento.get('dataHora')
        if data_hora:
            data_hora = converte_data(data_hora)
        lst_movimentos_final.append([codigo, nome, data_hora])
    return lst_movimentos_final

df['assuntos'] = df['assuntos'].apply(gera_lista_assuntos)
df['movimentos'] = df['movimentos'].apply(gera_lista_movimentos)
df['data_ajuizamento'] = df['data_ajuizamento'].apply(converte_data)
df['ultima_atualizacao'] = df['ultima_atualizacao'].apply(converte_data)
df['movimentos']= df['movimentos'].apply(lambda x: sorted(x, key=lambda tup: tup[2], reverse=False))
df.sample(10)

df.to_csv('casos.csv', sep=',', header=True, index=False)

with open('movimentos.txt', 'w') as file:
    for index, row in df.iterrows():
        file.write(f"Autos n. {row['numero_processo']}, Classe: {row['classe']}\n")
        file.write(f"Ajuizamento: {row['data_ajuizamento']}\n")
        file.write(f"Assuntos: {row['assuntos']}\n\n")
        for movimento in row['movimentos']:
            file.write(f"{str(movimento[2])} | Cód: {str(movimento[0])} | Mov.: {movimento[1]} \n")
        file.write('\n-----------------------------------------------------------------------------\n\n')

"""# Análises"""

df.info()

df['assuntos'].value_counts()

df.columns

contagem = df['data_ajuizamento'].dt.hour.value_counts().sort_index()
plt.figure(figsize=(12, 6))
contagem.plot(kind='bar', color='skyblue')
plt.title('Horário de ajuizamento dos casos')
plt.xlabel('Hora')
plt.ylabel('Número de ajuizamentos')
plt.grid(axis='y', alpha=0.8)
plt.savefig('horario_casos.jpg')
plt.show()

display(contagem[8:19])
ajuizamentos_expediente = contagem[8:19].sum()
ajuizamentos_expediente

display(contagem[0:8])
display(contagem[19:])
ajuizamentos_fora = contagem[0:8].sum() + contagem[19:].sum()
ajuizamentos_fora

labels = ['Das 9h às 19h', 'Fora do expediente']

sizes = [ajuizamentos_expediente, ajuizamentos_fora]

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', startangle=45)

plt.title('Ajuizamento de casos pelo Tribunal de Justiça do Estado do RJ')

plt.axis('equal')
plt.savefig('pizza.jpg')
plt.show()