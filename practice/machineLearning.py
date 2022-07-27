import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def combine_data(file_name_array):
    good_traceroute = []
    bad_traceroute = []
    good_delay = []
    bad_delay = []
    good_latency =[]
    bad_latency = []
    good_accuracy = []
    bad_accuracy = []

    for file_name in file_name_array:

        df = pd.read_csv(file_name)
        if(df['Accuracy'] == True):
            good_traceroute.append(df['Traceroute'])
            good_delay.append(df['Delay'])
            good_latency.append(df['Latency'])
            good_accuracy.append(df['Accuracy'])
        else:
            bad_traceroute.append(df['Traceroute'])
            bad_delay.append(df['Dealy'])
            bad_latency.append(df['Latency'])
            bad_accuracy.append(df['Accuracy'])

    random.shuffle(bad_traceroute)
    random.shuffle(bad_delay)
    random.shuffle(bad_latency)

    if(len(good_traceroute) == len(good_delay) and len(good_delay) == len(good_latency)):
        length = len(good_traceroute)
        bad_traceroute = bad_traceroute[:length]
        bad_delay = bad_delay[:length]
        bad_latency = bad_latency[:length]
        bad_accuracy = bad_accuracy[:length]
    else:
        print("Error: lists are not all of the same length")
        exit

    total_traceroute = good_traceroute.append(bad_traceroute)
    total_delay = good_delay.append(bad_delay)
    total_latency = good_latency.append(bad_latency)
    total_accuracy = good_accuracy.append(bad_accuracy)

    random.shuffle(total_traceroute)
    random.shuffle(total_delay)
    random.shuffle(total_latency)
    random.shuffle(total_accuracy)

    machine_learning_dict = {'Traceroute': total_traceroute, 'Delay': total_delay, 'Latency': total_latency, 'Accuracy': total_accuracy}
    machine_learning_df = pd.DataFrame(machine_learning_dict)
    
    X = machine_learning_df.drop['Accuracy']
    y = machine_learning_df['Accuracy']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    #try classification model
    score = accuracy_score(y_test, predictions)
    print(score)