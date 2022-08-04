from train import train
from test_traceroute import test_trace, test_trace_verbose
import pandas as pd

ips = [
    ["75.174.31.107", "Boise, ID"],
    ["66.219.235.31","Provo, UT"],
    ["66.219.235.215", "Provo, UT"],
    ["66.219.236.117", "Provo, UT"],
    ["69.73.60.141", "Alabama?"],
    ["72.160.10.9", "Kalispell, MT"],

    ["76.8.213.221", "Provo, UT"],
    ["76.8.213.231", "Provo, UT"],
    ["97.117.140.93", "Salt Lake City, UT"],
    ["136.36.62.167", "Provo, UT"],
    ["136.36.203.65", "Provo, UT"],
    ["174.52.180.239", "Sandy, UT?"],
    ["byu.edu", "Provo, UT"],
]

data = []
for ip in ips:
    data.append(pd.read_csv('../parsed_data/' + ip[0] + '.csv'))

provo_data = pd.read_csv('../parsed_data/66.219.235.215.csv')
boise_data = pd.read_csv('../parsed_data/75.174.31.107.csv')

total_data = pd.concat([boise_data, provo_data], ignore_index=True)


def simmulate():
    for i in range(len(data)):
        starting_ip = ips[i]
        starting_data = data[i]
        print()
        print('Starting ', starting_ip)
        print()
        for j in range(len(data)):
            if ips[i] != ips[j]:
                moved_ip = ips[j]
                moved_data = data[j]
                string = 'Moving from: ' + starting_ip[0] + ' Located in ' + starting_ip[1]
                print('-'*len(string))
                print('Moving from: ' + starting_ip[0] + ' Located in ' + starting_ip[1])
                print('... to ' + moved_ip[0] + ' Located in ' + moved_ip[1])
                print()
                total_data = pd.concat([starting_data, moved_data], ignore_index=True)
                run_all_tests(total_data, starting_ip[0], moved_ip[0])

def run_all_tests(total_data, starting_ip, moving_ip):
    if(len(total_data) < 200):
        print('Could not detect move')
        print()
        return
    m_ip = starting_ip
    train_data = total_data[0:99]
    test_data = total_data[100:199]
    trained_df = train(train_data)
    predicted_move = test_trace(trained_df, test_data)
    has_moved = False

    for idx, ip in enumerate(test_data['IP'].value_counts().index.tolist()):
        count = test_data['IP'].value_counts()[idx]
        # print('starting_ip ', starting_ip)
        # print('ip ', ip)
        if ip != starting_ip:
            m_ip = ip
            if count/len(test_data) > 0.00:
                # print('I think it may have worked')
                has_moved = True

    # if has_moved is False and predicted_move is True:
    #     print('False Negative')
    # elif has_moved is True and predicted_move is False:
    #     print('False Positive')
    # elif has_moved is False and predicted_move is False:
    #     print('True Negative')
    # else:
    #     print('True Positive')

    if predicted_move:
        print('The Sesor has moved locations')

        if predicted_move != has_moved:
            print('trained')
            print(train_data)
            print(trained_df)
            print('test failed, starting ip: ' + starting_ip)
            print('moved ip: ' + moving_ip)
            print(m_ip)
            test_trace_verbose(trained_df, test_data)

        if has_moved:
            print('Prediction was correct')
        else:
            print('Prediction was false')
        print()
        return

    total_data = total_data.tail(-50)
    total_data = total_data.reset_index(drop=True)
    run_all_tests(total_data, starting_ip, moving_ip)


# run_all_tests(total_data, ips[1][0])

simmulate()