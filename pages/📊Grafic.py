import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pygwalker as pyg



# streamlit run .\Main.py   para arrancar

# st.set_page_config(page_title='Dashboard', page_icon=None, layout='wide', initial_sidebar_state='auto')
# st.markdown("##")


#page layout
st.set_page_config(page_title="Analiticas de Viviendas", page_icon="📊", layout="wide") 

#title
st.title("⏱ Graficar")

#load dataset
df = pd.read_excel("data/Dataset_final_ventas.xlsx",sheet_name="Dataset_final_ventas")

logo_path = "img/bob_logo.jpg"
st.sidebar.image(logo_path, width=150)

#pyg_html = pyg.to_html(df)
pyg_html=pyg.walk(df, return_html=True,dark="light")
components.html(pyg_html, height=1000, scrolling=True)