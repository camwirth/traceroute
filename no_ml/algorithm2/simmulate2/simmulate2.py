from train2 import train
from test2 import test_trace
import pandas as pd

ips = [
    ["75.174.31.107", "Boise, ID"],
    ["136.36.62.167", "Provo, UT"],
    ["174.52.180.239", "Sandy, UT?"],

    ["66.219.235.31","Provo, UT"],
    ["66.219.235.215", "Provo, UT"],
    ["66.219.236.117", "Provo, UT"],
    ["69.73.60.141", "Alabama?"],
    ["72.160.10.9", "Kalispell, MT"],
    ["76.8.213.221", "Provo, UT"],
    ["76.8.213.231", "Provo, UT"],
    ["97.117.140.93", "Salt Lake City, UT"],

    ["136.36.203.65", "Provo, UT"],
    ["byu.edu", "Provo, UT"],
]

#read data from each of the parsed csv files
data = []
for ip in ips:
    data.append(pd.read_csv('../parsed_data2/' + ip[0] + '.csv', index_col=False))

#function runs the simmulation
def simmulate():
    for i in range(len(data)):
        #open file and write information about the "starting ip" address
        file = open('../simmulated_data2/' + ips[i][0], 'w')
        file.write('Information for ' + ips[i][0] + ' Located in: ' + ips[i][1])
        file.write('\n\n')

        #determine the "starting" ip address
        starting_ip = ips[i]
        starting_data = data[i]
        
        #run through each other ip address as the "moved" ip address
        for j in range(len(data)):
            if ips[i] != ips[j]:
                moved_ip = ips[j]
                moved_data = data[j]

                file.write('-'*56)
                file.write('\nMoving to: ' + moved_ip[0] + ' Located in ' + moved_ip[1] + '\n')

                #concatenate moved ip's data to starting ip's data and run tests
                total_data = pd.concat([starting_data, moved_data], ignore_index=True)
                result_df = pd.DataFrame()
                run_all_tests(total_data, starting_ip, moved_ip, file, result_df)


def run_all_tests(total_data, starting_ip, moving_ip, file, result_df):
    #check that dataframe is greater then 200
    if(len(total_data) < 200):
        # if test has made it to the end of the dataframe, the move was not detected 
        file.write('Move was not detected...\n\n')
        print_results(result_df, file)
        return

    #set the first 100 data points as training data and test the next 100 data points
    train_data = total_data[0:100]
    test_data = total_data[100:200]

    #use training algorithm to train the data and test if the ip address has moved
    trained_df = train(train_data)
    predicted_move = test_trace(trained_df, test_data)
    has_moved = False

    #if an ip address in the test_data exists that is not the starting ip address
    # the device has moved
    for idx, ip in enumerate(test_data['IP'].value_counts().index.tolist()):
        count = test_data['IP'].value_counts()[idx]
        if ip != starting_ip[0]:
            if count/len(test_data) > 0.1:
                has_moved = True

    #if the test has predicted that the device has moved
    if predicted_move:
        file.write('The Sensor has moved from ' + starting_ip[1] + ' to ' + moving_ip[1] + '\n')

        #check if the device has not actually moved
        if predicted_move != has_moved:
            file.write("The test predicted a False Move\n\n")
            result = pd.DataFrame({'Moved IP': [moving_ip[0]], 'Result': ['False Postitve']})
        else:
            file.write('The test predicted a True Move!\n\n')
            result = pd.DataFrame({'Moved IP': [moving_ip[0]], 'Result': ['True Postitve']})
        
        result_df = pd.concat([result_df, result], ignore_index=True)
        print_results(result_df, file)
        return

    else:
        if has_moved:
            result = pd.DataFrame({'Moved IP': [moving_ip[0]], 'Result': ['False Negative']})
        else:
            result = pd.DataFrame({'Moved IP': [moving_ip[0]], 'Result': ['True Negative']})
        result_df = pd.concat([result_df, result], ignore_index=True)

    #remove the first 50 data points from the dataframe 
    total_data = total_data.tail(-50)
    total_data = total_data.reset_index(drop=True)

    #recursively run tests again
    run_all_tests(total_data, starting_ip, moving_ip, file, result_df)

def print_results(result_df, file):
    file.write('---RESULTS---\n')
    for idx, result in enumerate(result_df['Result'].value_counts().index.tolist()):
        count = result_df['Result'].value_counts()[idx]
        file.write(result + ": " + str(count))
        file.write('\n\n')

simmulate()