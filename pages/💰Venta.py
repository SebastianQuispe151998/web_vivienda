import streamlit as st
import pandas as pd 
import streamlit.components.v1 as stc
import plotly.express as px
import time 
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import locale

# Configurar la localización para utilizar separadores de millares
locale.setlocale(locale.LC_ALL, '')
# streamlit run .\🤖Main.py   para arrancar
#Streamlit, una biblioteca de Python utilizada para crear aplicaciones web interactivas con facilidad


#configuramos el title de nuestra pagina
st.set_page_config(page_title="Análisis de Ventas de Viviendas", page_icon="🧱", layout="wide")  

logo_path = "img/bob_logo.jpg"
st.sidebar.image(logo_path, width=150)

# https://www.webfx.com/tools/emoji-cheat-sheet/ 

#Eliminamos tema prederteminado
theme_plotly = None #  Ninguno o iluminado

# CSS Estilos
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#Leemos el excel
ruta_del_archivo = 'data/Dataset_final_ventas.xlsx'
#df=pd.read_excel('data/viviendas_web.xlsx', sheet_name='Sheet1')
df = pd.read_excel(ruta_del_archivo, sheet_name="Dataset_final_ventas")

#Usamos de prueba para ver si leen o no los datos 
#st.dataframe(df,use_container_width=True)


##Metodo filtrar precios
def filter_dataframe(df):
    # Obtener el rango de precios mínimo y máximo
    precio_min = df["Precio"].min()
    precio_max = df["Precio"].max()

    # Formatear los valores para el rango de precios con comas como separadores de miles
    precio_min_str = f"{precio_min:,.0f}"
    precio_max_str = f"{precio_max:,.0f}"

    # Crear un slider en la barra lateral para seleccionar el rango de precios
    precio_range = st.sidebar.slider(
        "Selecciona el rango de precios:",
        min_value=precio_min,
        max_value=precio_max,
        value=(precio_min, precio_max),
        format="%.0f",  # Establecer el formato para mostrar números enteros
        help=f"({precio_min_str} - {precio_max_str})"
    )

    # Filtrar DataFrame según el rango de precios seleccionado
    df_filtered = df[(df["Precio"] >= precio_range[0]) & (df["Precio"] <= precio_range[1])]

    # Filtrar por Tipo_vivienda, Población y Municipios seleccionados
    Tipo_vivienda = st.sidebar.multiselect(
        "Selecciona el tipo de vivienda:",
        options=df_filtered["Tipo_vivienda"].unique(),
        default=df_filtered["Tipo_vivienda"].unique()
    )

    Poblacion_options = df_filtered["Población"].unique()
    Poblacion = st.sidebar.multiselect(
        "Selecciona la Población:",
        options=Poblacion_options,
        default=Poblacion_options[:1]
    )

    Municipios_options = df_filtered["Municipios"].unique()
    Municipios = st.sidebar.multiselect(
        "Selecciona los Municipios correspondientes:",
        options=Municipios_options,
        default=Municipios_options[:1]
    )

    df_result = df_filtered.query(
        "Tipo_vivienda == @Tipo_vivienda & Población == @Poblacion & Municipios == @Municipios"
    )

    return df_result

# Método para mostrar el DataFrame filtrado
def show_dataframe(df):
    with st.expander("💵 Mi database de Viviendas en Ventas en Madrid 🏠"):
        # Imprimir el DataFrame con las columnas seleccionadas
        shwdata = st.multiselect('Filtro :', df.columns, default=["Tipo_vivienda", "Población", "Municipios"])
        st.dataframe(df[shwdata], use_container_width=True)

# Llamada a los métodos
df_filtered = filter_dataframe(df)
show_dataframe(df_filtered)

#-----Barra de progreso-----

def ProgressBar():
  st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
  target=30000000000
  current=df["precio"].sum()
  percent=round((current/target*100))
  my_bar = st.progress(0)

  if percent>100:
    st.subheader("Target 100 complited")
  else:
   st.write("you have ", percent, " % " ," of ", (format(target, ',d')), " TZS")
   for percent_complete in range(percent):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1,text="Target percentage")

#-----SIDE BAR----- CAMBIO DE PAGINA DE UNA A OTRA
 
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
         #menu_title=None,
        options=["Home"],
        menu_icon="cast", #option
        default_index=0, #option
        )
    
     
    
 if selected=="Progress":
   try:
    ProgressBar()
    #Graphs()
   except:
    st.warning("una o más opciones son obligatorias ! ")
 
    
#print side bar
sideBar()

footer="""<style>
 

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
height:7%;
bottom: 0;
width: 100%;
background-color: #243946;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Creador 🤖 por <a style='display: block; text-align: center;' href="www.linkedin.com/in/aaron-chacon" target="_blank">Aarón Chacón</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)