import pandas as pd
import math

def parse_files(name):
    file_path = '../data/' + name + '.txt'
    csv_data = pd.read_csv(
        file_path,
        sep='\t',
        names=['Date', 'TTL', 'Traceroute', 'Delay', 'Latency']
    )

    latency_lst = []
    delay_lst = []
    ttl_lst = []
    traceroute_lst = []

    csv_data['Traceroute'] = csv_data['Traceroute'].str.split(' ')
    csv_data['Delay'] = csv_data['Delay'].str.split(' ')

    for index in csv_data.index:
        traceroute = parse_traceroute(csv_data.loc[index, "Traceroute"])
        delay = parse_delay(csv_data.loc[index, 'Delay'])
        latency = float(csv_data.loc[index, 'Latency'])
        ttl = float(csv_data.loc[index, 'TTL'])

        if traceroute != 'ERROR' and delay != 'ERROR' and not math.isnan(latency):
            latency_lst.append(latency)
            delay_lst.append(delay)
            ttl_lst.append(ttl)
            traceroute_lst.append(traceroute)
        else:
            continue
    df = pd.DataFrame()
    df['Traceroute'] = traceroute_lst
    df['TTL'] = ttl_lst
    df['Latency'] = latency_lst
    df['Delay'] = delay_lst

    # df.to_csv('./parsed_data/' + name + '.csv')

    return df

def parse_traceroute(traceroute):
    ips = []
    
    for i in range(len(traceroute)):
        if traceroute[i] == '*' or traceroute[i] == '':
            continue
        else:
            ips.append(traceroute[i])
    
    five_ips = []
    for ip in ips[-5:]:
        ip = ip.split('.')
        single_ip = []
        for i in ip:
            if i == '':
                return 'ERROR'
            else:
                single_ip.append(int(i))
        five_ips.append(single_ip[0:3])

    return five_ips

def parse_delay(delay):
    delays = []
    for i in range(len(delay)):
        if delay[i] == '*' or delay[i] == '':
            continue
        else:
            delays.append(float(delay[i]))

    if len(delays) < 5:
        return 'ERROR'
    return delays[-5:]
