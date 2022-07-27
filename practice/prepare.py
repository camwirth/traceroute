from inspect import trace
import pandas as pd
import math

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
    # single_traceroute = traceroute[-1:]
    # if single_traceroute[0] == '*' or single_traceroute[0] == "":
    #     return float(-1)
    # else:
    #     return float(single_traceroute[0].replace('.', ''))
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
    # single_delay = delay[-1:]
    # if single_delay[0] == "" or single_delay[0] == "*":
    #     return float(-1)
    # else:
    #     return float(single_delay[0])

def parse_latency(latency):
    return float(latency)

def parse_ttl(ttl):
    return float(ttl)

def prepare_data(name, accurate):
    file_path = name
    i = 0
    csv_data = pd.read_csv(
        file_path,
        sep="\t",
        names=["Date", "TTL", "Traceroute", "Delay", "Latency"])

    traceroute_list = [[], [], [], [], []]
    delay_list = [[], [], [], [], []]
    latency_list = []
    accuracy = []
    ttl_list = []
    csv_data["Traceroute"] = csv_data["Traceroute"].str.split(" ")
    csv_data["Delay"] = csv_data["Delay"].str.split(" ")

    for index in csv_data.index:
        ttl = parse_ttl(csv_data.loc[index, "TTL"])
        traceroute = parse_traceroute(csv_data.loc[index, "Traceroute"])
        delay = parse_delay(csv_data.loc[index, "Delay"])
        latency = parse_latency(csv_data.loc[index, "Latency"])

        if(not math.isnan(latency) and traceroute != 'ERROR' and delay != 'ERROR'):
            ttl_list.append(ttl)
            for i in range(len(traceroute_list)):
                traceroute_list[i].append(traceroute[i])
            for i in range(len(delay_list)):
                delay_list[i].append(delay[i])
            latency_list.append(latency)
            accuracy.append(accurate)
        else:
            continue

    data_dictionary = {
        "TTL": ttl_list, 'TR1': traceroute_list[0],
        'TR2': traceroute_list[1], 'TR3': traceroute_list[2],
        'TR4': traceroute_list[3], 'TR5': traceroute_list[4],
        "Delay1": delay_list[0], "Delay2": delay_list[1], "Delay3": delay_list[2],
        "Delay4": delay_list[3], "Delay5": delay_list[4],
         "Latency": latency_list, "Accurate": accuracy}
    return pd.DataFrame(data_dictionary)