import pandas as pd
from train import train

ips = [
    ["75.174.31.107", "Boise, ID"],
    ["97.117.140.93", "Salt Lake City, UT"],
    ["136.36.62.167", "Provo, UT"],
    ["174.52.180.239", "Sandy, UT?"],

    ["66.219.235.31","Provo, UT"],
    ["66.219.235.215", "Provo, UT"],
    ["66.219.236.117", "Provo, UT"],
    ["69.73.60.141", "Alabama?"],
    ["72.160.10.9", "Kalispell, MT"],
    ["76.8.213.221", "Provo, UT"],
    ["76.8.213.231", "Provo, UT"],


    ["136.36.203.65", "Provo, UT"],
    ["byu.edu", "Provo, UT"],
]

#read data from each of the parsed csv files
data = []
for ip in ips:
    data.append(pd.read_csv('../parsed_data_2/' + ip[0] + '.csv'))

def analyze():
    file = open('./trained_dat', 'a')
    file.truncate(0)
    for i in range(len(data)):
        file.write('trained information for ' + ips[i][0] + '\n\n')
        train(data[i]).to_csv(file)
        file.write('\n\n')
        # file.write(train(data[i]))


# def train(data):
#     training_data_df = pd.DataFrame()
#     traceroutes = train_traceroute(data['Traceroute'])
#     train_df = pd.DataFrame({'Traceroutes': traceroutes})
#     training_data_df = pd.concat([training_data_df, train_df], ignore_index=True)
#     return training_data_df

# def train_traceroute(traceroute):
#     traceroute_lst = []
#     for trace in traceroute:
#         if trace not in traceroute_lst:
#             traceroute_lst.append(trace)
#     return traceroute_lst

analyze()