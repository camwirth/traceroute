from prepare import prepare_data
import pandas as pd
import numpy as np
import argparse
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

parser = argparse.ArgumentParser()
parser.add_argument('--percent', type=float, default=0.5, help='percentage of data that are false')
parser.add_argument('--size', type=int, default=100, help='size of the data group')
args = parser.parse_args()

percent = args.percent
size = args.size

false_size = int(size*percent)
true_size = int(size-false_size)

confusion = np.array([['TP', 'FN'], ['FP', 'TN']])

outputs = [
    '../../data/byu.edu.txt',
    '../../data/66.219.235.215.txt',
    '../../data/66.219.236.117.txt',
    '../../data/69.73.60.141.txt',
    '../../data/72.160.10.9.txt',
    '../../data/75.174.31.107.txt',
    '../../data/76.8.213.221.txt',
    '../../data/76.8.213.231.txt',
    '../../data/97.117.140.93.txt',
    '../../data/136.36.62.167.txt',
    '../../data/136.36.203.65.txt',
    '../../data/174.52.180.239.txt',
]

def print_information(train_confusion, train_classification, test_confusion, test_classification):
    # print()
    # print('For Train Data:')
    # print()
    # print('CONFUSION MATRIX')
    # print(train_confusion)
    # print()
    # print('CLASSIFICATION REPORT')
    # print(train_classification)

    print()
    print('For Test Data:')
    print()
    print('CONFUSION MATRIX')
    print(test_confusion)
    print()
    print('CLASSIFICATION REPORT')
    print(test_classification)

def count_false(y_test):
    false = 0
    true = 0
    for data in y_test:
        if data is False:
            false = false + 1
        else:
            true = true + 1
    print('FALSE ', false)
    print('TRUE', true)

def collect_data(true_data, false_data):
    true_df = prepare_data(true_data, True)
    false_df = pd.DataFrame()
    for data in false_data:
        false_df = pd.concat([false_df, prepare_data(data, False)], ignore_index=True)

    false_df = shuffle(false_df)
    print(len(false_df))
    print(len(true_df))
    train_df = pd.concat([true_df.iloc[:true_size], false_df.iloc[:false_size]])
    test_df = pd.concat([true_df.iloc[true_size:], false_df.iloc[false_size:]])
    train_df = shuffle(train_df)
    test_df = shuffle(test_df)

    X_train = train_df[['TTL', 'TR1', 'TR2', 'TR3', 'TR4', 'TR5', 
        'Delay1', 'Delay2', 'Delay3', 'Delay4', 'Delay5', 'Latency']]
    y_train = train_df['Accurate']
    X_test = test_df[['TTL', 'TR1', 'TR2', 'TR3', 'TR4', 'TR5', 
        'Delay1', 'Delay2', 'Delay3', 'Delay4', 'Delay5', 'Latency']]
    y_test = test_df['Accurate']

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    count_false(y_test)

    mlp = MLPClassifier(hidden_layer_sizes=(12,12,12),activation='relu', solver='adam', max_iter=500)
    mlp.fit(X_train, y_train)

    predict_train = mlp.predict(X_train)
    predict_test = mlp.predict(X_test)

    print_information(
        confusion_matrix(y_train, predict_train), classification_report(y_train, predict_train),
        confusion_matrix(y_test, predict_test), classification_report(y_test, predict_test))
    
def run():
    false_data = []
    for true_data in outputs:
        for data in outputs:
            if data != true_data:
                false_data.append(data)
        print()
        print(true_data)
        collect_data(true_data, false_data)

run()
#collect_data(true_data, false_data)