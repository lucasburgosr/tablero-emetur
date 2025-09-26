import streamlit as st
import pandas as pd
from services.sheets_interaction import get_cumpleaños_from_sheets, get_proyectos_from_sheets, get_personas_from_sheets, get_persona_proyecto_from_sheets

st.title("Visualización de Proyectos - EMETUR")

df_cumpleaños = get_cumpleaños_from_sheets()

proximo_cumpleaños = df_cumpleaños.loc[df_cumpleaños['Estado'] == 'Próximo']

proximo_cumpleaños = proximo_cumpleaños.iloc[0]

nombre_cumpleaños = proximo_cumpleaños['Nombre']

st.write(f"Próximo cumpleaños 🎈: {nombre_cumpleaños}")

st.divider()

st.set_page_config(layout='wide')

df_proyectos = get_proyectos_from_sheets()
df_personas = get_personas_from_sheets()
df_personas_proyectos = get_persona_proyecto_from_sheets()

df_personas = df_personas.rename(columns={'Nombre': 'Nombre Persona'})
df_proyectos = df_proyectos.rename(columns={'Nombre': 'Nombre Proyecto'})

df_final = df_personas_proyectos.merge(right=df_personas, left_on=['ID persona'], right_on=['ID'])
df_final = df_final.merge(right=df_proyectos, left_on=['ID proyecto'], right_on=['ID'])

nombres = ['Mostrar todos']

for index, row in df_personas.iterrows():
    nombres.append(row['Nombre Persona'])
    
responsable = st.selectbox("Selecciona un responsable/colaborador", nombres)

if responsable != 'Mostrar todos':
    df_proyectos = df_final.loc[df_final['Nombre Persona'] == responsable]
    df_proyectos = df_proyectos[['ID proyecto', 'Nombre Proyecto', 'Objetivo General']].copy()
    df_proyectos.rename(columns={'ID proyecto': 'ID'}, inplace=True)

col_izquierda, col_derecha = st.columns(2)

if df_proyectos.empty:
        st.info("Esta persona no tiene proyectos asignados")
else:
    with col_izquierda:
            st.header("Proyecto")
            
    with col_derecha:
            st.header("Responsables")

for index, row in df_proyectos.iterrows():
    
    col_izquierda, col_derecha = st.columns(2)
    
    with col_izquierda:
        st.header(row['Nombre Proyecto'])
        st.write(row['Objetivo General'])
        
    with col_derecha:
        personas = df_final.loc[df_final['ID proyecto'] == row['ID']]
        personas = personas.rename(columns={'Nombre Persona': 'Nombre'})

        st.dataframe(personas[['Nombre', 'Rol']], hide_index=True)
        
    st.divider()