import webbrowser
import streamlit as st
from UI import *
import os
# Configuración de la página
st.set_page_config(page_title="Mapa de Madrid", page_icon="🏙", layout ="wide")  

# Estilo del título
st.markdown("""
    <h1 style='
        text-align: center;
        color: #3498db;
        font-size: 4em;
        font-weight: bold;
        text-shadow: 2px 2px 4px #aaaaaa;
        margin-bottom: 20px;
    '>
    Construyamos un Futuro
    </h1>
""", unsafe_allow_html=True)

# Encabezado
heading2()

logo_path = "img/bob_logo.jpg"
st.sidebar.image(logo_path, width=150)

# Función para abrir el mapa
def abrir_mapa():
    # Especifica la ruta completa al archivo HTML o la URL
    # Ruta relativa al archivo HTML
    ruta_relativa = 'html/mapa_madrid.html'

# Obtiene la ruta completa al archivo HTML
    ruta_html = os.path.abspath(ruta_relativa)

# Abre el archivo HTML en el navegador web predeterminado
    webbrowser.open('file://' + ruta_html)
    
if st.button('Abrir Mapa'):
    abrir_mapa()


# Agregar imagen
imagen_url = "img/somos.JPG"  # Reemplaza esto con la URL o la ruta local de tu imagen
st.image(imagen_url, caption='SI SOMOS 🧑‍💻', use_column_width=True)    
# imagen_url = "img/bob.JPG"  # Reemplaza esto con la URL o la ruta local de tu imagen
# st.image(imagen_url, caption='Descripción de la imagen', use_column_width=True)
















































# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('mapa_madrid.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# import streamlit as st
# from UI import *
# st.set_page_config(page_title="Agregar / Eliminar", page_icon="📊", layout="wide")  
# heading()



# footer="""<style>
 

# a:hover,  a:active {
# color: red;
# background-color: transparent;
# text-decoration: underline;
# }

# .footer {
# position: fixed;
# left: 0;
# height:7%;
# bottom: 0;
# width: 100%;
# background-color: #243946;
# color: white;
# text-align: center;
# }
# </style>
# <div class="footer">
# <p>Creador 🤖 por <a style='display: block; text-align: center;' href="www.linkedin.com/in/aaron-chacon" target="_blank">Aarón Chacón</a></p>
# </div>
# """
# st.markdown(footer,unsafe_allow_html=True)