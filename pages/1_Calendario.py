import streamlit as st
import pandas as pd
import gspread
from streamlit_calendar import calendar
from services.sheets_interaction import get_acciones_from_sheets, get_proyectos_from_sheets
st.set_page_config(layout="centered")

# Configuración del calendario
calendar_options = {
    'editable': False,
    'selectable': True,
    'locale': 'es',
    'headerToolbar': {
        'left': 'today prev,next',
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

st.header('Calendario de acciones')

# Selector que usa los nombres de los proyectos como opciones
nombres_proyecto = ['Seleccionar...']

for index, row in df_proyectos.iterrows():
    nombres_proyecto.append(row["Nombre"])
    
proyecto_seleccionado = st.selectbox(label='Seleccione un proyecto', options=nombres_proyecto)

if proyecto_seleccionado != 'Seleccionar...':
    proyecto_id = df_proyectos[df_proyectos['Nombre'] == proyecto_seleccionado]['ID'].item()
    acciones_filtradas = df_acciones[df_acciones['ID proyecto'] == proyecto_id].to_dict(orient='records')
else:
    acciones_filtradas = pd.DataFrame()
    
_ = calendar(
    events=acciones_filtradas,
    options=calendar_options,
    key='calendar'
)
