import streamlit as st
from statsbombpy import sb
import glob
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import pydeck as pdk
import geopandas as gpd
from functools import reduce
from deep_translator import MyMemoryTranslator 
from itertools import zip_longest
from statsbombpy import sb

@st.cache_data
def load_competitions() -> pd.DataFrame:
    """
    Load competitions from StatsBomb API
    """    
    competitions = sb.competitions()    
   
    return competitions


# https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def grouped(iterable, n) -> tuple:
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip_longest(*[iter(iterable)]*n)

#https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    
    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Filtrar Dados")

    if not modify:
        return df

    df = df.copy()
    # para poder filtrar pelos indices
    df.reset_index(inplace=True)
    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filtrar em", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[col], dict):
                continue
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 20 or column == 'type':
                user_cat_input = right.multiselect(
                    f"Valores para {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                with st.spinner('filtrando...'):
                    df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Valores para {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                with st.spinner('filtrando...'):
                    df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Valores para {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    with st.spinner('filtrando...'):
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring ou regex em {column}",
                )
                if user_text_input:
                    with st.spinner('filtrando...'):
                        df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

def row_type(row) -> int:
    """
    Função que verifica se a linha é um continente
    """
    if row.local in ['África', 'América Central', 'América do Sul', 'América do Norte', 'Ásia', 'Europa', 'Oriente Médio', 'Oceania']:
        return 1
    if row.local == "Total":
        return 0
    if row.local == "Países não especificados":
        return 3
    return 2

def get_continent(row) -> str:
    """
    Função que obtem o continente da linha olhando o ultimo continente encontrado
    """
    if row.tipo == 1:
        st.session_state.last_continent = row.local
        return row.local
    if row.tipo == 0:
        return '-'
    if row.tipo == 2:
        return st.session_state.last_continent
    if row.tipo == 3:
        return "Zona não especificada"

def convert_to_datetime(row) -> pd.Timestamp | None:
    """
    Função que converte a string para datetime
    """
    ano, mes = row.split('_')
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    try:
        mes = meses.index(mes) + 1        
        return pd.to_datetime(f'{ano}-{mes}', format='%Y-%m', errors='coerce')
    except:
        return None


@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def load_country_data() -> pd.DataFrame:
    """
    Load data from file path and load into a DataFrame dictionary
    """
    # data = pd.read_csv('https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv')
    
    # data['name'] = data['name'].apply(lambda x: MyMemoryTranslator(source='en-US', target='pt-BR').translate(text=x))
    
    data = pd.read_csv('data/01_raw/geoData.csv')
    
    return data    

@st.cache_data       
def combine_data(data: dict) -> pd.DataFrame|None:
    """
    Combine all DataFrames into a single DataFrame
    """
    dataframe_combined = None
    with st.spinner('Combinando planilhas...'):               
        dataframe_combined = reduce(lambda  left,right: pd.merge(left,right, left_index=True, right_index=True,  how='outer'), data.values()).fillna(0)
        st.success('Planilhas combinadas com sucesso!')
        
    return dataframe_combined

                
def upload_csv_file() -> None:
    st.session_state["upload_csv"] = True
            
def upload_excel_file() -> None:
    st.session_state["upload_excel"] = True

def checkbox_container(data):
    cols = st.columns(2)
    if cols[0].button('Sel. Todos'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
        #st.experimental_rerun()
    if cols[1].button('Rem. Todos'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
        #st.experimental_rerun()

    ckcols = st.columns(4)
    for ix, i in enumerate(data):
        ckcols[ix % 4].checkbox(i, key='dynamic_checkbox_' + i, value=st.session_state.get('dynamic_checkbox_' + i, False))

def get_selected_checkboxes() -> list:
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def parse_excel_file(uploaded_excel) -> dict:
    progress_text = "Carregando planilhas, aguarde..."
    my_bar = st.progress(0, text=progress_text)
    dataframes = {}
    xl = pd.ExcelFile(uploaded_excel)                
    for sheet_name in xl.sheet_names:
        if sheet_name.isnumeric(): # carrega somente as planilhas que são anos, na ordem original
            dataframes[sheet_name] = xl.parse(sheet_name, header=5, index_col=None)
            # renomea coluna 0 para local
            dataframes[sheet_name].rename(columns={dataframes[sheet_name].columns[0]: 'local'}, inplace=True)
            dataframes[sheet_name]["local"] = dataframes[sheet_name]["local"].str.strip()
            #dataframes[sheet_name].index.rename('local', inplace=True)
            #dataframes[sheet_name].index = dataframes[sheet_name].index.str.strip()
            dataframes[sheet_name].columns = [sheet_name + "_" + col if col != 'local' else 'local' for col in dataframes[sheet_name].columns.str.strip() ]
            dataframes[sheet_name].dropna(inplace=True)
            dataframes[sheet_name].insert(0, 'tipo', '')
            dataframes[sheet_name].insert(0, 'continente', '')

            dataframes[sheet_name].reset_index(inplace=True)
           
            # loop para preencher a coluna continente, se não tiver ordenado por continente não funciona
            for index, row in dataframes[sheet_name].iterrows():
                dataframes[sheet_name].at[index, 'tipo'] = row_type(row)
                dataframes[sheet_name].at[index, 'continente'] = get_continent(dataframes[sheet_name].loc[index])
            
           
            dataframes[sheet_name].drop(columns=['index'], inplace=True)
            #st.write(dataframes[sheet_name].head(25))
            # define o index como continente e o index original 
            #dataframes[sheet_name].reset_index(drop=True, inplace=True)
            dataframes[sheet_name].set_index(['tipo', 'continente', 'local'], drop=True, inplace=True)
            # ordena o index
            #dataframes[sheet_name].sort_index(inplace=True)
            # converte colunas para nunmerico
            dataframes[sheet_name] = dataframes[sheet_name].apply(pd.to_numeric, errors='coerce')
        my_bar.progress((list(xl.sheet_names).index(sheet_name) + 1) / len(xl.sheet_names))
    my_bar.empty()
    st.write("Dados Carregados com Sucesso!") 
    return dataframes

def limpa_filtro() -> None:
    for i in st.session_state.keys():
        if i.startswith('dynamic_checkbox_'):
            del st.session_state[i]
