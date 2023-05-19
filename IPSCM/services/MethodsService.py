from sklearn.neighbors import KNeighborsRegressor
import pandas as pd


def applyMethod(data_train, data_test, method, ks_range):

    methods = {
        1: applyWknnMethod(data_train, data_test, ks_range)
    }

    methods.get(method)()
    

def applyWknnMethodAux(data_train, data_test, ks_range):
    # Separar los datos de entrenamiento en características (X_train) y etiquetas (y_train)
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    metric = 'euclidean' # métrica de distancia

    # Crear un arreglo vacío para almacenar los resultados
    results = []

    # Entrenar y evaluar el modelo para cada valor de k
    for i in range(ks_range[0], ks_range[1] + 1):
        # Entrenar el modelo de regresión wKNN con peso w igual a la inversa de la distancia Euclidiana
        regressor = KNeighborsRegressor(n_neighbors=i, weights=lambda distances: 1 / distances,
                                        metric=metric, algorithm='brute')
        regressor.fit(X_train, y_train)

        # Predecir los puntos desconocidos
        X_test = data_test[:, :-3]
        y_pred = regressor.predict(X_test)

        # Agregar las coordenadas predichas al arreglo de resultados
        results.append({'K': i, 'Points': y_pred})



def applyWknnMethod(data_train, data_test, ks_range):
 
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    metric = 'euclidean'

    ks = []
    points = []

    for i in range(ks_range[0], ks_range[1] + 1):

        regressor = KNeighborsRegressor(n_neighbors=i, weights=lambda distances: 1 / distances,
                                        metric=metric, algorithm='brute')
        regressor.fit(X_train, y_train)

        X_test = data_test[:, :-3]
        y_pred = regressor.predict(X_test)

        ks.append(i)
        points.append(y_pred)

    df_results = pd.DataFrame({'K': ks, 'Points': points})
    df_results.to_csv("Coordenadas_predichas.csv", index=False)

 
