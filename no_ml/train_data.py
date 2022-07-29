from statistics import stdev
from statistics import mean, median
import pandas as pd
import time

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

# data = [parse_files(ip) for ip in ips]

def train_data(data):
    training_data_df = pd.DataFrame()
    for i in range(len(data)):
        min_latency, max_latency = train_latency(data[i]['Latency'].loc[len(data[i]['Latency'])-2000:len(data[i]['Latency']) - 1000])
        min_ttl, max_ttl = train_ttl(data[i]['TTL'].loc[len(data[i]['TTL'])- 2000:len(data[i]['TTL']) - 1000])
        min_delay, max_delay = train_delay(data[i]['Delay'].loc[len(data[i]['Delay']) - 2000:len(data[i]['Delay']) - 1000])
        traceroutes = train_traceroute(data[i]['Traceroute'].loc[len(data[i]['Delay']) - 2000:len(data[i]['Traceroute']) - 1000])
        train_df = pd.DataFrame({
            'IP': ips[i], 'Min-Latency': min_latency, 'Max-Latency': max_latency,
            'Min-ttl': min_ttl, 'Max-ttl': max_ttl, 'Min-delay': min_delay, 
            'Max-delay': max_delay, 'Traceroutes': traceroutes
        })
        training_data_df = pd.concat([training_data_df, train_df], ignore_index=True)
    training_data_df.to_csv('./parsed_data/training_data.csv')
    return training_data_df


def train_latency(latencies):
    latency_stdev = stdev(latencies)
    latency_mean = mean(latencies)
    min_threshold = latency_mean - 2*latency_stdev
    max_threshold = latency_mean + 2*latency_stdev
    return min_threshold, max_threshold

def train_ttl(ttl):
    ttl_stdev = stdev(ttl)
    ttl_mean = mean(ttl)
    min_threshold = ttl_mean - ttl_stdev
    max_threshold = ttl_mean + ttl_stdev
    return min_threshold, max_threshold

def train_delay(delays):
    mean_delays = []
    for delay in delays:
        mean_delays.append(mean(delay))
    delay_stdev = stdev(mean_delays)
    delay_mean = mean(mean_delays)
    min_threshold = delay_mean - delay_stdev
    max_threshold = delay_mean + delay_stdev
    return min_threshold, max_threshold

def train_traceroute(traceroute):
    traceroute_lst = []
    for trace in traceroute:
        if trace not in traceroute_lst:
            traceroute_lst.append(trace)
    return traceroute_lst
