from prepareData import prepare_data
import pandas as pd
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle

parser = argparse.ArgumentParser()
parser.add_argument('--percent', type=float, default=0.5, help='percentage of data that are false')
parser.add_argument('--size', type=int, default=100, help='size of the data group')
parser.add_argument('--binary', type=bool, default=True, help='determine whether ip numbers should be converted to binary')
args = parser.parse_args()

percent = args.percent
size = args.size

binary = args.binary
false_size = int(size*percent)
true_size = int(size-false_size)

ips = [
    "66.219.235.31",
    "66.219.235.215",
    "66.219.236.117",
    "69.73.60.141",
    "72.160.10.9",
    "75.174.31.107",
    "76.8.213.221",
    "76.8.213.231",
    "97.117.140.93",
    "136.36.62.167",
    "136.36.203.65",
    "174.52.180.239",
    "byu.edu",
]

data = [prepare_data(i, 1) for i in ips]

model_list = [
    [RandomForestClassifier(), 'random_forest.txt'], 
    [LogisticRegression(), 'logistic_regression.txt'], 
    [DecisionTreeClassifier(), 'decision_tree.txt'],
    ]

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

def model_data(model, file, true_df, false_df):

    X_train, y_train, X_test, y_test = collect_data(true_df, false_df)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    class_report = classification_report(y_test, predictions)
    acc_score = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)

    file.write('\n\nClassification Report: \n')
    file.write(class_report)
    file.write('\nAccuracy: ' + str(acc_score))
    file.write('\n')
    file.write('\nTrue Negatives: ' + str(conf_matrix[0][0]))
    file.write('\nFalse Positives: ' + str(conf_matrix[0][1]))
    file.write('\nTrue Positives: ' + str(conf_matrix[1][1]))
    file.write('\nFalse Negatives: ' + str(conf_matrix[1][0]))

def run():
    for model in model_list:
        file = open('./mL_outcomes/' + model[1], 'w')
        for i in range(len(data)):
            data[i]['Accurate'] = [1]*len(data[i].index)
            true_df = data[i]
            false_df = pd.DataFrame()
            for j in range(len(data)):
                ip_i = ips[i].split('.')
                ip_j = ips[j].split('.')
                if ip_j[0:2] != ip_i[0:2]:
                    data[j]['Accurate'] = [0]*len(data[j]['Accurate'])
                    false_df = pd.concat([false_df, data[j]], ignore_index=True)
                else:
                    continue
            file.write('-'*56)
            file.write('\nTesting IP Address: ' + ips[i])
            file.write('\nTraining data has a size of ' + str(size) + ' and has ' + 
                str(percent*100) + '% false data\n')
            model_data(model[0], file, true_df, false_df)
            file.write('\n\n')

        file.close()

run()
