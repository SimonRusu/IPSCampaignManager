import re
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.multioutput import RegressorChain
from sklearn.preprocessing import StandardScaler


def applyMethod(data_train, data_test, method, ks_range):
    match method:
        case "WKNN":
            return applyWKNNmethod(data_train, data_test, ks_range)
        case "SVR":
            return applySVRmethod(data_train, data_test, ks_range)
        case "NuSVR":
            aplicado3()
        case "LinearSVR":
            aplicado4()


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

def applySVRmethod():
    print("2")

def aplicado3():
    print("3")

def aplicado4():
    print("4")

 
