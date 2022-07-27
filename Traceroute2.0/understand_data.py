from prepareData import prepare_data
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

true_size = 50
false_size = 50

ips = [
    "66.219.235.31", #provo
    "66.219.235.215", #provo
    "66.219.236.117", #provo
    "69.73.60.141", #alabama
    "72.160.10.9", #montana
    "75.174.31.107", #century link, idaho
    "76.8.213.221", #sandy
    "76.8.213.231", #sandy
    "97.117.140.93", #century link, salt lake
    "136.36.62.167", #google fiber, provo
    "136.36.203.65", #google fiber, provo
    "174.52.180.239", #comcast, provo
    "byu.edu",
]

#notes
#
#

data = [prepare_data(i, 1) for i in ips]

def collect_data(true_df, false_df):
    false_df = shuffle(false_df)
    train_df = pd.concat([true_df.iloc[:true_size], false_df.iloc[:false_size]])
    test_df = pd.concat([true_df.iloc[true_size:], false_df.iloc[false_size:]])
    train_df = shuffle(train_df)
    test_df = shuffle(test_df)

    X_train = train_df['Data'].to_list()
    y_train = train_df['Accurate'].to_list()
    X_test = test_df['Data'].to_list()
    y_test = test_df['Accurate'].to_list()

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    return X_train, y_train, X_test, y_test

def run_comp():
    for i in range(len(data)):
        print(ips[i])
        if ips[i] ==  '136.36.62.167':
            data[i]['Accurate'] = [1]*len(data[i].index)
            true_df = data[i]
            false_df = pd.DataFrame()
            for j in range(len(data)):
                ip_i = ips[i].split('.')
                ip_j = ips[j].split('.')
                if ip_j[0:2] != ip_i[0:2]:
                    print(ips[j])
                    print('true')
                    print(true_df)
                    print('false')
                    print(data[j])
                    print()
                    data[j]['Accurate'] = [0]*len(data[j]['Accurate'])
                    false_df = pd.concat([false_df, data[j]], ignore_index=True)
                else:
                    continue
            X_train, y_train, X_test, y_test = collect_data(true_df, false_df)
            print(X_test)
            model = LogisticRegression()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            compare_train_test(X_test, y_test, predictions)
        else:
            continue

def compare_train_test(X_test, y_test, predictions):
    false_negative = 0
    false_positive = 0
    true_positive = 0
    true_negative = 0
    for i in range(len(y_test)):
        if y_test[i] == 1 and predictions[i] == 0:
            false_negative += 1
        if y_test[i] == 0 and predictions[i] == 1:
            false_positive += 1
        if y_test[i] == 1 and predictions[i] == 1:
            true_positive += 1
        if y_test[i] == 0 and predictions[i] == 0:  
            true_negative += 1

    print(false_positive)
    print(false_negative)
    print(true_positive)
    print(true_negative)

        # if y_test[i] != predictions[i]:
        #     print('Failure at ', i)
        #     print('X-Test Value:')
        #     print(X_test[i])
        #     print('Prediction: ')
        #     print(predictions[i])
        #     print('Actual: ')
        #     print(y_test[i])
        #     print()

run_comp()