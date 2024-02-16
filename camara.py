import requests
import datetime
import pandas as pd
import streamlit as st



st.set_page_config(layout = 'wide')
#inserindo o titulo
st.title('Monitoramento das Proposições Legistalivas da Câmara dos Deputados')
st.title('FORA DO AR PARA AJUSTES')



st.text("São acompanhados os PLs, PLPs, PECs e Requerimentos que apresentaram alguma tramitação nos ultimos 15 dias e no último dia")

st.text("Os temas em monitoramento são: gás natural, petróleo, energia e CDE")

