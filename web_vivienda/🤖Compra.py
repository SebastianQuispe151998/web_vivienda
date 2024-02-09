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

# streamlit run .\🤖Compra.py   para arrancar
#Streamlit, una biblioteca de Python utilizada para crear aplicaciones web interactivas con facilidad

#pip install pygwalker

#configuramos el title de nuestra pagina
st.set_page_config(page_title="Análisis de Viviendas", page_icon="🧱", layout="wide")  

st.title("Análisis de Viviendas en Madrid")


# https://www.webfx.com/tools/emoji-cheat-sheet/ 

#Eliminamos tema prederteminado
theme_plotly = None #  Ninguno o iluminado

# CSS Estilos
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#Leemos el excel
ruta_del_archivo = 'data/viviendas_web.xlsx'
#df=pd.read_excel('data/viviendas_web.xlsx', sheet_name='Sheet1')
df = pd.read_excel(ruta_del_archivo, sheet_name="viviendas_web")

#Usamos de prueba para ver si leen o no los datos 
#st.dataframe(df,use_container_width=True)

logo_path = "img/bob_logo.jpg"
st.sidebar.image(logo_path, width=150)

#2. switcher para escoger nuestros filtros 


st.sidebar.header("Por favor filtre aquí:")

Tipo_vivienda= st.sidebar.multiselect(
    "Selecciona el tipo vivienda:",
    options=df["Tipo_vivienda"].unique(),
    default=df["Tipo_vivienda"].unique()
)

Municipio = st.sidebar.multiselect(
    "Selecciona el Municipio:",
    options=df["Municipio"].unique(),
    default=df["Municipio"].unique()
     
)

ICA = st.sidebar.multiselect(
    "Selecciona el Indice de calidad del aire (ICA):",
    options=df["ICA"].unique(),
    default=df["ICA"].unique()
     
)


df_selection = df.query(
    "Tipo_vivienda == @Tipo_vivienda & Municipio == @Municipio & ICA == @ICA"
)

#metodo / funcion

def HomePage():
  #1. print dataframe
 with st.expander("💵 Mi database de Viviendas en Madrid 🏠"):
  #st.dataframe(df_selection,use_container_width=True)
  shwdata = st.multiselect('Filtro :', df_selection.columns, default=["Tipo_vivienda","Municipio", "ICA"])
  st.dataframe(df_selection[shwdata],use_container_width=True)

 #2. análisis superior de cálculo
 
 total_habitantes = float(df_selection['Habitantes (2022)'].sum())
 vivienda_mode = df_selection['Tipo_vivienda'].mode().iloc[0]
 distancia_mean = int(df_selection['Distancia a Madrid (km)'].mean())
 ICA_median= int(df_selection['ICA'].median()) 
 Precio = float(df_selection['Precio'].sum())
 
  #3. Columnas
 total1,total2,total3,total4,total5 = st.columns(5,gap='large')
 with total1:

    st.info('Total de habitantes en Madrid 👫', icon="🔍")
    st.metric(label = 'nº habitantes', value= f"{total_habitantes:,.0f}")
    
 with total2:
    st.info('Tipo de vivienda mas comprada 🏘', icon="🔍")
    st.metric(label='Tipo vivienda', value=f"{vivienda_mode}")

 with total3:
    st.info('Media (km) de Distancia a Madrid 🚙', icon="🔍")
    st.metric(label= 'Media distancia',value=f"{distancia_mean:,.0f} km")

 with total4:
    st.info('Mediana Indice de calidad del aire (ICA) 🌬', icon="🔍")
    st.metric(label='Median ICA',value=f"{ICA_median:,.0f}")

 with total5:
    st.info('Precio Total de viviendas 💸', icon="🔍")
    st.metric(label='Precio',value=numerize(Precio),help=f"""Total Precio: {Precio}""")
    
 st.markdown("""---""") #Diferencia entre dos 

#-------Graficos-------------

def Graphs():
 total_habitantes = int(df_selection["Habitantes (2022)"].sum())
 average_rating = round(df_selection["Rating"].mean(), 1)
 star_rating = ":star:" * int(round(average_rating, 0))
 average_habitantes = round(df_selection["Habitantes (2022)"].mean(), 2)

#1. simple bar graph
 Habitantes_by_businessType = (
    df_selection.groupby(by=["Tipo_vivienda"]).count()[["Habitantes (2022)"]].sort_values(by="Habitantes (2022)")
 )
 fig_Habitantes = px.bar(
    Habitantes_by_businessType,
    x="Habitantes (2022)",
    y=Habitantes_by_businessType.index,
    orientation="h",
    title="Habitantes (2022) por Tipo_vivienda",
    color_discrete_sequence=["#0083B8"] * len(Habitantes_by_businessType),
    template="plotly_white",
 )

 fig_Habitantes.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
 )

#2. simple line graph------------------
 Habitantes_by_state = df_selection.groupby(by=["Municipio"]).count()[["Habitantes (2022)"]]
 fig_state = px.line(
    Habitantes_by_state,
    x=Habitantes_by_state.index,
     orientation="v",
    y="Habitantes (2022)",
    title="Habitantes (2022) por Municipio ",
    color_discrete_sequence=["#0083B8"] * len(Habitantes_by_state),
    template="plotly_white",
 )
 fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
 )

 left_column, right_column,center = st.columns(3)
 left_column.plotly_chart(fig_state, use_container_width=True)
 right_column.plotly_chart(fig_Habitantes, use_container_width=True)

 #pie chart
 with center:
  fig = px.pie(df_selection, values='Rating', names='Municipio', title='Municipio por Ratings')
  fig.update_layout(legend_title="Municipio", legend_y=0.9)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


#-----Barra de progreso-----

def ProgressBar():
  st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
  target=30000000000
  current=df_selection["Habitantes (2022)"].sum()
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
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast", #option
        default_index=0, #option
        )
 if selected=="Home":   
    #EXCEPCIONES DE ERROR
    try:
     HomePage()
     Graphs()
    except:
        st.warning("una o más opciones son obligatorias ! ")
     
    
 if selected=="Progress":
   try:
    ProgressBar()
    Graphs()
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