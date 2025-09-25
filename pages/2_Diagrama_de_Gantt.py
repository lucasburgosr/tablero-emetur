import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from services.sheets_interaction import get_acciones_from_sheets, get_proyectos_from_sheets

fecha_hoy = datetime.today()
fecha_string = fecha_hoy.strftime("%d/%m/%Y")

st.set_page_config(layout="wide")
st.header("Diagrama de Gantt")

df_acciones = get_acciones_from_sheets()
df_proyectos = get_proyectos_from_sheets()

nombres_proyecto = ['Seleccionar...']

for index, row in df_proyectos.iterrows():
    nombres_proyecto.append(row["Nombre"])

proyecto_seleccionado = st.selectbox(
    label='Seleccione un proyecto', options=nombres_proyecto)

plotly_config = {
    'locale': 'es'
}

# Carga las acciones en el gráfico en caso de que haya un proyecto seleccionado y este
# tenga acciones asociadas.
if proyecto_seleccionado != 'Seleccionar...':
    proyecto_id = df_proyectos[df_proyectos['Nombre'] == proyecto_seleccionado]['ID'].item()
    df_filtered = df_acciones[df_acciones['ID proyecto'] == proyecto_id]

    if not df_filtered.empty:
        df_gantt = df_filtered.copy()
        
        accion_height = len(df_gantt) * 60

        fig = px.timeline(
            data_frame=df_gantt,
            x_start='start',
            x_end='end',
            y='title_wrapped',
            color='Estado',
        )
        
        fig.add_vline(x=fecha_hoy, line_color='blue')
        fig.add_annotation(x=fecha_hoy, text= f'Hoy, {fecha_string}', y=1.05, yref='paper', showarrow=False, font=dict(size=16))

        fig.update_layout(
            height=accion_height,
            yaxis_tickfont_size=14,
            yaxis_title=None,
            bargap=0.5,
            xaxis_title='Meses',
            xaxis_title_font_size=18
        )
        fig.update_xaxes(showgrid=True, dtick='M1', gridcolor='Gainsboro')

        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    else:
        st.info("Este proyecto aún no tiene acciones definidas.")
else:
    st.info('Seleccione un proyecto para ver el diagrama de Gantt.')
