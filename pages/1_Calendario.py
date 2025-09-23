import streamlit as st
import pandas as pd
import gspread
from streamlit_calendar import calendar
from services.sheets_interaction import get_acciones_from_sheets, get_proyectos_from_sheets
# st.set_page_config(layout="wide")

# Configuración del calendario
calendar_options = {
    'selectable': True,
    'locale': 'es',
    'headerToolbar': {
        'left': 'prev,next',
        'center': 'title',
        'right': 'dayGridMonth,dayGridWeek,dayGridDay',
    },
    'buttonText': {
        'today': 'Hoy',
        'month': 'Mes',
        'week': 'Semana',
        'day': 'Día'
    },
    'slotMinTime': '06:00:00',
    'slotMaxTime': '18:00:00',
    'initialView': 'dayGridMonth',
}

df_proyectos = get_proyectos_from_sheets()
df_acciones = get_acciones_from_sheets()
eventos_calendario = []

st.header('Calendario de acciones')

# Selector que usa los nombres de los proyectos como opciones
nombres_proyecto = ['Seleccionar...']

for index, row in df_proyectos.iterrows():
    nombres_proyecto.append(row["Nombre"])

proyecto_seleccionado = st.selectbox(
    label='Seleccione un proyecto', options=nombres_proyecto)

if proyecto_seleccionado != 'Seleccionar...':
    proyecto_id = df_proyectos[df_proyectos['Nombre']
                               == proyecto_seleccionado]['ID'].item()
    acciones_filtradas = df_acciones[df_acciones['ID proyecto'] == proyecto_id]

    for index, row in acciones_filtradas.iterrows():
        inicio_evento = {
            'title': row['title'],
            'start': row['start'],
            'description': 'Descripción: ' + row['Descripción breve'],
            'end': row['start'],
            'color': 'green'
        }

        fin_evento = {
            'title': row['title'],
            'start': row['end'],
            'description': 'Descripción: ' + row['Descripción breve'],
            'end': row['end'],
            'color': 'red'
        }

        eventos_calendario.append(inicio_evento)
        eventos_calendario.append(fin_evento)

else:
    eventos_calendario = []

col_izquierda, col_derecha = st.columns(2)

with col_izquierda:
    evento_seleccionado = calendar(
        events=eventos_calendario,
        options=calendar_options,
        key='calendar'
    )

with col_derecha:
    if 'eventClick' in evento_seleccionado:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        with st.container(border=True):
            st.header(f'Acción: {evento_seleccionado['eventClick']['event']['title']}')
            
            st.subheader(evento_seleccionado['eventClick']['event']['extendedProps']['description'])
            if evento_seleccionado['eventClick']['event']['backgroundColor'] == 'green':
                st.subheader(f'Fecha de inicio: {evento_seleccionado['eventClick']['event']['start']}')
            elif evento_seleccionado['eventClick']['event']['backgroundColor'] == 'red':
                st.subheader(f'Fecha de fin: {evento_seleccionado['eventClick']['event']['start']}')
    else:
        st.info('Selecciona una acción para ver sus detalles')
