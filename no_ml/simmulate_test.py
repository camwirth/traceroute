from parse_data import parse_files
import pandas as pd
from train_data import train
from test_data import test

ips = [
    ["66.219.235.31","Provo, UT"],
    # ["66.219.235.215", "Provo, UT"],
    # ["66.219.236.117", "Provo, UT"],
    # ["69.73.60.141", "Alabama?"],
    # ["72.160.10.9", "Kalispell, MT"],
    # ["75.174.31.107", "Boise, ID"],
    # ["76.8.213.221", "Provo, UT"],
    # ["76.8.213.231", "Provo, UT"],
    ["97.117.140.93", "Salt Lake City, UT"],
    # ["136.36.62.167", "Provo, UT"],
    # ["136.36.203.65", "Provo, UT"],
    # ["174.52.180.239", "Sandy, UT?"],
    # ["byu.edu", "Provo, UT"],
]

total_data = pd.DataFrame()
for ip in ips:
    total_data = pd.concat([total_data, parse_files(ip[0])], ignore_index=True)
results = []

def simmulate(data):
    if(len(data) < 100):
        return results
    trained_data = total_data.loc[0:99]
    test_data = total_data.loc[100:199]

    trained_data = train(trained_data)
    print(trained_data)
    moved = test(trained_data, test_data)
    results.append(moved)
    # print(data)
    # data = data.drop(trained_data.index)
    data = data.tail(-10)
    data = data.reset_index(drop=True)
    # data = data.drop(trained_data.index).reset_index()
    # data[~data.isin(trained_data)].dropna(how='all')
    # print(data)
    # data = pd.concat([data, trained_data]).drop_duplicates(keep=False)
    # data = data.reset_index()
    # print(data)
    simmulate(data)
    return results

print(simmulate(total_data))
