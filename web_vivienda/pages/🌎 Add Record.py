import streamlit as st
import pandas as pd
import seaborn as sns
from UI import *



st.set_page_config(page_title="Agregar / Eliminar", page_icon="📊", layout="wide")  
#heading()
st.title("Agregar Viviendas en Madrid")

logo_path = "img/bob_logo.jpg"
st.sidebar.image(logo_path, width=150)

if 'number_of_rows' not in st.session_state:
    st.session_state['number_of_rows']=4
    st.session_state['type']='Categorical'
    

increment=st.sidebar.button('mostrar más columnas ➕')
if increment:
  st.session_state.number_of_rows +=1
decrement=st.sidebar.button('mostrar menos columnas ➖')
if decrement:
 st.session_state.number_of_rows -=1

ruta_del_archivo = 'data/viviendas_web.xlsx'
#df=pd.read_excel('data/viviendas_web.xlsx', sheet_name='Sheet1')
df = pd.read_excel(ruta_del_archivo, sheet_name="viviendas_web")


 

theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.markdown("##")

st.sidebar.header("Agregar nuevo")
options_form=st.sidebar.form("Option Form")

municipio = options_form.selectbox("Municipio",{'Alcalá de Henares', 'San Sebastián de los Reyes',
       'Madrid Capital', 'Pozuelo de Alarcón', 'Móstoles', 'Fuenlabrada',
       'Las Rozas de Madrid', 'La Moraleja', 'Other', 'Majadahonda',
       'Boadilla del Monte'})
provincia = options_form.selectbox("Provincia",{"Madrid"})
comunidad_autonoma = options_form.selectbox("Comunidad Autónoma",{"Madrid"})
habitantes = options_form.number_input("Habitantes (2022)")
#carril_bici=options_form.selectbox("Carril Bici",{"Yes","No"})
carril_bici=options_form.number_input("Carril Bici")
rating=options_form.number_input("Rating")
distancia_madrid=options_form.number_input("Distancia a Madrid (km)")
precio_medio = options_form.number_input("Precio medio vivienda (EUR/m2)")
ica = options_form.number_input("ICA")
tipo_vivienda = options_form.selectbox("Tipo_vivienda",{'Chalet', 'Piso', 'Casa', 'Casa pareada'})
precio = options_form.number_input("Precio")
superficie = options_form.number_input("Superficie")
habitaciones = options_form.number_input("Habitaciones")
banos = options_form.number_input("Baños")
comprado = options_form.number_input("Comprado")

add_data=options_form.form_submit_button(label="Agregar nueva informacion")

if add_data:
 if provincia  !="" or municipio !="":
     df = pd.concat([df, pd.DataFrame.from_records([{ 
         'Municipio': municipio,
         'Provincia':provincia,
         'Comunidad Autónoma':comunidad_autonoma,
         'Habitantes':float(habitantes),
         'Carril Bici':int(carril_bici), #'carril_bici':flood
         'Rating':float(rating),
         'Distancia a Madrid (km)':int(distancia_madrid),
         'Precio medio vivienda (EUR/m2)':int(distancia_madrid),
         'ICA':int(ica),
         'Tipo_vivienda': tipo_vivienda,
         'Precio': float(precio),
         'Superficie': float(superficie),
         'Habitaciones': int(habitaciones),
         'Baños': int(banos),
         'Comprado': int(comprado)   
         }])])
     try:
        df.to_excel("data/viviendas_web.xlsx",index=False)
     except:
        st.warning("Cerrar dataset 😫")
     st.success("¡Se ha agregado un nuevo registro exitosamente! 😎")
 else:
    st.sidebar.error("nombre requerido")



#st.dataframe(df_selection,use_container_width=True)
shwdata = st.multiselect('Filter :', df.columns, default=["Tipo_vivienda","Municipio", "ICA"])
st.dataframe(df.tail(st.session_state['number_of_rows']),use_container_width=True,)

 
 