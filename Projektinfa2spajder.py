import pandas as pd
import numpy as np
import streamlit as st
from streamlit_player import st_player
import os
from currency_converter import CurrencyConverter
import math as m
import pydeck as pdk

st.set_page_config(layout = 'wide')

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True)
st.header('Unia Europejska w pigułce')
query_params = st.experimental_get_query_params()
zak1 = 'Witaj!'
zak2 = 'Rozmówki'
zak3 = 'Kursy walut'
zak4 = 'Odległość'
zak5 = 'Państwa w pigułce'
tabs = [zak1, zak2, zak3, zak4, zak5]

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
    st.header("Witaj!")
    st.subheader("Historia Unii Europejskiej zaczęła się 18 kwietnia 1951 roku, kiedy 6 państw założyło Europejską Wspólnotę Węgla i Stali. Od tego momentu związek rozrasta się i obecnie Unia Europejska składa się z 27 państw.")
    st.subheader("Dzięki naszej aplikacji poznasz uroki każdego z nich i nie tylko! Znajdziesz tu rozmówki w 25 językach, możesz równieć sprawdzić odległoć między miastami Unii Europejskiej oraz przeliczyć waluty.")
    st.write('')
    st.write('Twórcy:')
    st.write('Bajura Michał')
    st.write('Baranowska Julia')
    st.write('Dymek Małgorzata')
    st.write('Fejtko Julia')
    st.write('Gibuła Angelika')
    st.write('Gira Paulina')
    st.write('Kwiecień Piotr')
    st.write('Warulik Mirosława')
    st.write('Zmorzyński Michał')

elif active_tab == zak2:
    
    fpath = r'C:\Users\Mirka\OneDrive\Pulpit\PajczarmProdżekts\Slowniczekint.xlsx'
    if not os.path.exists(fpath):
        raise Exception('O nie! Wygląda na to, że plik z danymi nie został odnaleziony: %s' %fpath)
            
    tabela = pd.ExcelFile(fpath, engine='openpyxl')
    names = tabela.sheet_names

    st.sidebar.write('Wybierz dział:')
    dzial = st.sidebar.selectbox('', names)
    tabela = pd.read_excel(fpath, sheet_name=dzial, engine='openpyxl')
    st.subheader(dzial)
    
    n = tabela.columns
    jezyki =  list(sorted(n))
    st.sidebar.write('Przetłumacz z:')
    wejscie = st.sidebar.selectbox('Wybierz język:', jezyki)
    st.sidebar.write('Przetłumacz na:')
    jezyki2 = jezyki
    wyjscie = st.sidebar.selectbox('Wybierz inny język:', jezyki2)
    
    
    if wyjscie == wejscie:
        st.error("Wybrane języki są takie same! Zmień język.")
    else:
        with st.form('kolejnajezu'):

            col1, col2, col3, col4 = st.beta_columns(4)
            tab = tabela[[wejscie, wyjscie]]
            with col1:
                st.write('Przetlumacz z:', wejscie)
                wej = st.selectbox('', tabela[wejscie])
            with col2:
                st.write('')
            with col3:
                st.write('')
                st.form_submit_button('Tłumacz')
            ind = tab.loc[tab.isin([wej]).any(axis=1)].index.tolist()
            with col4:
                
                st.write('Przetłumacz na:', wyjscie)
                st.write(list(tab[wyjscie][ind])[0])
                
            
            tab = pd.DataFrame(tab)
            tab = tab.style.hide_index()
        st.table(tab)
            
    
elif active_tab == zak3:
    st.header('Kalkulator walut')
    with st.form("my_form"):
        currency_list = ['EUR', 'BGN', 'DKK', 'GBP', 'SEK', 'CZK', 'PLN', 'HUF', 'RON', 'HRK', 'RUB']
        base_price_unit = st.selectbox('Wybierz walutę do przeliczenia:', currency_list)
        number = st.number_input('Kwota:')
        symbols_price_unit = st.selectbox('Wybierz walutę, którą chcesz otrzymać:', currency_list)
        
        def przelicznik_walut(wartosc, w1, w2):
            c = CurrencyConverter()
            przelicznik = c.convert(wartosc, w1, w2)
            return round(przelicznik, 2)
        
        submitted = st.form_submit_button("Przelicz")
        
        df = przelicznik_walut(number, base_price_unit, symbols_price_unit)
        if submitted:
            with st.beta_container():
                st.write('Kwota:')
                st.write(df, symbols_price_unit)
                
        

    
elif active_tab == zak4:
    file = r'C:\Users\Mirka\OneDrive\Pulpit\PajczarmProdżekts\worldcities.xlsx'
    if not os.path.exists(file):
        raise Exception('O nie! Wygląda na to, że plik z danymi nie został odnaleziony: %s' %file)
    df = pd.read_excel (file, sheet_name='Sheet1')
    lista_miast = list((df['city']))
    
    st.write("""
             # Odległość
             Uwaga! Odległoć jest liczona przy pomocy algorytmu 
             Vincentego - nie jest to rzeczywisty czas podróży 
             pomiędzy wybranymi miejscami.
             Obliczenia mogą chwilę potrwać.
             """)
        
    lista_panstw = ['Austria', 'Belgia', 'Bułgaria', 'Chorwacja', 'Cypr', 'Czechy', 'Dania', 'Estonia', 'Finlandia', 'Francja', 'Niemcy', 'Grecja', 'Węgry', 'Irlandia', 'Włochy', 'Łotwa', 'Litwa', 'Luksemburg', 'Malta', 'Holandia', 'Polska', 'Portugalia', 'Rumunia', 'Słowacja', 'Słowenia', 'Hiszpania', 'Szwecja', 'Rosja', 'Wielka Brytania']
    wk1 = st.selectbox('Wybierz kraj1:', lista_panstw)
    lista_miast1 = []
    for panstwo, miasto in zip(df.country, df.city):
        if panstwo == wk1:
            lista_miast1.append(miasto)
    mk1 = st.selectbox('Wybierz miasto1:', list(sorted(lista_miast1)))
    wk2 = st.selectbox('Wybierz kraj2', list(sorted(lista_panstw)))
    lista_miast2 = []
    for panstwo, miasto in zip(df.country, df.city):
        if panstwo == wk2:
            lista_miast2.append(miasto)
    mk2 = st.selectbox('Wybierz miasto2:', lista_miast2)
    

    with st.form("my_form"):  
        def odleglosc(wk1, wk2, mk1, mk2):
            import math as m
            a = 6378137.000
            e2 = 0.00669438002290
            for k, c, x, y in zip(df.country, df.city, df.lat, df.lng):
                if k == wk1 and c == mk1:
                    fa = m.radians(float(x))
                    la = m.radians(float(y))
            for k, c, x, y in zip(df.country, df.city, df.lat, df.lng):
                if k == wk2 and c == mk2:
                    fb = m.radians(float(x))
                    lb = m.radians(float(y))
            b=a*(m.sqrt(1-e2))
            f=1-(b/a)
            dl=lb-la
            Ua=m.atan((1-f)*m.tan(fa))
            Ub=m.atan((1-f)*m.tan(fb))
            
            L=dl
            while True:
                ssigma=m.sqrt((m.cos(Ub)*m.sin(L))**2 + (m.cos(Ua)*m.sin(Ub)- m.sin(Ua)*m.cos(Ub)*m.cos(L))**2)
                csigma=m.sin(Ua)*m.sin(Ub) + m.cos(Ua)*m.cos(Ub)*m.cos(L)
                sigma=m.atan(ssigma/csigma)
                snalfa=(m.cos(Ua)*m.cos(Ub)*m.sin(L))/ssigma
                cskwalfa=1-((snalfa)**2)
                cs2sigmam=csigma-((2*m.sin(Ua)*m.sin(Ub))/(cskwalfa))
                C=(f/16)*cskwalfa*(4+f*(4-3*cskwalfa))
                Ls=L
                L=dl+((1-C)*f*(snalfa)*(sigma+(C*(ssigma)*((cs2sigmam)+(C*(csigma)*(-1+(2*((cs2sigmam)**2))))))))
                if abs(L-Ls)<(0.000001/206265):
                    break
            u2=((a**2 - b**2)/(b**2))*cskwalfa
            A=1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)))        
            B=(u2/1024)*(256+u2*(-128+u2*(74-47*u2)))
            deltaro=B*ssigma*(cs2sigmam+(0.25)*B*(csigma*(-1+2*((cs2sigmam)**2))-(1/6)*B*cs2sigmam*(-3+4*(ssigma)**2)*(-3+4*((cs2sigmam)**2))))
            sab=b*A*(sigma-deltaro)
            
            return round(sab, 3)
        submitted = st.form_submit_button("Przelicz")
        if submitted:
            with st.beta_container():
                S = odleglosc(wk1, wk2, mk1, mk2)
                sab_km = S / 1000
                #srednia predkosc samolotu [km/h]:
                sp = 900 
                
                czas = sab_km / sp
                godzina = m.trunc(czas)
                m1 = czas - godzina
                m2 = m1 * 60
                minuty = m.trunc(m2)
                s1 = m2 - minuty
                s2 = s1 * 60
                sekundy = m.trunc(s2)
                czas = (godzina, minuty, sekundy)
                st.write('Odległość:')
                sab_km = round(sab_km, 3)
                st.write(sab_km, 'km')
                st.write('Średni czas lotu samolotem:')
                st.write(godzina, 'h', minuty, 'm', sekundy, 's')
elif active_tab == zak5:
    fppath = r'C:\Users\Mirka\OneDrive\Pulpit\PajczarmProdżekts\Panstwa.xlsx'
    if not os.path.exists(fppath):
        raise Exception('O nie! Wygląda na to, że plik z danymi nie został odnaleziony: %s' %fppath)
    
    tabelap = pd.ExcelFile(fppath, engine='openpyxl')
    namesp = tabelap.sheet_names
    namesp = list(sorted(namesp))
    
    st.sidebar.write('Wybierz państwo')
    panstwo = st.sidebar.selectbox('', namesp)
    tabelap = pd.read_excel(fppath, sheet_name=panstwo, engine='openpyxl')
    st.header(panstwo)
    st.subheader(tabelap.columns[0])
    n = tabelap.columns
    costam =  list(n)
    opis = str(tabelap[costam[0]][0])
    #st.write(costam)
    st.write(opis)
    st.subheader('Najważniejsze lotniska')
    for lot in tabelap[costam[10]]:
        if lot != 'x':
            st.write('-', lot)
        else:
            pass
    st.subheader('Najważniejsze zabytki')
    for zab in tabelap[costam[9]]:
        st.write('-', zab)        
    st.subheader('Flaga')
    st.image(tabelap[costam[2]][0])
    st.subheader('Godło')
    st.image(tabelap[costam[3]][0])
    st.subheader('Hymn')
    tytulh = tabelap[costam[4]][0]
    st.write('Tytuł:', tytulh)
    hymn = tabelap[costam[11]][0]
    st_player(hymn)
    st.write('Jeżeli chcesz odsłuchać hymn, a odtwarzacz nie działa, kliknij poniższy link:')
    st.write(hymn)
    
    F = []
    L = []
    N = []
    for f, l, n in zip(tabelap.fi_miasta, tabelap.lam_miasta, tabelap.Największe_miasta):
        F.append(f)
        L.append(l)
        N.append(n)
    dat = pd.DataFrame({'name':N, 'lat':F, 'lon':L})
    midpoint = (np.average(dat['lat']), np.average(dat['lon']))
    
    st.subheader('Najwieksze miasta')
    st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=4,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=dat,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=10000,
         ),
     ],
 ))

    


else:
    st.error("Something has gone terribly wrong.")


