from prepareData import prepare_data
import pandas as pd
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
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

outputs = [
    # 'byu.edu',
    '66.219.235.215',
    # '66.219.236.117',
    # '69.73.60.141',
    '72.160.10.9',
    '75.174.31.107',
    # '76.8.213.221',
    # '76.8.213.231',
    '97.117.140.93',
    # '136.36.62.167',
    '136.36.203.65',
    '174.52.180.239',
]

#continue to do novelty and outlier detection
#also try a k map maybe?
#also the neural network
model_list = [
    [RandomForestClassifier(), 'random_forest.txt'], 
    [LogisticRegression(), 'logistic_regression.txt'], 
    [DecisionTreeClassifier(), 'decision_tree.txt'],
    ]

def count_true_false(y_test, file):
    true = 0
    false = 0
    for test in y_test:
        if test:
            true += 1
        else:
            false += 1
    file.write('\nTrue data in test set: ' + str(true))
    file.write('\nFalse data in test set: ' + str(false))

def collect_data(true_data, false_data):
    true_df = prepare_data(true_data, 1, binary)
    false_df = pd.DataFrame()
    for data in false_data:
        false_df = pd.concat([false_df, prepare_data(data, 0, binary)], ignore_index=True)

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

def model_data(model, file, true_data, false_data):

    X_train, y_train, X_test, y_test = collect_data(true_data, false_data)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    count_true_false(y_test, file)

    class_report = classification_report(y_test, predictions)
    acc_score = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)

    file.write('\n\nClassification Report: \n')
    file.write(class_report)
    file.write('\nAccuracy: ' + str(acc_score))
    file.write('\n')
    file.write('\nTrue Negatives: ' + str(conf_matrix[0][0]))
    file.write('\nFalse Negatives: ' + str(conf_matrix[0][1]))
    file.write('\nTrue Positives: ' + str(conf_matrix[1][1]))
    file.write('\nFalse Positives: ' + str(conf_matrix[1][0]))

def run():
    for model in model_list:
        file = open('./mL_outcomes/' + model[1], 'w')
        
        false_data = []
        for true_data in outputs:
            for data in outputs:
                if data != true_data:
                    false_data.append(data)
            file.write('-'*56)
            file.write('\nTesting IP Address: ' + true_data)
            file.write('\nTraining data has a size of ' + str(size) + ' and has ' + 
                str(percent*100) + '% false data\n')
            model_data(model[0], file, true_data, false_data)
            file.write('\n\n')
        
        file.close()
run()
