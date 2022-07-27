from prepare import prepare_data
import pandas as pd
import numpy as np
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

parser = argparse.ArgumentParser()
parser.add_argument('--percent', type=float, default=0.5, help='percentage of data that are false')
parser.add_argument('--size', type=int, default=100, help='size of the data group')
args = parser.parse_args()

percent = args.percent
size = args.size

false_size = int(size*percent)
true_size = int(size-false_size)

# true_data = '../data/66.219.235.31.txt'
# false_data = [
#     '../data/byu.edu.txt',
#     '../data/66.219.235.215.txt',
#     '../data/66.219.236.117.txt',
#     '../data/69.73.60.141.txt',
#     '../data/72.160.10.9.txt',
#     '../data/75.174.31.107.txt',
#     '../data/76.8.213.221.txt',
#     '../data/76.8.213.231.txt',
#     '../data/97.117.140.93.txt',
#     '../data/136.36.62.167.txt',
#     '../data/136.36.203.65.txt',
#     '../data/174.52.180.239.txt',
# ]

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


def collect_data(true_data, false_data):
    true_X, true_y = prepare_data(true_data, True)
    false_X = np.array([])
    false_y = np.array([])

    for data in false_data:
        new_X, new_y = prepare_data(data, False)
        np.append(false_X, new_X)
        np.append(false_y, new_y)
    
    false_X = shuffle(false_X)
    false_y = shuffle(false_y)

    true_X = shuffle(true_X)
    true_y = shuffle(true_y)

    X_train = np.append(true_X[:true_size], false_X[:false_size])
    y_train = np.append(true_y[:true_size], false_y[:true_size])

    X_test = np.append(true_X[true_size:], false_X[false_size:])
    y_test = np.append(true_y[true_size:], false_y[false_size:])

    X_train = shuffle(X_train)
    y_train = shuffle(y_train)

    X_test = shuffle(X_test)
    y_test = shuffle(y_test)

    false_df = shuffle(false_df)
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
    
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    score = classification_report(y_test, predictions)
    print(score)
    print(accuracy_score(y_test, predictions))
    print()
    print(confusion_matrix(y_test, predictions))

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
