from inspect import trace
import pandas as pd
import math
import numpy as np

def parse_traceroute(traceroute):
    traceroutes = []
    if(len(traceroute) < 5):
        return 'ERROR'
    else:
        last_5_traceroutes = traceroute[-5:]
    
    for ip in last_5_traceroutes:
        ip = ip.replace("*", "-1")
        
        if(ip == ''):
            traceroutes.append(float(-1))
        else:
            traceroutes.append(float(ip.replace(".", "")))
    return traceroutes

def parse_delay(delay):
    delays = []
    if(len(delay) < 5):
        return 'ERROR'
    else:
        last_5_delays = delay[-5:]

    for delay in last_5_delays:
        if(delay == ''):
            delays.append(float(-1))
        else:
            delays.append(float(delay.replace("*", "-1")))
    return delays

def parse_latency(latency):
    return float(latency)

def parse_ttl(ttl):
    return float(ttl)

def prepare_data(name, accurate):
    lst = np.array([])
    accuracy = np.array([])
    file_path = name
    csv_data = pd.read_csv(
        file_path,
        sep="\t",
        names=["Date", "TTL", "Traceroute", "Delay", "Latency"])

    csv_data["Traceroute"] = csv_data["Traceroute"].str.split(" ")
    csv_data["Delay"] = csv_data["Delay"].str.split(" ")

    for index in csv_data.index:
        ttl = parse_ttl(csv_data.loc[index, "TTL"])
        traceroute = parse_traceroute(csv_data.loc[index, "Traceroute"])
        delay = parse_delay(csv_data.loc[index, "Delay"])
        latency = parse_latency(csv_data.loc[index, "Latency"])

        if(not math.isnan(latency) and traceroute != 'ERROR' and delay != 'ERROR'):
            np.append(lst, ttl)
            for tr in traceroute:
                np.append(lst, tr)
            for d in delay:
                np.append(lst, d)
            np.append(lst, latency)
            np.append(accuracy, accurate)
        else:
            continue
    return lst, accuracy