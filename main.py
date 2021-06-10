import pandas as pd
import streamlit as st
from pandas import read_excel
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True)
st.header('Unia Europejska w pigułce')
query_params = st.experimental_get_query_params()
zak1 = 'Witaj!'
zak2 = 'Rozmówki'
zak3 = 'Kursy walut'
zak4 = 'Coś jeszcze innego'
tabs = [zak1, zak2, zak3, zak4]

if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = zak1

if active_tab not in tabs:
    st.experimental_set_query_params(tab=zak1)
    active_tab = zak1

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == zak1:
    st.write("")
    st.write("**SZLAAAAAAAAAAAAAAAAAAAAAAAAG**")
    st.slider(
        "Does this get preserved? You bet it doesn't!",
        min_value=0,
        max_value=100,
        value=50)

elif active_tab == zak2:

    st.write("Rozmówki w językach")
    jezyki =  ['fsefesf', 'hisjnbckjes', 'blabla']
    wejscie = st.selectbox('Wybierz język wejściowy:', jezyki)
    wyjscie = st.selectbox('Wybierz język wyjściowy:', jezyki)
    if wyjscie == wejscie:
        st.error("Tak nie wolno!")
    else:
        pass





elif active_tab == zak3:
    st.write("If you'd like to contact me, then please don't.")
elif active_tab == zak4:
    st.write("To ma potencjał XD")
else:
    st.error("Something has gone terribly wrong.")

tabela = pd.read_excel(r'C:\Users\Mirka\PycharmProjects\ODjakiegostypa\Slowniczekint.xlsx', sheet_name='Slowniczekint', engine='openpyxl')
print(tabela)