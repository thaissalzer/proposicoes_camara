import requests
import datetime
import pandas as pd
import streamlit as st
import schedule
import time

st.set_page_config(layout='wide')
# inserindo o titulo
st.title('Monitoramento das Proposições Legistalivas da Câmara dos Deputados')

st.text(
    "São acompanhados os PLs, PLPs, PECs e Requerimentos que apresentaram alguma tramitação nos ultimos 15 dias e no último dia")

st.text("Os temas em monitoramento são: gás natural, petróleo, energia e CDE")

st.text("TRAMITAÇÕES DE INTERESSE DOS ÚLTIMOS 15 DIA")

# Definir a URL da API para o endpoint de projetos
url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"

# Definir os parâmetros da requisição
data_inicio = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
data_fim = datetime.datetime.now().strftime("%Y-%m-%d")
params = {
    "dataInicio": data_inicio,
    "dataFim": data_fim,
    "ordenarPor": "id",
    "itens": 100,  # Quantidade de itens por página
    "pagina": 1,  # Começar pela primeira página
    "siglaTipo": ["PL", "PLP", "PEC", "REQ"],
}
# Definir as palavras-chave que deseja filtrar na ementa dos projetos
palavras_chave = ["gás natural", "petróleo",
                  "energia",
                  "CDE"]


def get_data():
    # Fazer requisições para todas as páginas de resultados
    projetos = []
    while True:
        # Fazer a requisição para a API
        response = requests.get(url, params=params)
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Acessar o conteúdo da resposta em formato JSON
            dados = response.json()["dados"]
            # Verificar se há projetos na página atual
            if len(dados) == 0:
                break
            # Filtrar os projetos que contêm pelo menos uma palavra-chave na ementa
            projetos.extend(
                [projeto for projeto in dados if any(palavra in projeto["ementa"].lower() for palavra in palavras_chave)])
            # Avançar para a próxima página
            params["pagina"] += 1
        else:
            print("Erro ao fazer requisição para a API:", response.status_code)
            break

    from datetime import datetime, timedelta

    token = "seu_token_de_acesso_aqui"

    # Definir o período de tempo desejado (última semana)
    data_atual = datetime.now()
    data_inicio = data_atual - timedelta(days=15)

    # Percorrer a lista de proposições
    for proposicao in projetos:
        id_proposicao = proposicao['id']

        # Fazer uma chamada ao endpoint /proposicoes/{id}/tramitacoes para obter as tramitações da proposição
        url_tramitacoes = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_proposicao}/tramitacoes"
        response_tramitacoes = requests.get(url_tramitacoes, headers={"Authorization": f"Bearer {token}"})

        if response_tramitacoes.status_code == 200:
            tramitacoes = response_tramitacoes.json()['dados']

            # Obter a última tramitação da proposição
            ultima_tramitacao = tramitacoes[-1]

            # Extrair a situação de tramitação dessa última tramitação
            situacao_tramitacao = ultima_tramitacao['descricaoSituacao']

            # Adicionar a situação de tramitação à proposição
            proposicao['situacaoTramitacao'] = situacao_tramitacao
        else:
            print(f"Erro ao obter as tramitações da proposição {id_proposicao}: {response_tramitacoes.status_code}")

    colunas = ['siglaTipo', 'numero', 'ano', 'ementa', 'situacaoTramitacao']

    pd.set_option('display.max_colwidth', None)
    df = pd.DataFrame(projetos, columns=colunas)
    pd.set_option('display.max_colwidth', None)

    st.dataframe(df)

    st.text("A atualização é realizada em tempo real")

get_data()
