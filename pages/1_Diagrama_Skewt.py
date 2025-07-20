# 🌡️ Diagrama Skewt 

import streamlit as st
from datetime import datetime, time
from funcs.skewt_funcs import get_wyoming, plot_T_Td

# import locale

st.markdown('# 🌡️ Diagrama Skewt')

st.sidebar.markdown('# Selecione os dados')
st.write('Um diagrama Skew-T é um gráfico termodinâmico utilizado para representar o perfil \
         vertical da atmosfera, mostrando variáveis como temperatura, ponto de orvalho, pressão, \
         vento e índices de instabilidade. Ele permite analisar a estabilidade atmosférica, \
         prever formações de nuvens, tempestades e fenômenos convectivos, sendo essencial na meteorologia operacional e na aviação.')

st.write("No gráfico abaixo, o eixo vertical representa altitude (por pressão)\
 e o horizontal mostra temperatura (em vermelho) e ponto de orvalho (em azul).")

# ——— Mapa ICAO → WMO ———
# Adicione, remova ou edite conforme necessário
ICAO2WMO = {
    "SBBH": "83566",   # Belo Horizonte / Confins
    "SBSP": "83948",   # São Paulo / Guarulhos
    "SBKP": "83383",   # Belém / Val-de-Cans
    "SBGL": "83746",   # Rio de Janeiro / Galeão
    "SBFZ": "82397",   # Fortaleza
    "SBCT": "82384",   # Curitiba / Bacacheri
    "SBEG": "83383",   # Manaus / Eduardo Gomes
    # …adicione quantos códigos você precisar
}

station_name = st.sidebar.selectbox(
    '🛫 Escolha o código do aeroporto',
    list(ICAO2WMO.keys())
)

date = st.sidebar.date_input(
    '🗓️ Escolha a data desejada',
    value=datetime.now() # Ver com a Eliana a questão da hora
)
date = datetime.combine(date, time(hour=0, minute=0))

st.write(f'🛫 Aeroporto selecionado: {station_name} ({ICAO2WMO[station_name]})')
st.write('📅 Data escolhida:')
st.write(f'- UTC: {date}')

try:
    df = get_wyoming(date, str(station_name), ICAO2WMO)
    plot_T_Td(df, f'Skew-T - {station_name} - {date:%d/%m/%Y %HZ}')
except ValueError as e:
    if f'No sounding for {station_name}' in str(e):
        st.error(f'Não há dados de radiossondagem disponíveis para {station_name} em  {date:%d/%m/%Y %HZ}')
    else:
        st.error(str(e))
