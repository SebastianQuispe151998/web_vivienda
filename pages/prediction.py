import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import metrics
from sklearn import preprocessing
import matplotlib.pyplot as plt 

# Leer el archivo de datos
ruta_del_archivo = 'data/viviendas_web.xlsx'
#df=pd.read_excel('data/viviendas_web.xlsx', sheet_name='Sheet1')
arbol = pd.read_excel(ruta_del_archivo, sheet_name="viviendas_web")

# Preprocesamiento de datos
label_encoder = preprocessing.LabelEncoder()
arbol["Tipo_vivienda"]= label_encoder.fit_transform(arbol["Tipo_vivienda"])
prueba_arbol = arbol[["Habitantes (2022)","Rating","ICA","Tipo_vivienda","Precio","Superficie","Habitaciones","Baños","Comprado"]]

# Dividir conjunto de datos en entrenamiento y prueba
feature_cols = ["Habitantes (2022)","Rating","ICA","Precio","Superficie","Habitaciones","Baños","Comprado"]
X = prueba_arbol[feature_cols]
y = prueba_arbol['Tipo_vivienda']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar el modelo de árbol de decisión
clf_entropy = DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf_entropy = clf_entropy.fit(X_train, y_train)

# Predecir valores de prueba
y_pred = clf_entropy.predict(X_test)

# Calcular y mostrar la precisión
accuracy = metrics.accuracy_score(y_test, y_pred)
st.write("Accuracy:", accuracy)

# Definir los nombres de las clases
class_names_str = [str(class_) for class_ in clf_entropy.classes_]


# Visualizar el árbol de decisión
plt.figure(figsize=(12, 8))
plot_tree(clf_entropy, filled=True, feature_names=feature_cols, class_names=class_names_str)
plt.title("Decision Tree")
plt.xlabel("Features")
plt.ylabel("Classes")
st.pyplot()  # Mostrar el gráfico en la aplicación web
