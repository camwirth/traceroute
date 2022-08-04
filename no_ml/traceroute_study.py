from parse_data import parse_files
import pandas as pd
import numpy as np
#find a way to compare the ip addresses -- can you count how often they each occur and which ones need to be used? 

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

data = [parse_files(ip) for ip in ips]

for i in range(len(data)):
    print(ips[i])
    data[i].drop(data[i].index[100:], inplace=True)

    traceroute = data[i]['Traceroute']
    valid_routes = []
    for idx, name in enumerate(traceroute.value_counts().index.tolist()):
        if traceroute.value_counts()[idx]/len(traceroute) > 0.4:
            valid_routes.append(name)
    print(valid_routes)
        # print('Name: ', name)
        # print(type(name))
        # print('Counts: ', traceroute.value_counts()[idx])
    # count = data[i]['Traceroute'].value_counts().index.to_list()
    # print(count)
    # print(type(count))
    # print(count.loc[])

    # traces = []
    # for i in range(5):
    #     traces.append(pd.DataFrame())
    #     traces[i]['IP'] = []
    #     traces[i]['Count'] = []


    # traceroute_lst = []
    # count = []
    # total = 0

    # for trace in traceroute:
    #     if trace not in traceroute_lst:
    #         traceroute_lst.append(trace)
    #         count.append(1)
    #     else:
    #         i = traceroute_lst.index(trace)
    #         count[i] += 1
        
    # for i in range(len(count)):
    #     print(count[i]/len(traceroute))
    #     if count[i]/len(traceroute) > 0.4:
    #         traceroute.pop(i)
    #         count.pop(i)
            
    # df = pd.DataFrame({'traceroute': traceroute_lst, 'count': count})
    # print(df)
    print('--------')


    

    