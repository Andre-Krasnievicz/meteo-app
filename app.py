import streamlit as st

main_page = st.Page('main_page.py', title='Diagrama Skewt', icon='🌡️')
page_2 = st.Page('Page_2.py', title='Meteograma', icon='📈')

pg = st.navigation([main_page, page_2])

pg.run()
