import streamlit as st
import time
from io import StringIO
from backend import obtener_file, graf_no_neteo_total, graf_neteo_total, graf_no_neteo, graf_coste_exc, graf_coste_pvpc, graf_demver



#configuramos la web y cabecera
st.set_page_config(
    page_title="excedentes",
    page_icon=":bulb:",
    layout='wide',
    initial_sidebar_state='collapsed'
)
st.title('Autoconsumo con excedentes')
st.caption("Copyright by Jose Vidal :ok_hand:")
url_apps = "https://powerappspy-josevidal.streamlit.app/"
st.write("Visita mi mini-web de [PowerAPPs](%s) con un montón de utilidades." % url_apps)
url_linkedin = "https://www.linkedin.com/posts/jfvidalsierra_powerapps-activity-7216715360010461184-YhHj?utm_source=share&utm_medium=member_desktop"
st.write("Deja tus comentarios y propuestas en mi perfil de [Linkedin](%s)" % url_linkedin)


#usamos ejemplo de curva por defecto
file=st.file_uploader('Curva de carga a analizar')

zona_mensajes=st.empty()


if file is not None:
    try:
        stringio = StringIO(file.getvalue().decode("utf-8"))
        df_origen, df_coste_24h, df_demver_24h, demanda, demanda_neteo,vertido,vertido_neteo, fecha_ini_curva, fecha_fin_curva, precio_medio_exc, coste_exc,precio_medio_pvpc, coste_pvpc=obtener_file(stringio)
        zona_mensajes.success('Archivo cargado correctamente!')
    except Exception as e:
        zona_mensajes.error(f'Error al cargar el archivo. Asegúrate de que el archivo tenga el formato correcto')
        time.sleep(3)
        zona_mensajes.warning('Se cargará el archivo de ejemplo')
        time.sleep(3)
        zona_mensajes.warning('Por favor, sube una curva de carga de i-DE para autoconsumidores. Lo que estás viendo es un archivo de ejemplo')
        file='curvas/2024 07.csv'
        df_origen, df_coste_24h, df_demver_24h, demanda, demanda_neteo,vertido,vertido_neteo, fecha_ini_curva, fecha_fin_curva, precio_medio_exc, coste_exc,precio_medio_pvpc, coste_pvpc=obtener_file(f'curvas/2024 07.csv')
else:
    zona_mensajes.warning('Por favor, sube una curva de carga. Lo que estás viendo es un archivo de ejemplo')
    #file='curvas/2024 07.csv'
    df_origen, df_coste_24h, df_demver_24h, demanda, demanda_neteo,vertido,vertido_neteo, fecha_ini_curva, fecha_fin_curva, precio_medio_exc, coste_exc,precio_medio_pvpc, coste_pvpc=obtener_file(f'curvas/2024 07.csv')
    
#df_origen, df_coste_24h, df_demver_24h, demanda, demanda_neteo,vertido,vertido_neteo, fecha_ini_curva, fecha_fin_curva, precio_medio_exc, coste_exc,precio_medio_pvpc, coste_pvpc=obtener_file(f'curvas/2024 07.csv')


col1, col2 = st.columns([.8,.2])
with col1:
    neteo = st.toggle('Cambia a NETEO (saldos horarios facturables). Recuerda que en la parte superior derecha del gráfico tienes herramientas de zoom.')

    if neteo:
        graf2=graf_neteo_total(df_origen)
        st.write(graf2)
    else:
        graf1=graf_no_neteo_total(df_origen)
        st.write(graf1)
with col2:
    st.subheader('Datos generales',divider='rainbow')
    mensaje = f"Se dispone de datos desde el **{fecha_ini_curva}** hasta el **{fecha_fin_curva}**"
    st.markdown(mensaje, unsafe_allow_html=True)
    st.info('Estos son los valores de demanda y excedentes, tanto leídos por el contador como facturados por saldos horarios (NETEO). Valores en kWh.',icon="ℹ️")
    
    col11,col12=st.columns(2)
    with col11:
        st.metric('Lectura de demanda',value=demanda)
        st.metric(f':red-background[Demanda a facturar]', value=demanda_neteo)
    with col12:
        st.metric('Lectura de excedentes', value=vertido)
        st.metric(f':green-background[Excedentes a facturar]', value=vertido_neteo)

col3, col4 = st.columns([.8,.2])
with col3:
    graf3=graf_no_neteo(df_origen)
    st.write(graf3)
with col4:
    st.subheader('Valores horarios por días. Gráfico animado',divider='rainbow')
    mensaje = f"Se dispone de datos desde el **{fecha_ini_curva}** hasta el **{fecha_fin_curva}**"
    #st.markdown(mensaje, unsafe_allow_html=True)
    st.info('Mueve el cursor en la parte inferior del gráfico para visualizar valores horarios según la fecha seleccionada. Valores de contador',icon="ℹ️")
    
col5, col6 = st.columns([.8,.2])
with col5:
    graf4=graf_coste_exc(df_coste_24h)
    st.write(graf4)
with col6:
    st.subheader('Excedentes: Facturación',divider='rainbow')
    mensaje = f"Periodo facturado desde el **{fecha_ini_curva}** hasta el **{fecha_fin_curva}**"
    st.markdown(mensaje, unsafe_allow_html=True)
    st.info('En esta sección puedes ver una gráfica del acumulado horario de excedentes contrastada con el valor de los mismos. Como resultado, se obtiene el precio medio del excedente a facturar',icon="ℹ️")
    col61,col62=st.columns(2)
    with col61:
        st.metric(f':green-background[Excedentes a facturar (kWh)]', value=vertido_neteo)
        st.metric(f':violet-background[Precio medio excedente €/kWh]',value=precio_medio_exc)
        #st.metric(f':red-background[Demanda a facturar]', value=demanda_neteo)
    with col62:
        st.metric(f':green-background[Coste a facturar (€)]', value=coste_exc)
        
col7, col8 = st.columns([.8,.2])
with col7:
    graf5=graf_coste_pvpc(df_coste_24h)
    st.write(graf5)
with col8:
    st.subheader('Demanda: Facturación',divider='rainbow')
    mensaje = f"Periodo facturado desde el **{fecha_ini_curva}** hasta el **{fecha_fin_curva}**"
    st.markdown(mensaje, unsafe_allow_html=True)
    st.info('En esta sección puedes ver una gráfica del acumulado horario de la demanda contrastada con el valor de la misma. Como resultado, se obtiene el precio medio de la demanda a facturar',icon="ℹ️")
    col81,col82=st.columns(2)
    with col81:
        st.metric(f':green-background[Demanda a facturar (kWh)]', value=demanda_neteo)
        st.metric(f':violet-background[Precio medio demanda €/kWh]',value=precio_medio_pvpc)
        #st.metric(f':red-background[Demanda a facturar]', value=demanda_neteo)
    with col82:
        st.metric(f':green-background[Coste a facturar (€)]', value=coste_pvpc)        
            
        

    
