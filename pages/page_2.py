import streamlit as st
from datetime import datetime, time
import pytz
from funcs.meteograma_funcs import get_data, plot_temp_td

STATIONS = {
    "Cabo Frio":       {"id": "82613", "tz": "America/Sao_Paulo"},
    "Arraial do Cabo":  {"id": "82613", "tz": "America/Sao_Paulo"},
    # adicione outros se desejar
}

st.markdown('# 📈 Meteograma')

st.warning('Atualmente não está funcionando pois as estações estão sendo descontinuadas, assim que for possível obter os dados necessários isso será corrigido.')

st.sidebar.markdown('# Selecione os dados')
st.write('Um meteograma T–Td exibe a variação da temperatura do ar (T) e da temperatura do ponto de orvalho (Td) ao longo do tempo em um local. \
         Ele permite avaliar a umidade relativa, identificar momentos de saturação e mudanças térmicas, sendo útil para previsão do tempo, \
         monitoramento ambiental e tomada de decisão em atividades meteorologicamente sensíveis.')

station_name = st.sidebar.selectbox(
    '📡 Selecione a estação desejada',
    list(STATIONS.keys())
)

station_info = STATIONS[station_name]
station_id = station_info['id']
local_tz = pytz.timezone(station_info['tz'])

st.write(f'📡 Estação selecionada: {station_name} ({station_id})')

date_init = st.sidebar.date_input('🗓️ Escolha a **data inicial** do intervalo')
end_date = st.sidebar.date_input('🗓️ Escolha a **data final** do intervalo')

date_init_local = local_tz.localize(datetime.combine(date_init, time(hour=0, minute=0)))
end_date_local = local_tz.localize(datetime.combine(end_date, time(hour=0, minute=0)))

date_init_utc = date_init_local.astimezone(pytz.utc)
end_date_utc = end_date_local.astimezone(pytz.utc)

st.write(f'📅 Intervalo selecionado:')
st.write(f'- Local: {date_init_local.strftime('%Y-%m-%d %H:%M %Z')} → {end_date_local.strftime('%Y-%m-%d %H:%M %Z')}')
st.write(f"- UTC:   {date_init_utc.strftime('%Y-%m-%d %H:%M %Z')} → {end_date_utc.strftime('%Y-%m-%d %H:%M %Z')}")

df = get_data(station_id, date_init_local, end_date_local, local_tz)
if df is not None and not df.empty:
    plot_temp_td(df, station_name, date_init_local, end_date_local, local_tz)
else:
    st.error('Dados horários para o intervalo não estão disponíveis no repositório da Meteostat.')