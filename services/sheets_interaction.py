import streamlit as st
import gspread
import pandas as pd
import textwrap

# Configuración de la conexión con Google Sheets
SHEETS_ID = st.secrets["SHEETS_ID"]
ACCOUNT_CRED = st.secrets["ACCOUNT_CRED"]
gc = gspread.service_account(ACCOUNT_CRED)
sh = gc.open_by_key(SHEETS_ID)

# El decorador st.cache_data sirve para mantener los datos en la memoria cache durante un
# determinado periodo de tiempo sin tener que hacer nuevas requests a la API.
@st.cache_data(ttl=300)
def get_proyectos_from_sheets():
    proyectos = sh.get_worksheet(1).get_all_records()
    df_proyectos = pd.DataFrame(data=proyectos, index=None)
    
    return df_proyectos

@st.cache_data(ttl=300)
def get_acciones_from_sheets():
    acciones = sh.get_worksheet(4).get_all_records()
    df_acciones = pd.DataFrame(data=acciones, index=None)
    df_acciones = df_acciones.rename(columns={'Acción / Etapa': 'title', 'Fecha de inicio': 'start', 'Fecha finalización': 'end'})
    df_acciones['title_wrapped'] = df_acciones['title'].apply(lambda title: '<br>'.join(textwrap.wrap(title, width=60)))
    df_acciones['completada'] = (df_acciones['Estado'] == 'Finalizada').astype(int)
    
    return df_acciones

@st.cache_data(ttl=300)
def get_metas_from_sheets():
    metas = sh.get_worksheet(3).get_all_records()
    df_metas = pd.DataFrame(data=metas, index=None)
    
    return df_metas

@st.cache_data(ttl=300)
def get_personas_from_sheets():
    personas = sh.get_worksheet(5).get_all_records()
    df_personas = pd.DataFrame(data=personas)
    
    return df_personas

@st.cache_data(ttl=300)
def get_persona_proyecto_from_sheets():
    personas_proyectos = sh.get_worksheet(7).get_all_records()
    df_personas_proyectos = pd.DataFrame(data=personas_proyectos, index=None)
    
    return df_personas_proyectos