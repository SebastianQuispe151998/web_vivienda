import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import seaborn as sns
import streamlit as st

ruta_del_archivo = 'data\Dataset_final_ventas.xlsx'
#df=pd.read_excel('data/viviendas_web.xlsx', sheet_name='Sheet1')
df = pd.read_excel(ruta_del_archivo)


df = df.dropna().reset_index()


df[['Precio', 'Superficie', 'Habitaciones', 'Baños', 'Zona_binaria', 'PMZona', 'PMm²Zona', 'RMP', 'RMH']].describe()

df['Tipo_vivienda'].value_counts()

from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder

enc = OneHotEncoder(handle_unknown='error')
df=df.join(pd.DataFrame(enc.fit_transform(df[['Tipo_vivienda']]).toarray(), columns=['Casa', 'Chalet', 'Piso']), how='right') ## 2 valores que OneHotEncoder falla asique hacemos el join a la dcha y se eliminan
#df


#"""Correlaciones entre las features"""

column_features = ['Superficie', 'Habitaciones', 'Baños', 'Zona_binaria', 'PMZona', 'PMm²Zona', 'RMP', 'RMH', 'Casa', 'Chalet', 'Piso']
target = 'Precio'

import seaborn as sns
import matplotlib.pyplot as plt

# Generate a large random dataset
# Compute the correlation matrix
corr = df[column_features].corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, annot=True, mask=mask, cmap=cmap, vmax=1.0, vmin=-1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

X = df[list(column_features)]
y = df[target]

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

#Escalamos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test) # SOLO HAY QUE ESCALAR LAS Xs

sns.boxplot(x='Tipo_vivienda', y='Precio', data=df)

#"""Correlaciones entre Precio-Features"""

#column_features

total_columns=['Superficie', 'Habitaciones', 'Baños', 'Zona_binaria', 'PMZona', 'PMm²Zona', 'RMP', 'RMH', 'Casa', 'Chalet', 'Piso']

total_columns[len(total_columns)-1]=target

#total_columns

df_correlation_target = df[total_columns].corr().sort_values(by='Precio', ascending=False)[['Precio']]
sns.heatmap(df_correlation_target, vmin=-1, vmax=1, annot=True)

#column_features

"""# Modelo: LinearRegression"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV

# Create a polynomial regression pipeline
lr = LinearRegression()

# Define the parameter grid for GridSearch
param_grid = {
    'fit_intercept': [True, False]
}

# Create the GridSearchCV object
grid_search = GridSearchCV(lr, param_grid, scoring='neg_mean_squared_error', cv=5)

# Fit the GridSearchCV object to the training data
grid_search.fit(X_train_scaled, y_train)

# Get the best parameters and best model
best_model = grid_search.best_estimator_

#grid_search.best_params_

"""Evaluación del modelo"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import numpy as np
#METRICAS DEL TRAIN
y_pred = best_model.predict(X_train_scaled)

#METRICAS DEL TEST
y_pred_test = best_model.predict(X_test_scaled)
data = {
    'TRAIN' : [mean_absolute_error(y_train, y_pred), mean_squared_error(y_train, y_pred), np.sqrt(mean_squared_error(y_train, y_pred)), r2_score(y_train, y_pred), (mean_absolute_percentage_error(y_train, y_pred)*100)],
    'TEST' : [mean_absolute_error(y_test, y_pred_test), mean_squared_error(y_test, y_pred_test), np.sqrt(mean_squared_error(y_test, y_pred_test)), r2_score(y_test, y_pred_test), (mean_absolute_percentage_error(y_test, y_pred_test)*100)]
}
df_errors = pd.DataFrame(data, index=['MAE', 'MSE', 'RMSE', 'R2Score', 'MAPE'])
df_errors['Difference']=df_errors['TEST']-df_errors['TRAIN']
df_errors.T

from sklearn.model_selection import cross_val_score


def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())


scoresd = cross_val_score(best_model, X_test_scaled, y_pred_test, scoring="neg_mean_squared_error", cv=10)
scoresfinal = np.sqrt(-scoresd)

display_scores(scoresfinal)


print(f"\nTest: {best_model.score(X_test_scaled, y_pred_test)}\nTrain: {best_model.score(X_train_scaled, y_pred)}")

df[df['Zonas']=='Moratalaz'].head(3)


st.markdown(
    """<style>
        .st-ef {
            width: 150px !important;
        }
    </style>""",
    unsafe_allow_html=True
)

# Definir los widgets de entrada para cada característica
superficie = st.number_input('Superficie', value=93)
habitaciones = st.number_input('Habitaciones', value=3)
baños = st.number_input('Baños', value=2)
zona_binaria = st.number_input('Zona binaria', value=1)
pm_zona = st.number_input('PMZona', value=249681.67)
pm_m2_zona = st.number_input('PMm²Zona', value=2796.49)
rmp = st.number_input('RMP', value=15.667)
rmh = st.number_input('RMH', value=38.421)
casa = st.number_input('Casa', value=0)
chalet = st.number_input('Chalet', value=0)
piso = st.number_input('Piso', value=1)

# Crear DataFrame con los valores ingresados
X_prueba = pd.DataFrame({
    'Superficie': [superficie],
    'Habitaciones': [habitaciones],
    'Baños': [baños],
    'Zona_binaria': [zona_binaria],
    'PMZona': [pm_zona],
    'PMm²Zona': [pm_m2_zona],
    'RMP': [rmp],
    'RMH': [rmh],
    'Casa': [casa],
    'Chalet': [chalet],
    'Piso': [piso]
})

# Escalar los datos
X_prueba_scaled = scaler.transform(X_prueba)

# Predecir utilizando el modelo
predecimos = best_model.predict(X_prueba_scaled)

# Mostrar el resultado en la aplicación web
st.write('El precio predicho es: ', round(predecimos[0], 2),' €')

# si=pd.DataFrame({'Caracteristica': column_features, 'Importancia': best_model.coef_}).sort_values(by='Importancia', ascending=True)

# plt.figure(figsize=(10, 6))
# plt.barh(si['Caracteristica'], si['Importancia'], color='darkblue')
# plt.xlabel('Importancia')
# plt.ylabel('Característica')
# plt.title('Importancia de Características')
# plt.show()

# best_model.coef_