from sklearn.neighbors import KNeighborsRegressor

def applyMethod(data_train, data_test, method, ks_range):
    match method:
        case "WKNN":
            return applyWknnMethod(data_train, data_test, ks_range)
        case "SVR":
            aplicado2()
        case "NuSVR":
            aplicado3()
        case "LinearSVR":
            aplicado4()


def applyWknnMethod(data_train, data_test, ks_range):
    # Separar los datos de entrenamiento en características (X_train) y etiquetas (y_train)
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]
        
    metric = 'euclidean' # métrica de distancia

    # Crear un arreglo vacío para almacenar los resultados
    results = {}

    # Entrenar y evaluar el modelo para cada valor de k
    for i in range(ks_range[0], ks_range[1] + 1):
        # Entrenar el modelo de regresión wKNN con peso w igual a la inversa de la distancia Euclidiana
        regressor = KNeighborsRegressor(n_neighbors=i, weights=lambda distances: 1 / distances,
                                        metric=metric, algorithm='brute')
        regressor.fit(X_train, y_train)

        # Predecir los puntos desconocidos
        X_test = data_test[:, :-3]
        y_pred = regressor.predict(X_test).tolist()

        # Agregar las coordenadas predichas al arreglo de resultados
        results[str(i)] = y_pred

    return results

def aplicado2():
    print("2")

def aplicado3():
    print("3")

def aplicado4():
    print("4")

 
