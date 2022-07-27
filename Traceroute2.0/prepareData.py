import pandas as pd
import math 

number_of_data = 5

def parse_traceroute(traceroute, binary):
    ips = []

    for i in range(len(traceroute)):
        if traceroute[i] == '*' or traceroute[i] == '':
            continue
        else:
            ips.append(traceroute[i])
    numbers=[]

    if(len(ips) < number_of_data):
        return 'ERROR'

    for ip in ips[-number_of_data:]:
        ip = ip.split('.')
        for num in ip:
            if num == '':
                return 'ERROR'
            else:
                # if binary:
                #     num  = int(num)
                #     num = bin(num)[2:]
                # else:
                num = int(num)
                numbers.append(num)
    return numbers

def parse_delay(delay):
    delays = []
    for i in range(len(delay)):
        if delay[i] == '*' or delay[i] == '':
            continue
        else:
            delays.append(delay[i])
    if len(delays)<number_of_data:
        return 'ERROR'
    return delays[-2:]
     


def prepare_data(name, binary):
    file_path = '../data/' + name + '.txt'
    csv_data = pd.read_csv(
        file_path,
        sep="\t",
        names=["Date", "TTL", "Traceroute", "Delay", "Latency"])

    data = []
    # accuracy = []
    csv_data["Traceroute"] = csv_data["Traceroute"].str.split(" ")
    csv_data['Delay'] = csv_data['Delay'].str.split(' ')

    for index in csv_data.index:
        traceroute = parse_traceroute(csv_data.loc[index, "Traceroute"], binary)
        delay = parse_delay(csv_data.loc[index, 'Delay'])
        latency = float(csv_data.loc[index, 'Latency'])
        ttl = float(csv_data.loc[index, 'TTL'])

        if traceroute != 'ERROR' and delay != 'ERROR' and not math.isnan(latency):
            data_info = []
            data_info.append(latency)
            data_info.append(ttl)
            data_info += traceroute+delay
            data.append(data_info)
        else:
            continue
    # accuracy = [accurate]*len(data)

    data_dictionary = {
        'Data': data,
        'Accurate': [-1]*len(data)
    }
    return pd.DataFrame(data_dictionary)