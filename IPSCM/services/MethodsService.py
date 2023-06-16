import json
import numpy as np
from sklearn.svm import SVR, LinearSVR, NuSVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler


def applyMethod(data_train, data_test, method, metrics, algorithms, ks_range, kernel, cs, gammas, nus, Is, description):
    match method:
        case "WKNN":
            return applyWKNNmethod(data_train, data_test, metrics, algorithms, ks_range, description)
        case "SVR":
            return applySVRmethod(data_train, data_test, kernel, cs, gammas, description)
        case "NuSVR":
            return applyNuSVRmethod(data_train, data_test, kernel, cs, gammas, nus, description)
        case "LinearSVR":
            return applyLinearSVRmethod(data_train, data_test, Is, cs, description)


def applyWKNNmethod(data_train, data_test, metric, algorithm, ks_range, description):
    keyName = getKeyDescription(description)

    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    for i in range(ks_range[0], ks_range[1] + 1):
        regressor = KNeighborsRegressor(n_neighbors=i, weights=lambda distances: 1 / distances,
                                        metric=metric, algorithm=algorithm)
        regressor.fit(X_train, y_train)

        X_test = data_test[:, :-3]
        y_pred = regressor.predict(X_test).tolist()
        newKeyName = keyName + f'[k={str(i)}]'
        results[newKeyName] = y_pred

    return results

def applySVRmethod(data_train, data_test, kernel, cs, gammas, description):
    keyName = getKeyDescription(description)

    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(data_test[:, :-3])

    for c in cs:
        if isinstance(gammas, list):
            for gamma in gammas:
                model = SVR(kernel=kernel, C=c, gamma=gamma)
                wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                y_pred = wrapper.predict(X_test)
                y_pred_list = y_pred.tolist() 

                newKeyName = keyName + f'[k={f"C{c}_G{gamma}"}]'
                results[newKeyName] = y_pred_list
        else:
            model = SVR(kernel=kernel, C=c, gamma=gammas)
            wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

            y_pred = wrapper.predict(X_test)
            y_pred_list = y_pred.tolist() 

            newKeyName = keyName + f'[k={f"C{c}_G{gamma}"}]'
            results[newKeyName] = y_pred_list

    return results


def applyNuSVRmethod(data_train, data_test, kernel, cs, gammas, nus, description):
    keyName = getKeyDescription(description)

    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(data_test[:, :-3])

    for nu in nus:
        for c in cs:
            if isinstance(gammas, list):
                for gamma in gammas:
                    model = NuSVR(nu=nu, kernel=kernel, C=c, gamma=gamma)
                    wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                    y_pred = wrapper.predict(X_test)
                    y_pred_list = y_pred.tolist()

                    newKeyName = keyName + f'[k={f"nu{nu}_C{c}_G{gamma}"}]'
                    results[newKeyName] = y_pred_list
            else:
                model = NuSVR(nu=nu, kernel=kernel, C=c, gamma=gammas)
                wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                y_pred = wrapper.predict(X_test)
                y_pred_list = y_pred.tolist()
                newKeyName = keyName + f'[k={f"nu{nu}_C{c}_G{gamma}"}]'
                results[newKeyName] = y_pred_list

    return results
                   
def applyLinearSVRmethod(data_train, data_test, Is, cs, description):
    keyName = getKeyDescription(description)

    X_train = data_train[:, :-3]
    y_train = data_train[:, -3:]

    results = {} 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(data_test[:, :-3])


    for i in Is:
        for c in cs:
                model = LinearSVR(C=c, max_iter=i, random_state=0)
                wrapper = MultiOutputRegressor(model).fit(X_train, y_train)

                y_pred = wrapper.predict(X_test)
                y_pred_list = y_pred.tolist()

                newKeyName = keyName + f'[k={f"i{i}_C{c}"}]'
                results[newKeyName] = y_pred_list

    return results

def calculate_error(aleMatrix, results):

    y_test = aleMatrix[:, -3:]
    errors = {}

    for k, y_pred in results.items():   
        error = np.sqrt(np.sum((y_test - y_pred) ** 2, axis=1))
        mean_error_rounded = round(np.mean(error), 3)
        newKeyName = f'{str(k)}[Mean={str(mean_error_rounded)}]'
        errors[newKeyName] = error

    errorsList = {k: sorted(v) for k, v in errors.items()}
        
    return errorsList


def getKeyDescription(description):
    key = json.loads(description)
    keyName = ''

    for field, value in key.items():
        if value != [None] and value != 0 and field != 'ksRange' and field != 'cs' and field != 'Is' and field != 'nus' and field != 'gammas':
            keyName += f'[{value}]'
    
    return keyName