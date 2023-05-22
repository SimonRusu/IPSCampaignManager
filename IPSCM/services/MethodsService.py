from sklearn.svm import SVR, LinearSVR, NuSVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler


def applyMethod(data_train, data_test, method, ks_range):
    match method:
        case "WKNN":
            return applyWKNNmethod(data_train, data_test, ks_range)
        case "SVR":
            return applySVRmethod(data_train, data_test)
        case "NuSVR":
            return applyNuSVRmethod(data_train, data_test)
        case "LinearSVR":
            return applyLinearSVRmethod(data_train, data_test)


def applyWKNNmethod(data_train, data_test, ks_range):
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 
    metric = 'euclidean'

    for i in range(ks_range[0], ks_range[1] + 1):
        regressor = KNeighborsRegressor(n_neighbors=i, weights=lambda distances: 1 / distances,
                                        metric=metric, algorithm='brute')
        regressor.fit(X_train, y_train)

        X_test = data_test[:, :-3]
        y_pred = regressor.predict(X_test).tolist()

        results[str(i)] = y_pred

    return results

def applySVRmethod(data_train, data_test):
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(data_test[:, :-3])

    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    Cs = [0.01, 0.1, 0.5, 1, 2, 5]
    gammas = ['auto', 'scale', 0.01, 0.05, 0.1, 0.5]

    for kernel in kernels:
        for C in Cs:
            for gamma in gammas:
                model = SVR(kernel=kernel, C=C, gamma=gamma)
                wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                y_pred = wrapper.predict(X_test)
                y_pred_list = y_pred.tolist() 

                model_name = f"{kernel}_C{C}_G{gamma}"
                results[model_name] = y_pred_list

    return results


def applyNuSVRmethod(data_train, data_test):
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(data_test[:, :-3])

    nus = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    Cs = [0.01, 0.1, 0.5, 1, 2, 5]
    gammas = ['auto', 'scale', 0.01, 0.05, 0.1, 0.5]

    for nu in nus:
        for kernel in kernels:
            for C in Cs:
                for gamma in gammas:
                    model = NuSVR(nu=nu, kernel=kernel, C=C, gamma=gamma)
                    wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                    y_pred = wrapper.predict(X_test)
                    y_pred_list = y_pred.tolist()
                    model_name = f"nu{nu}_{kernel}_C{C}_G{gamma}"
                    results[model_name] = y_pred_list

    return results
                   
def applyLinearSVRmethod(data_train, data_test):
    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(data_test[:, :-3])

    Cs = [0.01, 0.1, 0.5, 1, 2, 5, 6, 7, 8, 9, 10, 15, 20]
    Is = [250, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12500, 15000, 20000]

    for i in Is:
        for C in Cs:
                model = LinearSVR(C=C, max_iter=i, random_state=0)
                wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                y_pred = wrapper.predict(X_test)
                y_pred_list = y_pred.tolist()

                model_name = f"i{i}_C{C}"
                results[model_name] = y_pred_list

    return results