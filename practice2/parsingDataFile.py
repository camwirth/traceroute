import pandas as pd
import math

def parse_traceroute(traceroute):
    traceroutes = []
    if(len(traceroute) < 5):
        return -1
    else:
        last_5_traceroutes = traceroute[-5:]
    
    for ip in last_5_traceroutes:
        ip = ip.replace("*", "-1")
        ip = float(ip.replace(".", ""))
        traceroutes.append(ip)

    return traceroutes

def parse_delay(delay):
    delays = []
    if(len(delay) < 5):
        return -1
    else:
        last_5_delays = delay[-5:]

    for delay in last_5_delays:
        delay = delay.replace("*", "-1")
        delay = float(delay)
        delays.append(delay)

    return delays

def parse_latency(latency):
    return float(latency)

def parse_ttl(ttl):
    return float(ttl)

def prepare_data(name, df, accurate):
    file_path = '../data/' + name + '.txt'
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

        if(len(traceroute) != 5 and len(delay) != 5):
            print("didn't work")
        if(not math.isnan(latency)):
            df.loc[len(df.index)] = [ttl, traceroute, delay, latency]
        else:
            continue
        print()
        print(df)

def main():
    name = 'byu.edu'
    dict = {'TTL': None, 'TRACEROUTE': None, 'DELAY': None, 'LATENCY': None}
    df = pd.DataFrame(dict)
    print(df)
    prepare_data(name,df,True)

main()
