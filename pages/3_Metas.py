import streamlit as st
import pandas as pd
from services.sheets_interaction import get_metas_from_sheets, get_acciones_from_sheets, get_proyectos_from_sheets

st.header('Progreso de Metas')

df_metas = get_metas_from_sheets()
df_acciones = get_acciones_from_sheets()
df_proyectos = get_proyectos_from_sheets()

# Selector que usa los nombres de los proyectos como opciones
nombres_proyecto = ['Seleccionar...']

for index, row in df_proyectos.iterrows():
    nombres_proyecto.append(row["Nombre"])
    
proyecto_seleccionado = st.selectbox(label='Seleccione un proyecto', options=nombres_proyecto)

if proyecto_seleccionado != 'Seleccionar...':
    proyecto_id = df_proyectos[df_proyectos['Nombre'] == proyecto_seleccionado]['ID'].item()
    df_metas = df_metas[df_metas['ID proyecto'] == proyecto_id]
    acciones_por_proyecto = df_acciones[df_acciones['ID proyecto'] == proyecto_id]
    
# ----------


    acciones_por_proyecto = df_acciones.groupby('ID meta')

    agg_instructions = {
        'title':'count', 'completada':'sum'
    }

    # Agrupa las acciones por meta y combina ambas para mostrar el progreso según tareas completadas
    acciones_agrupadas_por_meta = acciones_por_proyecto.agg(agg_instructions)
    acciones_agrupadas_por_meta = acciones_agrupadas_por_meta.rename(columns={'title':'Total Tareas', 'completada': 'Tareas Completadas'})
    acciones_agrupadas_por_meta['progreso'] = ((acciones_agrupadas_por_meta['Tareas Completadas'] / acciones_agrupadas_por_meta['Total Tareas']) * 100).astype(int)
    acciones_agrupadas_por_meta = acciones_agrupadas_por_meta.reset_index()
    df_metas = df_metas.rename(columns={'ID': 'ID meta'})
    acciones_metas_df = pd.merge(left=acciones_agrupadas_por_meta, right=df_metas, on='ID meta')
    
    col_izquierda, col_derecha = st.columns(2)
    
    with col_izquierda:
        st.header("Metas")
        
    with col_derecha:
        st.header("Acciones")

    for index, row in acciones_metas_df.iterrows():
        col_izquierda, col_derecha = st.columns(2)
        
        with col_izquierda:
            st.write(row['Meta'])
            st.metric(value=row['progreso'], label='Estado de la meta (%)')
            st.progress(row['progreso'])
            
        with col_derecha:
            acciones_filtradas = df_acciones[df_acciones['ID meta'] == row['ID meta']]
            acciones_filtradas = acciones_filtradas[['title', 'Descripción breve', 'start', 'end', 'Estado']]
            acciones_filtradas = acciones_filtradas.rename(columns={'title': 'Acción / Etapa', 'start': 'Inicio', 'end': 'Fin'})
            st.dataframe(acciones_filtradas, hide_index=True)
            
        st.divider()
else:
    st.info('Selecciona un proyecto para ver el estado de las metas')