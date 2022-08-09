from prepareData import prepare_data
import pandas as pd
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle

#from command line get arguments to determine size and percentage of true to false data in training set
parser = argparse.ArgumentParser()
parser.add_argument('--percent', type=float, default=0.5, help='percentage of data that are false')
parser.add_argument('--size', type=int, default=100, help='size of the data group')
args = parser.parse_args()

percent = args.percent
size = args.size

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

#parse the data correctly for machine learning algorithm
data = [prepare_data(i) for i in ips]

#run program through 3 different machine learning algorithms 
model_list = [
    [RandomForestClassifier(), 'random_forest.txt'], 
    [LogisticRegression(), 'logistic_regression.txt'], 
    [DecisionTreeClassifier(), 'decision_tree.txt'],
    ]

#function recieves dataframe determined as true and dataframe as false
#returns the X and y for train and test data
def collect_data(true_df, false_df):
    false_df = shuffle(false_df)
    train_df = shuffle(true_df)

    #correct size is determined for the true and false data
    train_df = pd.concat([true_df.iloc[:true_size], false_df.iloc[:false_size]])
    test_df = pd.concat([true_df.iloc[true_size:], false_df.iloc[false_size:]])
    train_df = shuffle(train_df)
    test_df = shuffle(test_df)

    #X and y are determined for train and test data
    X_train = train_df['Data'].to_list()
    y_train = train_df['Accurate'].to_list()
    X_test = test_df['Data'].to_list()
    y_test = test_df['Accurate'].to_list()

    #X for train and test data are scaled
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    #return necessary data for machine learning algorithm
    return X_train, y_train, X_test, y_test

#model recieves model to be used, file to be printed to, and the dataframe determined as
#true and false
def model_data(model, file, true_df, false_df):
    #gather necessary information for machine learning algorithm
    X_train, y_train, X_test, y_test = collect_data(true_df, false_df)

    #fit model and predict test
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    #gather necessary data 
    class_report = classification_report(y_test, predictions)
    acc_score = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)

    #print results to file
    file.write('\n\nClassification Report: \n')
    file.write(class_report)
    file.write('\nAccuracy: ' + str(acc_score))
    file.write('\n')
    file.write('\nTrue Negatives: ' + str(conf_matrix[0][0]))
    file.write('\nFalse Positives: ' + str(conf_matrix[0][1]))
    file.write('\nTrue Positives: ' + str(conf_matrix[1][1]))
    file.write('\nFalse Negatives: ' + str(conf_matrix[1][0]))

#run all machine learning models
def run():
    #go through each model
    for model in model_list:
        #open correct file to write to 
        file = open('./mL_outcomes/' + model[1], 'w')
        #determine each dataset representing a certain ip as true
        for i in range(len(data)):
            data[i]['Accurate'] = [1]*len(data[i].index)
            true_df = data[i]
            false_df = pd.DataFrame()

            #determine all others to be false 
            #find a way here to not include data in local area as false data
            for j in range(len(data)):
                if ips[j] != ips[i]:
                    data[j]['Accurate'] = [0]*len(data[j]['Accurate'])
                    false_df = pd.concat([false_df, data[j]], ignore_index=True)

            #write information about true ip to the file
            file.write('-'*56)
            file.write('\nTesting IP Address: ' + ips[i])
            file.write('\nTraining data has a size of ' + str(size) + ' and has ' + 
                str(percent*100) + '% false data\n')
            model_data(model[0], file, true_df, false_df)
            file.write('\n\n')

        file.close()

run()
