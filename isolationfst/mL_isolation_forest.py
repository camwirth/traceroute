from xml.dom.expatbuilder import FragmentBuilderNS
from prepareData import prepare_data
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.utils import shuffle

outputs = [
    'byu.edu',
    '66.219.235.215',
    '66.219.236.117',
    '69.73.60.141',
    '72.160.10.9',
    '75.174.31.107',
    '76.8.213.221',
    '76.8.213.231',
    '97.117.140.93',
    '136.36.62.167',
    '136.36.203.65',
    '174.52.180.239',
]

def count_true_false(y_test):
    true = 0
    false = 0 
    for test in y_test:
        if test:
            true += 1
        else:
            false += 1
    print('True data in the test set: ' + str(true))
    print('False data in the test set: ' + str(false))

def collect_data(true_data, false_data):
    true_df = prepare_data(true_data, 1, 1)
    false_df = pd.DataFrame()
    for data in false_data:
        false_df = pd.concat([false_df, prepare_data(data, 0, -1)], ignore_index=True)

    false_df = shuffle(false_df)
    test_df = pd.concat([true_df, false_df])
    X_train = true_df['Data'].to_list()
    X_test = test_df['Data'].to_list()
    y_test = test_df['Accurate'].to_list()

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    model = IsolationForest()
    model.fit(X_train)
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

def run():
    false_data = []
    for true_data in outputs:
        for data in outputs:
            if data != true_data:
                false_data.append(data)

        print('-'*56)
        print('Testing IP Address: ' + true_data)
        collect_data(true_data, false_data)

run()